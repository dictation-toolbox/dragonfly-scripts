"""A command module for Dragonfly, for controlling the mouse using a grid.

This is still an experimental functionality. It may contain several bugs,
and it may be heavily modified.

Apart from the normal mouse grid, this grid is made to support multiple
monitors, ctrl-click and shift-click.
So far this is only tested on a dual screen setup.

-----------------------------------------------------------------------------
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from dragonfly import (
    MappingRule,
    Function,
    IntegerRef,
    Choice,
    Dictation,
    Grammar,
#     AppContext,
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    should_send_to_aenea,
)

import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    import lib.grid_base_x

import  lib.grid_base_win


def mouse_pos(pos1, pos2=None, pos3=None, pos4=None, pos5=None, pos6=None,
              pos7=None, pos8=None, pos9=None, action=None):
    if should_send_to_aenea():
        lib.grid_base_x.mouse_pos(pos1, pos2, pos3, pos4, pos5, pos6, pos7,
            pos8, pos9, action)
    else:
        lib.grid_base_win.mouse_pos(pos1, pos2, pos3, pos4, pos5, pos6, pos7,
            pos8, pos9, action)


def left_click():
    if should_send_to_aenea():
        lib.grid_base_x.left_click()
    else:
        lib.grid_base_win.left_click()


def right_click():
    if should_send_to_aenea():
        lib.grid_base_x.right_click()
    else:
        lib.grid_base_win.right_click()


def double_click():
    if should_send_to_aenea():
        lib.grid_base_x.double_click()
    else:
        lib.grid_base_win.double_click()


def control_click():
    if should_send_to_aenea():
        lib.grid_base_x.control_click()
    else:
        lib.grid_base_win.control_click()


def shift_click():
    if should_send_to_aenea():
        lib.grid_base_x.shift_click()
    else:
        lib.grid_base_win.shift_click()


def mouse_mark():
    if should_send_to_aenea():
        lib.grid_base_x.mouse_mark()
    else:
        lib.grid_base_win.mouse_mark()


def mouse_drag():
    if should_send_to_aenea():
        lib.grid_base_x.mouse_drag()
    else:
        lib.grid_base_win.mouse_drag()


def hide_grids():
    if should_send_to_aenea():
        lib.grid_base_x.hide_grids()
    else:
        lib.grid_base_win.hide_grids()


def go():
    if should_send_to_aenea():
        lib.grid_base_x.go()
    else:
        lib.grid_base_win.go()


def unload_grids():
    if should_send_to_aenea():
        pass  # The grid Windows are on the server side, no need to unload.
    else:
        lib.grid_base_win.unload_grids()


actions = {
    "[left] click": left_click,
    "right click": right_click,
    "double click": double_click,
    "control click": control_click,
    "shift click": shift_click,
    "mark": mouse_mark,
    "drag": mouse_drag,
    "go": go,
}


navigate_rule = MappingRule(
    mapping={
        "<pos1> [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>] [<action>]": Function(mouse_pos),  # @IgnorePep8
        "[left] click": Function(left_click),
        "right click": Function(right_click),
        "double click": Function(double_click),
        "control click": Function(control_click),
        "shift click": Function(shift_click),
        "mark": Function(mouse_mark),
        "drag": Function(mouse_drag),
        "(close|cancel|stop|abort) [[mouse] grid]": Function(hide_grids),  # @IgnorePep8
        "go": Function(go),
    },
    extras=[  # Interval 1-9.
        IntegerRef("pos1", 1, 10),
        IntegerRef("pos2", 1, 10),
        IntegerRef("pos3", 1, 10),
        IntegerRef("pos4", 1, 10),
        IntegerRef("pos5", 1, 10),
        IntegerRef("pos6", 1, 10),
        IntegerRef("pos7", 1, 10),
        IntegerRef("pos8", 1, 10),
        IntegerRef("pos9", 1, 10),
        Dictation("text"),
        Choice("action", actions),
    ],
    defaults={
        "pos1": 1
    }
)

# Use global context, and activate/deactivate grammar dynamically.
grammarNavigation = Grammar("Grid navigation", context=GlobalDynamicContext())
grammarNavigation.add_rule(navigate_rule)  # Add the top-level rule.
grammarNavigation.load()  # Load the grammar.
grammarNavigation.disable()


def mouse_grid_start(pos1=None, pos2=None, pos3=None, pos4=None, pos5=None,
    pos6=None, pos7=None, pos8=None, pos9=None, action=None):
    if should_send_to_aenea():
        lib.grid_base_x.set_grammar_reference(grammarNavigation)
        grammarNavigation.enable()
        lib.grid_base_x.mouse_grid(pos1, pos2, pos3, pos4, pos5, pos6, pos7,
            pos8, pos9, action)
    else:
        lib.grid_base_win.set_grammar_reference(grammarNavigation)
        grammarNavigation.enable()
        lib.grid_base_win.mouse_grid(pos1, pos2, pos3, pos4, pos5, pos6, pos7,
            pos8, pos9, action)

init_rule = MappingRule(
    mapping={
        "[mouse] grid [<pos1>] [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>] [<action>]": Function(mouse_grid_start),  # @IgnorePep8
        # In case focus on the grid/grids has been lost.
#         "(close|cancel|stop|abort) [mouse] grid": Function(hide_grids),  # @IgnorePep8
    },
    extras=[
        IntegerRef("pos1", 1, 10),
        IntegerRef("pos2", 1, 10),
        IntegerRef("pos3", 1, 10),
        IntegerRef("pos4", 1, 10),
        IntegerRef("pos5", 1, 10),
        IntegerRef("pos6", 1, 10),
        IntegerRef("pos7", 1, 10),
        IntegerRef("pos8", 1, 10),
        IntegerRef("pos9", 1, 10),
        Dictation("text"),
        Choice("action", actions),
    ],
    defaults={
        "pos1": None
    }
)

grammarInit = Grammar("Grid init", context=GlobalDynamicContext())
grammarInit.add_rule(init_rule)
grammarInit.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammarInit
    if grammarInit:
        grammarInit.unload()
    grammarInit = None
    global grammarNavigation
    if grammarNavigation:
        grammarNavigation.unload()
    grammarNavigation = None
    unload_grids()
