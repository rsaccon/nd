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
import blf
from . preferences import get_preferences


def register_draw_handler(cls, callback):
    handler = bpy.app.driver_namespace.get('nd.overlay')

    if not handler:
        handler = bpy.types.SpaceView3D.draw_handler_add(callback, (cls, ), 'WINDOW', 'POST_PIXEL')
        dns = bpy.app.driver_namespace
        dns['nd.overlay'] = handler

        redraw_regions()


def unregister_draw_handler():
    handler = bpy.app.driver_namespace.get('nd.overlay')

    if handler:
        bpy.types.SpaceView3D.draw_handler_remove(handler, 'WINDOW')
        del bpy.app.driver_namespace['nd.overlay']

        redraw_regions()


def redraw_regions():
    for area in bpy.context.window.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    region.tag_redraw()


def toggle_pin_overlay(cls, event):
    cls.overlay_x = event.mouse_x - cls.region_offset_x + cls.overlay_offset_x
    cls.overlay_y = event.mouse_y - cls.region_offset_y + cls.overlay_offset_y

    cls.pin_overlay = not cls.pin_overlay

    if get_preferences().lock_overlay_pinning:
        get_preferences().overlay_pinned = cls.pin_overlay
        get_preferences().overlay_pin_x = cls.overlay_x
        get_preferences().overlay_pin_y = cls.overlay_y


def toggle_operator_passthrough(cls):
    cls.operator_passthrough = not cls.operator_passthrough


def init_overlay(cls, event):
    cls.overlay_offset_x = 25
    cls.overlay_offset_y = -15

    cls.line_step = 0
    cls.dpi = get_preferences().overlay_dpi
    cls.dpi_scalar = cls.dpi / 72
    cls.line_spacer = 40 * cls.dpi_scalar
    
    cls.region_offset_x = event.mouse_x - event.mouse_region_x
    cls.region_offset_y = event.mouse_y - event.mouse_region_y

    cls.overlay_x = event.mouse_x - cls.region_offset_x + cls.overlay_offset_x
    cls.overlay_y = event.mouse_y - cls.region_offset_y + cls.overlay_offset_y

    cls.pin_overlay = False
    cls.operator_passthrough = False
    cls.mouse_warped = False

    if get_preferences().lock_overlay_pinning:
        cls.pin_overlay = get_preferences().overlay_pinned
        cls.overlay_x = get_preferences().overlay_pin_x
        cls.overlay_y = get_preferences().overlay_pin_y


def update_overlay(cls, context, event):
    if not cls.pin_overlay:
        cls.overlay_x = event.mouse_x - cls.region_offset_x + cls.overlay_offset_x
        cls.overlay_y = event.mouse_y - cls.region_offset_y + cls.overlay_offset_y

    if not cls.operator_passthrough and get_preferences().enable_mouse_values:
        wrap_cursor(cls, context, event)

    redraw_regions()


def wrap_cursor(cls, context, event):
    if event.mouse_region_x <= 0:
        mouse_x = context.region.width + cls.region_offset_x - 10
        context.window.cursor_warp(mouse_x, event.mouse_y)
        cls.mouse_warped = True

    if event.mouse_region_x >= context.region.width - 1:
        mouse_x = cls.region_offset_x + 10
        context.window.cursor_warp(mouse_x, event.mouse_y)
        cls.mouse_warped = True

    if event.mouse_region_y <= 0:
        mouse_y = context.region.height + cls.region_offset_y - 10
        context.window.cursor_warp(event.mouse_x, mouse_y)

    if event.mouse_region_y >= context.region.height - 1:
        mouse_y = cls.region_offset_y + 100
        context.window.cursor_warp(event.mouse_x, mouse_y)


def draw_header(cls):
    is_summoned = getattr(cls, "summoned", False)

    if cls.operator_passthrough:
        blf.color(0, 238/255, 59/255, 43/255, 1.0)
    elif is_summoned and not cls.operator_passthrough:
        blf.color(0, 82/255, 224/255, 82/255, 1.0)
    else:
        blf.color(0, 255/255, 135/255, 55/255, 1.0)

    if cls.operator_passthrough or is_summoned or cls.pin_overlay:
        blf.size(0, 11, cls.dpi)
        blf.position(0, cls.overlay_x + (1 * cls.dpi_scalar), cls.overlay_y + (26 * cls.dpi_scalar), 0)

        states = []
        if cls.operator_passthrough:
            states.append("PAUSED")
        if is_summoned:
            states.append("RECALL")
        if cls.pin_overlay:
            states.append("PINNED")

        blf.draw(0, " // ".join(states))

    blf.size(0, 24, cls.dpi) 
    blf.position(0, cls.overlay_x, cls.overlay_y, 0)
    blf.draw(0, "ND — " + cls.bl_label)

    cls.line_step = 0


def draw_property(cls, property_content, metadata_content, active=False, alt_mode=False, mouse_value=False, input_stream=None):
    blf.size(0, 28, cls.dpi)

    is_ok, is_value, is_raw = input_stream or (False, None, None)
    
    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    elif is_value is not None and active:
        blf.color(0, 237/255, 185/255, 94/255, 1.0)
    elif active:
        blf.color(0, 55/255, 174/255, 255/255, 1.0)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 0.1)
    
    blf.position(0, cls.overlay_x, cls.overlay_y - ((38 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
    
    if not cls.operator_passthrough and alt_mode:
        blf.draw(0, "◑")
    else:
        blf.draw(0, "●")

    if get_preferences().enable_mouse_values and mouse_value:
        blf.size(0, 22, cls.dpi)
        blf.position(0, cls.overlay_x - (15 * cls.dpi_scalar), cls.overlay_y - ((34 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
        blf.draw(0, "»")

    blf.size(0, 16, cls.dpi)

    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 1.0)

    blf.position(0, cls.overlay_x + (25 * cls.dpi_scalar), cls.overlay_y - ((25 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
    blf.draw(0, property_content)
    
    blf.size(0, 11, cls.dpi)
    
    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 0.3)

    blf.position(0, cls.overlay_x + (25 * cls.dpi_scalar), cls.overlay_y - ((40 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)

    if is_value is not None:
        blf.draw(0, "Manual Override — [{}] to reset.".format(get_preferences().overlay_reset_key))
    else:
        blf.draw(0, metadata_content)

    cls.line_step += 1


def draw_hint(cls, hint_content, metadata_content):
    blf.size(0, 22, cls.dpi)
    
    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 0.5)

    blf.position(0, cls.overlay_x - (3 * cls.dpi_scalar), cls.overlay_y - ((36 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
    blf.draw(0, "◈")

    blf.size(0, 16, cls.dpi)

    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 1.0)

    blf.position(0, cls.overlay_x + (25 * cls.dpi_scalar), cls.overlay_y - ((25 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
    blf.draw(0, hint_content)
    
    blf.size(0, 11, cls.dpi)
    
    if cls.operator_passthrough:
        blf.color(0, 255/255, 255/255, 255/255, 0.2)
    else:
        blf.color(0, 255/255, 255/255, 255/255, 0.3)

    blf.position(0, cls.overlay_x + (25 * cls.dpi_scalar), cls.overlay_y - ((40 * cls.dpi_scalar) + (cls.line_spacer * cls.line_step)), 0)
    blf.draw(0, metadata_content)

    cls.line_step += 1
