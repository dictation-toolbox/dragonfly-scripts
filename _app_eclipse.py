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
    Grammar,
#     Key,
)

from proxy_nicknames import Key
from proxy_nicknames import AppContext as NixAppContext


rules = MappingRule(
    mapping={
        # Commands:
        "activate editor": Key("f12"),
        "close tab": Key("c-f4"),
        "go to line": Key("c-l"),
        "go to matching bracket": Key("cs-p"),
        "resume": Key("f8"),
        "show system menu": Key("a-minus"),
        "show view menu": Key("c-f10"),
        "step in": Key("f5"),
        "step next": Key("f6"),
        "step out": Key("f7"),
        "choose editor": Key("cs-e"),
        "tab left": Key("c-pgup"),
        "tab right": Key("c-pgdown"),
        "toggle breakpoint": Key("cs-b"),
        "toggle comment": Key("c-slash"),
        "toggle editor": Key("c-f6"),
        "toggle expand": Key("c-m"),
        "toggle perspective": Key("c-f8"),
        "toggle view": Key("c-f7"),
        "save": Key("c-s"),
        "save all": Key("cs-s"),
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
