from bpy.types import Panel


# Links footer for legacy (Install from Disk) builds. The row draws nothing while both are empty.
# Before publishing on extensions.blender.org, delete the footer: ADDON_NAME_PT_links, draw_links
# and the call in preferences.py. The platform rules forbid store and donation links in the UI
# (rule 6.1) and forbid touching the OS or other add-ons (rule 3.9).
WEBSITE_URL = ""
BUG_REPORT_URL = ""


def draw_links(layout):
    if not (WEBSITE_URL or BUG_REPORT_URL):
        return
    row = layout.row()
    row.alignment = 'CENTER'
    if WEBSITE_URL:
        row.operator("wm.url_open", text="", icon='URL').url = WEBSITE_URL
    if BUG_REPORT_URL:
        row.operator("wm.url_open", text="", icon='HELP').url = BUG_REPORT_URL


class ADDON_NAME_PT_panel(Panel):
    """PLACEHOLDER: one line saying what this panel does"""

    bl_label = "Addon Name"
    bl_idname = "ADDON_NAME_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Name"

    def draw(self, context):
        layout = self.layout
        props = context.scene.addon_name

        layout.operator("addon_name.example")

        # Settings fold away so the panel stays short until you need them.
        box = layout.box()
        box.prop(
            props, "show_settings",
            icon='DOWNARROW_HLT' if props.show_settings else 'RIGHTARROW',
            emboss=False,
        )
        if props.show_settings:
            box.prop(props, "target")


class ADDON_NAME_PT_links(Panel):
    """Links to the author's website and the bug report page"""

    bl_label = ""
    bl_idname = "ADDON_NAME_PT_links"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Addon Name"
    bl_parent_id = "ADDON_NAME_PT_panel"
    bl_options = {'HIDE_HEADER'}
    # Keeps the links under any sub-panels added later.
    bl_order = 100

    def draw(self, context):
        draw_links(self.layout)
