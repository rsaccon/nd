import importlib
from . import main_ui_panel
from . import utils_ui_panel
from . import main_menu
from . import utils_menu
from . import boolean_menu
from . import bevel_menu
from . import extrude_menu
from . import array_menu


def reload():
    importlib.reload(main_ui_panel)
    importlib.reload(utils_ui_panel)
    importlib.reload(main_menu)
    importlib.reload(utils_menu)
    importlib.reload(boolean_menu)
    importlib.reload(bevel_menu)
    importlib.reload(extrude_menu)
    importlib.reload(array_menu)


def register():
    main_ui_panel.register()
    utils_ui_panel.register()
    main_menu.register()
    utils_menu.register()
    boolean_menu.register()
    bevel_menu.register()
    extrude_menu.register()
    array_menu.register()


def unregister():
    main_ui_panel.unregister()
    utils_ui_panel.unregister()
    main_menu.unregister()
    utils_menu.unregister()
    boolean_menu.unregister()
    bevel_menu.unregister()
    extrude_menu.unregister()
    array_menu.unregister()