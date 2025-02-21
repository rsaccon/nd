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

import importlib
from . import screw
from . import solidify
from . import weighted_normal_bevel
from . import vertex_bevel
from . import mirror
from . import lattice
from . import simple_deform
from . import decimate
from . import weld
from . import profile_extrude
from . import circular_array
from . import array_cubed
from . import edge_bevel
from . import bevel


registerables = (
    screw,
    solidify,
    weighted_normal_bevel,
    vertex_bevel,
    mirror,
    lattice,
    simple_deform,
    decimate,
    weld,
    profile_extrude,
    circular_array,
    array_cubed,
    edge_bevel,
    bevel
)


def reload():
    for registerable in registerables:
        importlib.reload(registerable)


def register():
    for registerable in registerables:
        registerable.register()


def unregister():
    for registerable in registerables:
        registerable.unregister()
    