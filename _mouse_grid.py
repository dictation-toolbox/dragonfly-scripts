import os
# import thread

# import subprocess

from dragonfly import *  # @UnusedWildImport

import grid_experiment

WORKING_PATH = os.path.dirname(os.path.abspath(__file__))
GRID_WINDOWS = {}

MONITORS = DictList("MONITORS")
for i, m in enumerate(monitors):
    MONITORS[str(i + 1)] = m
MONITOR_COUNT = len(MONITORS)
MONITOR_SELECTED = None

"""
65537, Rectangle(0.0, 0.0, 1280.0, 948.0)
65539, Rectangle(1280.0, 0.0, 1280.0, 978.0)
"""


def mouse_grid(pos=None):
    global GRID_WINDOWS
    global MONITORS
    global MONITOR_COUNT
    global MONITOR_SELECTED
    if pos:
        if pos <= MONITOR_COUNT:
            print("Selected monitor: %s" % pos)
            index = pos - 1
            monitor = MONITORS[str(pos)]
            r = monitor.rectangle
            win = grid_experiment.TransparentWin(posX=int(r.x), posY=int(r.y),
                totalWidth=int(r.dx), totalHeight=int(r.dy))
            win.update()
            GRID_WINDOWS[index] = win
            win.deiconify()
            win.lift()
            win.focus_force()
            MONITOR_SELECTED = pos
            return

    for index, monitor in MONITORS.items():
        if not index in GRID_WINDOWS.keys():
            r = monitor.rectangle
            win = grid_experiment.TransparentWin(posX=int(r.x), posY=int(r.y),
                totalWidth=int(r.dx), totalHeight=int(r.dy))
            win.update()
            GRID_WINDOWS[index] = win
        else:
            win = GRID_WINDOWS[index]
        win.deiconify()
        win.lift()
        win.focus_force()
        MONITOR_SELECTED = None


def close_grid(exclude=None):
    global GRID_WINDOWS
    global MONITOR_SELECTED
    print("close_grid")
    count = 0
    for index, win in GRID_WINDOWS.items():
        if exclude and str(exclude) == index:
            continue
        win.withdraw()
        count += 1
    if count == len(GRID_WINDOWS):
        MONITOR_SELECTED = None


def mouse_pos(pos1, pos2=None, pos3=None, pos4=None, pos5=None, pos6=None,
              pos7=None, pos8=None, pos9=None):
    global GRID_WINDOWS
    global MONITOR_SELECTED
    if MONITOR_SELECTED != None:
        variables = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    else:
        variables = [pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
        MONITOR_SELECTED = pos1
        close_grid(exclude=pos1)
    positions = [str(var) for var in variables if var != None]
#     print("mouse_pos: %s" % (', '.join(positions)))
    for position in positions:
        _reposition_grid(position)


def _reposition_grid(position):
    global GRID_WINDOWS
    global MONITOR_SELECTED
    print("Reposition: %s" % position)
#     newGeometry = ""
#     win.geometry(newGeometry)


def left_click():
    print("left_click")


def right_click():
    print("right_click")


init_rule = MappingRule(
    mapping={
        "grid [<pos>]": Function(mouse_grid),
        "grid": Function(mouse_grid),
    },
    extras=[
        IntegerRef("pos", 1, 10),
        Dictation("text"),
    ],
    defaults={
        "pos": None
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar1 = Grammar("Grid init", context=global_context)
grammar1.add_rule(init_rule)
grammar1.load()


navigate_rule = MappingRule(
    mapping={
        "<pos1> [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>]": Function(mouse_pos),  # @IgnorePep8
        "[left] click": Function(left_click),
        "right click": Function(right_click),
        "close grid": Function(close_grid),
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
    ],
    defaults={
        "pos1": 1
    }
)

context = AppContext(executable="natspeak", title="Grid overlay")
grammar2 = Grammar("Grid navigation", context=context)
grammar2.add_rule(navigate_rule)  # Add the top-level rule.
grammar2.load()  # Load the grammar.


# Unload function which will be called at unload time.
def unload():
    global grammar1
    if grammar1:
        grammar1.unload()
    grammar1 = None
    global grammar2
    if grammar2:
        grammar2.unload()
    grammar2 = None
