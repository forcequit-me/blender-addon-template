"""The links footer's buttons, with tooltips that say where they go."""

import os

import bpy


class ADDON_NAME_OT_open_link(bpy.types.Operator):
    """Open a page in your browser"""
    bl_idname = "wm.addon_name_open_link"
    bl_label = "Open in Browser"
    bl_options = {'INTERNAL'}

    url: bpy.props.StringProperty()

    @classmethod
    def description(cls, context, properties):
        # Blender's own url_open tooltip only says "open a website", so say which and why
        from .panels import WEBSITE_URL
        if properties.url == WEBSITE_URL:
            return "My website: more add-ons and where to find me. Opens in your browser"
        return "Report a bug or suggest a change for Addon Name. Opens in your browser"

    def execute(self, context):
        bpy.ops.wm.url_open(url=self.url)
        return {'FINISHED'}


# Blender has no GitHub icon, so a bug report page on GitHub gets the GitHub mark from icons/
# (Octicons, MIT, licence beside it)
_icons = None


def github_icon():
    return _icons["github"].icon_id if _icons else 0


def _load_icons():
    global _icons
    import bpy.utils.previews  # here, not at the top: plain-Python tests stub bpy
    _icons = bpy.utils.previews.new()
    _icons.load("github", os.path.join(os.path.dirname(__file__), "icons", "github.png"), 'IMAGE')


def _unload_icons():
    global _icons
    if _icons is not None:
        bpy.utils.previews.remove(_icons)
        _icons = None
