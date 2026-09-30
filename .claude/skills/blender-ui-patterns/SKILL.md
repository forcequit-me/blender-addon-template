---
name: blender-ui-patterns
description: This template's default UI rules for a Blender add-on and the layout code that implements them - sidebar panel, Settings section, status text, header button, popover, operator dialog, confirmation, preferences screen and the legacy-only links footer. Use when designing or reviewing a panel or preferences screen, or when deciding whether a new control belongs on screen at all.
---

# Blender UI patterns

These are the template's default rules. They come from add-ons that shipped and got used; change them in this skill if your add-on needs different ones.

## The rules

1. **Every visible control has to earn its place.** Before adding a button, ask whether an existing control can absorb it, whether it can live in Settings, or whether it can be automatic. Most good features add no control at all.
2. **One visible control per idea.** A toggle whose label changes beats two buttons. A row icon beats a second list of actions.
3. **Advanced options go in a Settings section, closed by default**, behind a gear (`PREFERENCES` icon). The main panel shows the daily actions only.
4. **A status line says what state the user is in**, in words, without hovering. "Every preset renders here", "No folder saved, using //renders/", "Pick a preset to render". Never leave the user to read a tooltip to find out what will happen.
5. **Labels and tooltips say what happens.** "Delete Empties", not "Execute". Tooltip voice is in the `addon-writing` skill.
6. **Confirm only irreversible actions.** Undoable actions run straight away. Overwriting a file on disk asks first; deleting objects (undoable) does not.
7. **Every operator that changes Blender data is undoable**: `bl_options = {'REGISTER', 'UNDO'}` or `{'UNDO'}`. Operators that only open a folder, a URL or a dialog skip it.
8. **Non-destructive, with one-click restore.** An add-on that swaps the user's materials keeps the originals and brings them back with one click. One that overwrites a preset file backs it up first.
9. **Show counts or a preview before a scary action.** "12 materials into 3" in the confirm dialog; a header icon pressed in only while there is something to act on.
10. **Report what happened**, with numbers and what was skipped: "Removed 14 empties, kept 4 in use", "Purged 37 unused data blocks". `self.report({'INFO'}, ...)`; `'WARNING'` when something was skipped or nothing happened.
11. **Empty states say what to do next**: "No presets yet / Set up your render settings, / then Save Current as Preset."
12. **Sidebar tab (`bl_category`) is the plain add-on name.** Panel `bl_label` too.
13. **Legacy builds carry the links footer on the panel and on the preferences screen** (below). Extensions builds carry none.

## Panel skeleton

```python
class ADDON_NAME_PT_panel(bpy.types.Panel):
    """Main controls for Addon Name"""
    bl_label = "Addon Name"
    bl_idname = "ADDON_NAME_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Name"

    def draw(self, context):
        layout = self.layout
        props = context.scene.addon_name
        row = layout.row()
        row.scale_y = 1.5                      # the one primary action is the only tall row
        row.operator("wm.addon_name_example", icon='PLAY')
        _draw_settings(layout, props)
```

Group with `layout.separator()` between groups and `separator(factor=0.5)` inside a group. A panel with no gaps reads as one undifferentiated stack.

## Settings section closed by default

Draw the disclosure by hand so it stays level with the panel contents. A sub-panel header and `layout.panel()` are both inset by Blender. Both the triangle and the label drive one BoolProperty (default `False`):

```python
def _draw_settings(layout, props):
    open_ = props.show_settings
    layout.separator()
    row = layout.row(align=True)
    row.alignment = 'LEFT'                     # otherwise the label floats mid-panel
    row.prop(props, "show_settings", text="", emboss=False,
             icon='TRIA_DOWN' if open_ else 'TRIA_RIGHT')
    row.prop(props, "show_settings", text="Settings", emboss=False, icon='PREFERENCES')
    if open_:
        col = layout.column(align=True)
        col.prop(props, "keep_format")
```

`layout.panel(idname, default_closed=True)` (4.1+) returns `(header, body)` with `body` `None` when closed. It is fine inside dialogs and preferences, where the inset does not matter.

A collapsed section can still answer its question in the header: a folded "Output" block can show the output folder, greyed, after the title.

## Status line and self-describing toggles

```python
hint = col.row()
hint.enabled = False                           # greyed: information, not a control
hint.label(text=caption)

# A toggle whose text says what is happening now, not a checkbox that contradicts itself
col.prop(props, "keep_format", toggle=True,
         text="Ignore Format Settings" if props.keep_format else "Use Format Settings")
```

Keep the layout the same shape across states: draw a button disabled (`row.enabled = False`) rather than removing it, so the panel does not jump.

## Confirmations and previews

Irreversible action, short question:

```python
def invoke(self, context, event):
    return context.window_manager.invoke_confirm(
        self, event, title="Overwrite Preset?",
        message="The file on disk is replaced with your current settings.",
        confirm_text="Overwrite", icon='WARNING')
```

Preview with counts before a big change (`invoke_props_dialog` plus `draw`):

```python
copies: IntProperty(options={'SKIP_SAVE', 'HIDDEN'})
groups: IntProperty(options={'SKIP_SAVE', 'HIDDEN'})

def invoke(self, context, event):
    self.copies, self.groups = count_duplicates()
    if not self.copies:
        self.report({'INFO'}, "No duplicate materials to merge")
        return {'CANCELLED'}
    return context.window_manager.invoke_props_dialog(
        self, width=360, title="Merge Materials?", confirm_text="Merge")

def draw(self, context):
    self.layout.label(text=f"{self.copies} materials merge into {self.groups}.", icon='INFO')
```

