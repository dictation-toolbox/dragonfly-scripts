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

import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    import aenea
#     from proxy_nicknames import AppContext as NixAppContext
    from lib.grid_base_x import (
        set_grammar_reference,  # @UnusedImport
        left_click,  # @UnusedImport
        right_click,  # @UnusedImport
        double_click,  # @UnusedImport
        control_click,  # @UnusedImport
        shift_click,  # @UnusedImport
        mouse_mark,  # @UnusedImport
        mouse_drag,  # @UnusedImport
        go,  # @UnusedImport
        mouse_grid,  # @UnusedImport
        hide_grids,  # @UnusedImport
        mouse_pos  # @UnusedImport
    )
    unload_grids = lambda: None  # Dummy method.
    context = aenea.global_context
else:
    from lib.grid_base_win import (
        set_grammar_reference,  # @Reimport
        left_click,  # @Reimport
        right_click,  # @Reimport
        double_click,  # @Reimport
        control_click,  # @Reimport
        shift_click,  # @Reimport
        mouse_mark,  # @Reimport
        mouse_drag,  # @Reimport
        go,  # @Reimport
        mouse_grid,  # @Reimport
        hide_grids,  # @Reimport
        mouse_pos,  # @Reimport
        unload_grids
    )
    context = None


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
grammarNavigation = Grammar("Grid navigation", context=context)
grammarNavigation.add_rule(navigate_rule)  # Add the top-level rule.
grammarNavigation.load()  # Load the grammar.
grammarNavigation.disable()


def mouse_grid_start(pos1=None, pos2=None, pos3=None, pos4=None, pos5=None,
    pos6=None, pos7=None, pos8=None, pos9=None, action=None):
    set_grammar_reference(grammarNavigation)
    grammarNavigation.enable()
    mouse_grid(pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, action)

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

grammarInit = Grammar("Grid init", context=context)
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
