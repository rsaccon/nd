bl_info = {
    "name": "HugeMenace — ND",
    "author": "HugeMenace",
    "version": (1, 19, 0),
    "blender": (3, 0, 0),
    "location": "N Panel, Shift + 2",
    "description": "Non-destructive operations, tools, and generators.",
    "warning": "",
    "doc_url": "https://hugemenace.co",
    "category": "3D View"
}


import bpy
import rna_keymap_ui
from bpy.types import AddonPreferences
from bpy.props import BoolProperty, IntProperty, StringProperty, EnumProperty
from . import lib
from . import booleans
from . import interface
from . import sketching
from . import power_mods
from . import generators
from . import utils
from . import viewport


registerables = (
    booleans,
    interface,
    sketching,
    power_mods,
    generators,
    utils,
    viewport,
)


class NDPreferences(AddonPreferences):
    bl_idname = __name__

    update_available: BoolProperty(
        name="Update Available",
        default=False,
    )

    enable_quick_favourites: BoolProperty(
        name="Enable Quick Favourites",
        default=False,
    )

    utils_collection_name: StringProperty(
        name="Utils Collection Name",
        default="Utils",
    )

    overlay_dpi: IntProperty(
        name="Overlay DPI",
        default=72,
        min=1,
        max=300,
        step=1,
    )

    tabs: EnumProperty(
        name="Tabs",
        items=[
            ("GENERAL", "General", ""),
            ("UI", "UI", ""),
            ("KEYMAP", "Keymap", ""),
        ],
        default="GENERAL",
    )


    def draw(self, context):
        layout = self.layout

        column = layout.column(align=True)
        row = column.row()
        row.prop(self, "tabs", expand=True)

        box = layout.box()

        if self.tabs == "GENERAL":
            self.draw_general(box)
        elif self.tabs == "UI":
            self.draw_ui(box)
        elif self.tabs == "KEYMAP":
            self.draw_keymap(box)


    def draw_general(self, box):
        column = box.column(align=True)
        row = column.row()
        row.prop(self, "utils_collection_name")

    
    def draw_ui(self, box):
        column = box.column(align=True)
        row = column.row()
        row.prop(self, "overlay_dpi")

        column = box.column(align=True)
        row = column.row()
        row.prop(self, "enable_quick_favourites")

    
    def draw_keymap(self, box):
        name = "ND v%s" % ('.'.join([str(v) for v in bl_info['version']]))
        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user
        
        for keymap in ['3D View', 'Mesh', 'Object Mode']:
            km = kc.keymaps.get(keymap)

            column = box.column(align=True)
            row = column.row()
            row.label(text=keymap)

            for kmi in km.keymap_items:
                if kmi.idname == "wm.call_menu" and kmi.name.startswith(name):
                    column = box.column(align=True)
                    row = column.row()
                    rna_keymap_ui.draw_kmi(["ADDON", "USER", "DEFAULT"], kc, km, kmi, row, 0)


def register():
    lib.reload()

    for registerable in registerables:
        registerable.reload()
        registerable.register()

    bpy.utils.register_class(NDPreferences)

    lib.preferences.get_preferences().update_available = lib.updates.update_available(bl_info['version'])


def unregister():
    for registerable in registerables:
        registerable.unregister()

    bpy.utils.unregister_class(NDPreferences)