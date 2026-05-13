---
name: threading-async
description: Threading and async patterns specific to Blender — bpy is NOT thread-safe, main-thread marshalling via bpy.app.timers, modal operators for non-blocking UI, background I/O. Use for long-running file operations, network requests, or parallel data preprocessing.
---

# Threading and Async Patterns for Blender

Expert knowledge for threading, async operations, and background processing in Blender addons.

## When to Use This Skill
- Long-running I/O operations (file loading, network requests)
- Data preprocessing (calculations, parsing)
- Background monitoring (file watchers, polling)
- Non-blocking UI operations
- Parallel data processing

## CRITICAL WARNINGS

### Blender API is NOT Thread-Safe!
```python
# NEVER DO THIS - Will crash or corrupt data!
import threading

def unsafe_thread():
    # This will crash!
    bpy.ops.mesh.primitive_cube_add()
    obj = bpy.context.active_object  # UNSAFE!
    obj.location.z = 5  # UNSAFE!

threading.Thread(target=unsafe_thread).start()
```

### What You CANNOT Do in Threads
- Access `bpy.context` (will be None or wrong context)
- Call `bpy.ops.*` operators
- Modify `bpy.data.*` (objects, meshes, materials)
- Access `bpy.types.*` instances
- Update UI or viewport
- Register/unregister classes

### What You CAN Do in Threads
- File I/O (reading, writing, parsing)
- Network requests (downloading, API calls)
- Mathematical calculations
- Data structure manipulation (lists, dicts, numpy arrays)
- Image processing (on raw pixel data)
- String processing, JSON parsing
- Heavy computations on pure Python data

## Safe Threading Pattern

### Pattern 1: Prepare in Thread, Apply in Main Thread
```python
import threading
import bpy

class OBJECT_OT_threaded_load(bpy.types.Operator):
    """Load data in thread, apply in main thread"""
    bl_idname = "object.threaded_load"
    bl_label = "Threaded Load"

    _timer = None
    _thread = None
    _result = None
    _finished = False

    def modal(self, context, event):
        if event.type == 'TIMER':
            # Check if thread finished
            if self._finished and self._result is not None:
                # Safe to access bpy here (main thread)
                self.apply_result(context, self._result)
                self.cancel(context)
                return {'FINISHED'}

        return {'PASS_THROUGH'}

    def execute(self, context):
        # Start background thread
        self._thread = threading.Thread(target=self.load_data)
        self._thread.start()

        # Start timer for modal
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)

        return {'RUNNING_MODAL'}

    def load_data(self):
        """Runs in background thread - NO bpy access!"""
        import time
        import json

        # Safe: File I/O
        with open('/path/to/data.json', 'r') as f:
            data = json.load(f)

        # Safe: Data processing
        processed = [self.process_item(item) for item in data]

        # Store result
        self._result = processed
        self._finished = True

    def apply_result(self, context, result):
        """Runs in main thread - bpy access OK!"""
        for item in result:
            bpy.ops.mesh.primitive_cube_add()
            obj = context.active_object
            obj.name = item['name']

        self.report({'INFO'}, f"Loaded {len(result)} items")

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
```

### Pattern 2: Progress Reporting
```python
import threading
import time

class ProgressThread(threading.Thread):
    """Thread with progress reporting"""

    def __init__(self):
        super().__init__()
        self.progress = 0.0
        self.status = "Starting..."
        self.finished = False
        self.error = None

    def run(self):
        try:
            total_steps = 100

            for i in range(total_steps):
                # Do work (no bpy!)
                time.sleep(0.05)  # Simulate work

                # Update progress
                self.progress = (i + 1) / total_steps
                self.status = f"Processing step {i+1}/{total_steps}"

            self.status = "Complete!"
            self.finished = True

        except Exception as e:
            self.error = str(e)
            self.finished = True

# Usage in operator modal
def modal(self, context, event):
    if event.type == 'TIMER':
        if self._thread.finished:
            if self._thread.error:
                self.report({'ERROR'}, self._thread.error)
                return {'CANCELLED'}
            else:
                self.report({'INFO'}, "Processing complete")
                return {'FINISHED'}
        else:
            # Update UI with progress
            progress = int(self._thread.progress * 100)
            context.area.header_text_set(
                f"{self._thread.status} ({progress}%)"
            )

    return {'PASS_THROUGH'}
```

