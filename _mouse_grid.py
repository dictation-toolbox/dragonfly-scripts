import os
import subprocess

from dragonfly import *  # @UnusedWildImport

WORKING_PATH = os.path.dirname(os.path.abspath(__file__))
GRID_WINDOWS = {}


def mouse_grid(n):
    print("mouse_grid")
    path = os.sep.join([WORKING_PATH, "grid_experiment.py"])
    print("exec: %s" % r"C:\Python26\python.exe " + path)
    GRID_WINDOWS['1'] = subprocess.Popen([r"C:\Python26\python.exe", path])
    print("after process...")


def close_grid():
    print("close_grid")


def mouse_pos(n):
    print("mouse_pos")


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

context = AppContext(executable="python", title="Mouse Grid")
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
