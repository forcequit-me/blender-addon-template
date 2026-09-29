---
name: threading-async
description: Running long or background work in a Blender 5.0+ add-on without freezing or crashing Blender - bpy is main-thread only, bpy.app.timers for deferred and chunked work, a queue plus timer to hand results from a worker thread back, modal timer operators, job queues driven by handlers (a batch render), and cleanup on unregister and file load. Use for batch jobs, file or network I/O, file watchers, or anything that runs after the operator returns.
---

# Threads, timers and background work

## The one rule

`bpy` is not thread-safe. From a worker thread, never touch `bpy.context`, `bpy.data`, `bpy.ops`, any Blender object, UI or registration. It may seem to work and then crash or corrupt a file later. Threads may only do plain Python: file and network I/O, parsing, maths on copies of data.

See https://docs.blender.org/api/current/info_gotchas_threading.html

## Pick the tool

| Need | Use |
| --- | --- |
| Run something once after register or after the current event | `bpy.app.timers.register(fn, first_interval=0)` |
| Split a long bpy job into slices so the UI stays live | a timer that does one slice and returns the next interval |
| Wait on Blender's own job (a render) | handlers such as `render_complete` / `render_cancel`, plus a timer |
| Slow I/O that does not need bpy (download, big file scan) | `threading.Thread` + `queue.Queue`, drained by a timer |
| Interactive, cancellable with Esc, with progress | modal operator with `event_timer_add` |

Timers run on the main thread, so bpy is safe in them. Return `None` to stop, a float (seconds) to run again.

## Chunked work on a timer

```python
_pending = []

def _tick():
    if not _pending:
        return None
    for obj_name in _pending[:200]:
        obj = bpy.data.objects.get(obj_name)   # look up again: references go stale
        if obj is not None:
            process(obj)
    del _pending[:200]
    tag_redraw()
    return 0.0 if _pending else None            # 0.0 = next event-loop pass

def start(names):
    _pending[:] = names
    if not bpy.app.timers.is_registered(_tick):
        bpy.app.timers.register(_tick, first_interval=0)
```

Work done from a timer is not an operator: it has no undo step of its own and `bpy.context` there has no area or region. Changes the user must be able to undo belong in an operator.

## Worker thread, results back on the main thread

```python
import queue
import threading

_results = queue.Queue()
_stop = threading.Event()

def _worker(paths):
    for path in paths:
        if _stop.is_set():
            return
        _results.put((path, read_header(path)))    # plain Python only
    _results.put(None)                              # done marker

def _drain():
    try:
        while True:
            item = _results.get_nowait()
            if item is None:
                report_done()
                return None
            apply_to_blender(*item)                 # main thread: bpy is fine here
    except queue.Empty:
        return 0.1

def start(paths):
    _stop.clear()
    threading.Thread(target=_worker, args=(paths,), daemon=True).start()
    bpy.app.timers.register(_drain, first_interval=0.1)
```

Pass the thread copies (paths, numbers, numpy arrays), never Blender objects. `daemon=True` so a stuck thread cannot keep Blender from quitting.

## Job queue on Blender's own jobs (a batch render)

A queue that renders several setups one after another:

- A module-level queue and an `_active` flag.
- `render_complete` and `render_cancel` handlers (added on start, removed on finish) schedule the next step. The handlers take `*args` because their arguments have changed across versions.
- The next render starts from a timer, not from inside the handler, and the timer waits while `bpy.app.is_job_running('RENDER')`.
- `bpy.ops.render.render('INVOKE_DEFAULT', ...)` so the render window and Esc work as normal.
- `abort()` clears the queue, removes handlers and timers, restores the user's settings. It runs on `load_post` and first thing in `unregister()`.
- A status line in the panel shows "Rendering 2 of 5: Preview", with a Stop Batch button that is never folded away.

## Modal operator with a timer

```python
class ADDON_NAME_OT_batch(bpy.types.Operator):
    """Process every object in the file, a slice at a time. Esc stops"""
    bl_idname = "wm.addon_name_batch"
    bl_label = "Process All"

    _timer = None

    def invoke(self, context, event):
        self._todo = [o.name for o in bpy.data.objects]
        self._total = len(self._todo)
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.01, window=context.window)
        wm.modal_handler_add(self)
        wm.progress_begin(0, self._total)
        return {'RUNNING_MODAL'}

    def modal(self, context, event):
        if event.type == 'ESC':
            return self._end(context, f"Stopped after {self._total - len(self._todo)} of {self._total}")
        if event.type == 'TIMER':
            for name in self._todo[:100]:
                obj = bpy.data.objects.get(name)
                if obj is not None:
                    process(obj)
            del self._todo[:100]
            context.window_manager.progress_update(self._total - len(self._todo))
            if not self._todo:
                return self._end(context, f"Processed {self._total} objects")
        return {'PASS_THROUGH'}

    def _end(self, context, message):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        wm.progress_end()
        self.report({'INFO'}, message)
        return {'FINISHED'}
```

If the operator defines `__init__`, it must be `__init__(self, *args, **kwargs)` calling `super().__init__(*args, **kwargs)`; the no-argument form fails in 5.0.

## Cleanup

Anything still running when the add-on is disabled or a file is loaded calls into a dead module or a freed scene.

- In `unregister()`, first: set stop flags, `bpy.app.timers.unregister(fn)` if `is_registered`, remove handlers you added.
- In a `@persistent` `load_post` handler: abort jobs tied to the old file's data.
- Keep module state (`_pending`, `_active`) resettable, and reset it in `unregister()`.

## Avoid

- `multiprocessing` inside Blender. Worker processes start a fresh interpreter without `bpy` and are fragile on Windows. If you truly need a separate process, run a small script with `subprocess` and pass data through files.
- `asyncio` event loops. Blender does not drive them; use timers.
- `time.sleep()` on the main thread. It freezes the UI. Return a timer interval instead.