### Pattern 3: Thread Pool for Multiple Tasks
```python
import threading
from concurrent.futures import ThreadPoolExecutor
import time

class OBJECT_OT_parallel_processing(bpy.types.Operator):
    bl_idname = "object.parallel_processing"
    bl_label = "Parallel Processing"

    def execute(self, context):
        # Prepare data (in main thread)
        tasks = [
            {'id': i, 'value': i * 10}
            for i in range(10)
        ]

        # Process in parallel threads
        with ThreadPoolExecutor(max_workers=4) as executor:
            results = list(executor.map(self.process_task, tasks))

        # Apply results (back in main thread)
        for result in results:
            print(f"Task {result['id']}: {result['result']}")

        return {'FINISHED'}

    def process_task(self, task):
        """Runs in thread pool - NO bpy access!"""
        time.sleep(0.5)  # Simulate work

        return {
            'id': task['id'],
            'result': task['value'] ** 2
        }
```

## Using bpy.app.timers (Alternative to Threading)

### Timer-Based Async Operations
```python
import bpy

class OBJECT_OT_timer_based(bpy.types.Operator):
    bl_idname = "object.timer_based"
    bl_label = "Timer Based Operation"

    _step = 0
    _total_steps = 100

    def execute(self, context):
        # Register timer
        bpy.app.timers.register(self.process_step)
        return {'FINISHED'}

    def process_step(self):
        """Called by timer - safe to use bpy!"""
        if self._step < self._total_steps:
            # Do work (bpy access OK in timers)
            bpy.ops.mesh.primitive_cube_add()
            obj = bpy.context.active_object
            obj.location.x = self._step

            self._step += 1

            # Return time until next call (0.1 seconds)
            return 0.1
        else:
            # Return None to stop timer
            print("Timer finished")
            self._step = 0
            return None
```

### Advantages of Timers vs Threading
- Can use bpy.ops and bpy.data safely
- Simpler code, no thread synchronization
- No threading bugs or crashes
- But: Blocks main thread during execution
- Not true parallelism

## When Threading Actually Helps

### Example 1: File Loading
```python
import threading
import json

class FileLoader(threading.Thread):
    """Load large JSON file in background"""

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.data = None
        self.error = None
        self.finished = False

    def run(self):
        try:
            # File I/O is I/O bound - threading helps!
            with open(self.filepath, 'r') as f:
                self.data = json.load(f)

            # Process data (no bpy!)
            self.data = [self.clean_item(item) for item in self.data]

            self.finished = True
        except Exception as e:
            self.error = str(e)
            self.finished = True
```

### Example 2: Network Requests
```python
import threading
import urllib.request
import json

class APIFetcher(threading.Thread):
    """Fetch data from API in background"""

    def __init__(self, url):
        super().__init__()
        self.url = url
        self.result = None
        self.error = None
        self.finished = False

    def run(self):
        try:
            # Network I/O - threading helps!
            with urllib.request.urlopen(self.url) as response:
                data = response.read()
                self.result = json.loads(data)

            self.finished = True
        except Exception as e:
            self.error = str(e)
            self.finished = True
```

## When Threading DOESN'T Help

### Viewport Updates (Main thread only)
```python
# This won't make it faster!
def update_viewport_in_thread():  # DON'T DO THIS
    for obj in objects:
        obj.location.z += 1  # Must be main thread!
```

### bpy.ops Operations (Not thread-safe)
```python
# This will crash!
def add_cubes_in_thread():  # DON'T DO THIS
    for i in range(100):
        bpy.ops.mesh.primitive_cube_add()  # CRASH!
```

