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
import gpu
from mathutils import Vector, Matrix
from gpu_extras.batch import batch_for_shader
from . preferences import get_preferences


def register_axis_handler(cls):
    if cls.axis_obj is None:
        return

    if not get_preferences().enable_axis_helper:
        return

    handler = bpy.app.driver_namespace.get('nd.axis')

    if not handler:
        handler = bpy.types.SpaceView3D.draw_handler_add(update_axis, (cls, ), 'WINDOW', 'POST_VIEW')
        dns = bpy.app.driver_namespace
        dns['nd.axis'] = handler

        redraw_regions()


def unregister_axis_handler():
    handler = bpy.app.driver_namespace.get('nd.axis')

    if handler:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        del bpy.app.driver_namespace['nd.axis']

        redraw_regions()


def redraw_regions():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    region.tag_redraw()


def init_axis(cls, axis_obj = None, axis = 0):
    cls.axis_obj = axis_obj
    cls.axis = axis
    cls.axis_base_thickness = get_preferences().axis_base_thickness
    cls.axis_active_thickness = get_preferences().axis_active_thickness
    cls.axis_inactive_opacity = get_preferences().axis_inactive_opacity


def update_axis(cls):
    if cls.axis_obj is None:
        return

    axes = [
        (Vector((1, 0, 0)), (226/255, 54/255, 54/255)),
        (Vector((0, 1, 0)), (130/255, 221/255, 85/255)),
        (Vector((0, 0, 1)), (74/255, 144/255, 226/255)),
    ]

    for counter, conf in enumerate(axes):
        axis, color = conf
        coords = []

        mx = cls.axis_obj.matrix_world
        origin = mx.decompose()[0]

        # Draw the axis through the origin point.
        coords.append(origin + mx.to_3x3() @ axis * -1000)
        coords.append(origin + mx.to_3x3() @ axis * 1000)

        shader = gpu.shader.from_builtin('3D_UNIFORM_COLOR')
        shader.bind()
        shader.uniform_float("color", (*color, 1 if counter == cls.axis else cls.axis_inactive_opacity))

        gpu.state.depth_test_set('NONE')
        gpu.state.blend_set('ALPHA')
        gpu.state.line_width_set(
            cls.axis_active_thickness if counter == cls.axis else cls.axis_base_thickness
        )

        batch = batch_for_shader(
            shader,
            'LINES',
            {"pos": coords},
            indices=[(i, i + 1) for i in range(0, len(coords), 2)]
        )
        
        batch.draw(shader)

    redraw_regions()