`invoke_confirm` icons: `NONE`, `WARNING`, `QUESTION`, `ERROR`, `INFO`. Dialog labels do not wrap: keep each line under about 50 characters at width 360. Blender fixes the second button to "Cancel", so say in the text what Cancel does if it is not obvious.

## Lists

`template_list` with row actions as icon-only, `emboss=False` operators at the end of the row, destructive one last and furthest from the most used one. Size the list to its contents: `rows=min(max(len(items), 3), 6)`. Hide the list and show an empty-state label when there is nothing in it. For references that can go missing, draw `f"Missing: {item.name}"` with `icon='ERROR'` instead of hiding the row.

## Header buttons and popovers

A header button is for a one-click action or a popover with the whole panel. Show state on the icon itself (`depress=True` while there is work to do). Let the user switch the header and sidebar placements off in preferences, but never both (an update callback turns the other back on).

```python
def draw_header(self, context):
    self.layout.popover("ADDON_NAME_PT_header_popover", text="", icon='PRESET')
# register: bpy.types.VIEW3D_HT_header.append(draw_header); unregister: .remove(draw_header)
```

Popover panels use `bl_region_type = 'HEADER'` and `bl_ui_units_x` for width.

## The links footer (legacy builds only)

Two centred icon buttons: globe (`URL`) to `WEBSITE_URL`, and the bug report button to `BUG_REPORT_URL`: the GitHub mark when that page is on github.com, `HELP` otherwise. Both constants live at the top of `panels.py`, start empty, and `draw_links()` draws nothing while both are empty, so fill them in before shipping a legacy build. In the sidebar it is a header-less sub-panel with `bl_order = 100` so it always sits last:

```python
WEBSITE_URL = ""
BUG_REPORT_URL = ""


def draw_links(layout):
    if not (WEBSITE_URL or BUG_REPORT_URL):
        return
    row = layout.row()
    row.alignment = 'CENTER'
    if WEBSITE_URL:
        row.operator("wm.addon_name_open_link", text="", icon='URL').url = WEBSITE_URL
    if BUG_REPORT_URL:
        if "github.com" in BUG_REPORT_URL:
            row.operator("wm.addon_name_open_link", text="", icon_value=github_icon()).url = BUG_REPORT_URL
        else:
            row.operator("wm.addon_name_open_link", text="", icon='HELP').url = BUG_REPORT_URL


class ADDON_NAME_PT_links(bpy.types.Panel):
    """Links to the author's website and the bug report page"""
    bl_label = ""
    bl_idname = "ADDON_NAME_PT_links"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Name"
    bl_parent_id = "ADDON_NAME_PT_panel"
    bl_options = {'HIDE_HEADER'}
    bl_order = 100

    def draw(self, context):
        draw_links(self.layout)
```

The buttons use the add-on's own `wm.addon_name_open_link` from `links.py`, not Blender's `wm.url_open`, whose tooltip only says "open a website": ours says where each button goes. Blender has no GitHub icon, so `links.py` loads `icons/github.png` (the Octicons mark, MIT, licence beside it) with `bpy.utils.previews`.

The same row, after a `separator()`, ends `AddonPreferences.draw`. An add-on with no settings still gets an `AddonPreferences` class that draws only this row.

**Extensions builds carry no footer.** Rule 6.1 of the extensions platform bans links to commercial or funding sites and donation buttons inside Blender's UI. Before uploading to extensions.blender.org, delete `ADDON_NAME_PT_links`, `draw_links`, the call in preferences, `links.py` and `icons/` by hand (and drop the class from the tuple and the README line about the buttons). `python build.py package --extension` warns, but still builds, while either URL is set.

## Preferences screen

Group with `layout.column(heading="Show In")` and `column(heading="Settings")` rather than boxes of labels. Preferences hold defaults for new scenes and where the UI appears; per-file choices live on the scene.

## Draw code must be cheap and read-only

- Never write to a property in `draw()`; it can loop redraws. Do migrations and backfills in a `load_post` handler.
- Anything that walks `bpy.data` in `draw()` must be cached and invalidated by handlers, and throttled if it can run during a modal grab (for example scan at most every 0.25 s and stop at the first hit; see `blender-performance`).
- Check that the pointer is valid before drawing through it; a deleted ID returns `None`.

## Layout mechanics

- `column(align=True)` and `row(align=True)` pack buttons together; plain ones leave gaps.
- `layout.split(factor=0.3)` for label and field; `grid_flow(columns=0, even_columns=True)` for many checkboxes.
- `row.enabled = False` greys and blocks; `row.active = False` greys but stays clickable; `row.alert = True` tints red for problems.
- `layout.prop(..., expand=True)` turns an enum into a segmented row, good for 2 to 4 modes (Global / This File).
- `layout.progress(factor=, type='BAR', text=)` draws a progress bar for a running batch.
- `prop_search` or a `PointerProperty` field for picking objects and collections; the field keeps working after a rename.
- Icon names: browse with the Icon Viewer add-on, or read `bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items`.

## Before calling a panel done

- Could any control be removed, merged, or moved into Settings?
- Can the user tell the current mode without hovering?
- Is every data-changing operator undoable, and every irreversible one confirmed?
- Does every action report what it did?
- Links footer in the sidebar and in preferences for a legacy build, and none for an extensions build?
- README "How to use" lists every visible control in the order the user meets it (`addon-writing`).