### CPU-Bound Pure Python (GIL)
```python
# GIL prevents true parallelism for CPU-bound Python
def heavy_calculation():
    # Pure Python math - threading won't help!
    result = sum(i**2 for i in range(1000000))
    return result

# Use multiprocessing instead for CPU-bound tasks
```

## Multiprocessing Alternative

### For CPU-Bound Tasks
```python
import multiprocessing

def cpu_intensive_task(n):
    """Heavy calculation - benefits from multiprocessing"""
    return sum(i**2 for i in range(n))

class OBJECT_OT_multiprocess(bpy.types.Operator):
    bl_idname = "object.multiprocess"
    bl_label = "Multiprocessing Example"

    def execute(self, context):
        # Prepare tasks
        tasks = [1000000] * 4

        # Process in parallel (true parallelism!)
        with multiprocessing.Pool(processes=4) as pool:
            results = pool.map(cpu_intensive_task, tasks)

        # Use results
        print(f"Results: {results}")

        return {'FINISHED'}
```

### Multiprocessing Caveats
- Can't pass bpy objects between processes
- Higher memory overhead
- More complex error handling
- Startup cost per process

## Thread Safety Utilities

### Thread-Safe Queue
```python
import threading
import queue

class QueueWorker(threading.Thread):
    """Process tasks from queue"""

    def __init__(self, task_queue, result_queue):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.running = True

    def run(self):
        while self.running:
            try:
                # Get task (thread-safe)
                task = self.task_queue.get(timeout=0.1)

                # Process (no bpy!)
                result = self.process(task)

                # Put result (thread-safe)
                self.result_queue.put(result)

                self.task_queue.task_done()
            except queue.Empty:
                continue

    def stop(self):
        self.running = False
```

## Best Practices

### DO:
- Use threading for I/O operations (files, network)
- Process data in threads, apply in main thread
- Use timers for periodic tasks needing bpy access
- Add proper error handling in threads
- Clean up threads in operator cancel()
- Use thread-safe data structures (queue.Queue)

### DON'T:
- Access bpy from threads
- Share mutable state between threads without locks
- Use threading for CPU-bound pure Python
- Forget to join() threads
- Ignore thread exceptions
- Create too many threads (use thread pools)

## Threading Checklist

Before using threading:
- [ ] Is this I/O bound? (files, network) -> Threading helps
- [ ] Is this CPU-bound Python? -> Use multiprocessing instead
- [ ] Do I need bpy access? -> Use timers instead
- [ ] Can I separate data prep from bpy operations?
- [ ] Have I tested thread cleanup on cancel?
- [ ] Do I handle thread errors properly?
- [ ] Is progress reported to user?

## Common Threading Bugs

### Bug 1: Accessing bpy in Thread
```python
# BAD
def thread_func():
    obj = bpy.context.active_object  # None or crash!

# GOOD
def thread_func(obj_name):
    # Process obj_name (string) in thread
    result = process_name(obj_name)
    return result

# In main thread:
obj = bpy.context.active_object
result = apply_result_to_obj(obj, thread_result)
```

### Bug 2: Race Conditions
```python
# BAD
shared_data = []

def thread_func():
    shared_data.append("value")  # Not thread-safe!

# GOOD
import threading

shared_data = []
lock = threading.Lock()

def thread_func():
    with lock:
        shared_data.append("value")  # Thread-safe
```

### Bug 3: Thread Never Finishes
```python
# BAD
def thread_func():
    while True:  # Never stops!
        process_data()

# GOOD
class StoppableThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            process_data()

    def stop(self):
        self.stop_event.set()
```

## Summary

**Threading in Blender:**
- Great for: I/O operations, network requests, data preprocessing
- Not for: bpy operations, viewport updates, pure Python CPU tasks
- Pattern: Prepare in thread -> Apply in main thread
- Alternative: Use bpy.app.timers for simpler async operations

**Key Takeaway:** Threading is a tool, not a solution. Profile first, use appropriately!
