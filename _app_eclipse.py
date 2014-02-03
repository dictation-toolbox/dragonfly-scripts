"""A command module for Dragonfly, for controlling eclipse.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""
import sys
aeneaPath = r"E:\dev\projects\aenea\util"
if not aeneaPath in sys.path:
    sys.path.insert(0, aeneaPath)

from dragonfly import (
    MappingRule,
    AppContext,
    IntegerRef,
    Grammar,
#     Key,
)

from proxy_nicknames import Key
from proxy_nicknames import AppContext as NixAppContext


rules = MappingRule(
    mapping={
        # Commands:
        "activate editor": Key("f12"),
        "apply correction": Key("c-1"),
        "close tab": Key("c-w"),
        "close all tab": Key("cs-w"),
        "debug": Key("f11"),
        "find and replace": Key("c-f"),
        "go back": Key("a-right"),
        "go forward": Key("a-left"),
        "go to line": Key("c-l"),
        "go to matching bracket": Key("cs-p"),
        "go to source": Key("f3"),
        "resume": Key("f8"),
        "step in [<n>]": Key("f5/50:%(n)d"),
        "step next [<n>]": Key("f6/50:%(n)d"),
        "step out [<n>]": Key("f7/50:%(n)d"),
        "choose editor": Key("cs-e"),
        "tab left": Key("c-pgup"),
        "tab right": Key("c-pgdown"),
        "terminate all launches": Key("ca-f9"),  # Will switch tty in Linux!!
        "toggle breakpoint": Key("cs-b"),
        "toggle comment": Key("c-slash"),
        "toggle editor": Key("c-f6"),
        "toggle expand": Key("c-m"),
        "toggle perspective": Key("c-f8"),
        "toggle view": Key("c-f7"),
        "save file": Key("c-s"),
        "save all": Key("cs-s"),
        "show file menu": Key("apps"),
        "show system menu": Key("a-minus"),
        "show shortcuts": Key("cs-l"),
        "show view menu": Key("c-f10"),
    },
    extras=[
        IntegerRef("n", 1, 10),
    ],
    defaults={
        "n": 1
    }
)

winContext = AppContext(executable="javaw", title="Eclipse")
nixContext = NixAppContext(executable="java", title="Eclipse")
grammar = Grammar("Eclipse", context=winContext | nixContext)
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
