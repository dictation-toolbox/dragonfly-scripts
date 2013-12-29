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

"""
65537, Rectangle(0.0, 0.0, 1280.0, 948.0)
65539, Rectangle(1280.0, 0.0, 1280.0, 978.0)
"""


def mouse_grid(num):
    print("mouse_grid")
    if num:
        if num <= MONITOR_COUNT:
            print("Selected monitor: %s" % num)
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


def close_grid():
    print("close_grid")
    for win in GRID_WINDOWS.values():
        win.withdraw()


def mouse_pos(n):
    print("mouse_pos: %s" % n)
    win = GRID_WINDOWS["1"]
    newGeometry = ""
    win.geometry(newGeometry)


def left_click():
    print("left_click")


def right_click():
    print("right_click")


init_rule = MappingRule(
    mapping={
        "[mouse] grid [<num>]": Function(mouse_grid),
    },
    extras=[
        IntegerRef("num", 1, 9),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar1 = Grammar("Mouse grid init", context=global_context)
grammar1.add_rule(init_rule)
grammar1.load()


navigate_rule = MappingRule(
    mapping={
        "<num>": Function(mouse_pos),
        "[left] click": Function(left_click),
        "close grid": Function(close_grid),
    },
    extras=[
        IntegerRef("num", 1, 9),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

context = AppContext(executable="natspeak", title="Mouse Grid")
grammar2 = Grammar("Mouse grid navigation", context=context)
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
