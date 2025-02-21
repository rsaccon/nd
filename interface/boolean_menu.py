# ███╗   ██╗██████╗ 
# ████╗  ██║██╔══██╗
# ██╔██╗ ██║██║  ██║
# ██║╚██╗██║██║  ██║
# ██║ ╚████║██████╔╝
# ╚═╝  ╚═══╝╚═════╝ 
# 
# “Commons Clause” License Condition v1.0
# 
# See LICENSE for license details. If you did not receive a copy of the license,
# it may be obtained at https://github.com/hugemenace/nd/blob/main/LICENSE.
# 
# Software: ND Blender Addon
# License: MIT
# Licensor: T.S. & I.J. (HugeMenace)
# 
# ---
# Contributors: Tristo (HM)
# ---

import bpy
from .. import bl_info


class ND_MT_boolean_menu(bpy.types.Menu):
    bl_label = "Booleans"
    bl_idname = "ND_MT_boolean_menu"


    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_DEFAULT'
        layout.operator("nd.bool_vanilla", text="Difference", icon='MOD_BOOLEAN').mode = 'DIFFERENCE'
        layout.operator("nd.bool_vanilla", text="Union", icon='MOD_BOOLEAN').mode = 'UNION'
        layout.operator("nd.bool_vanilla", text="Intersect", icon='MOD_BOOLEAN').mode = 'INTERSECT'
        layout.separator()
        layout.operator("nd.bool_slice", icon='MOD_BOOLEAN')
        layout.operator("nd.bool_inset", icon='MOD_BOOLEAN')
        

def register():
    bpy.utils.register_class(ND_MT_boolean_menu)
   

def unregister():
    bpy.utils.unregister_class(ND_MT_boolean_menu)
