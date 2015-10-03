"""A command module for Dragonfly, for controlling eclipse.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""
from dragonfly import (
    MappingRule,
    AppContext,
    IntegerRef,
    Grammar,
)

from lib.dynamic_aenea import (
    DynamicContext,
    Key,
)

from aenea.proxy_contexts import ProxyAppContext as NixAppContext


rules = MappingRule(
    mapping={
        # Commands:
        "activate editor": Key("f12"),
        "apply (fix|correction)": Key("c-1"),
        "choose editor": Key("cs-e"),
        "close tab": Key("c-w"),
        "close all tab": Key("cs-w"),
        "debug": Key("f11"),
        "duplicate down [<n>]": Key("ca-down:%(n)d"),
        "duplicate up [<n>]": Key("ca-up:%(n)d"),
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
        "previous tab [<n>]": Key("c-pgup/10:%(n)d"),
        "next tab [<n>]": Key("c-pgdown/10:%(n)d"),
        "terminate": Key("c-f2"),  # Stop debug session.
        "terminate all launches": Key("ca-f9"),  # Will switch TTY in Linux!!
        "toggle breakpoint": Key("cs-b"),
        "toggle comment": Key("c-slash"),
        "toggle (tab|editor)": Key("c-f6"),
        "toggle expand": Key("c-m"),
        "toggle perspective": Key("c-f8"),
        "toggle view": Key("c-f7"),
        "save file": Key("c-s"),
        "save all": Key("cs-s"),
        "show file menu": Key("apps"),
        "show content assist": Key("c-space"),
        "show system menu": Key("a-minus"),
        "show shortcuts": Key("cs-l"),
        "show file properties": Key("a-enter"),
        "show view menu": Key("c-f10"),
        "show editors": Key("c-e"),
    },
    extras=[
        IntegerRef("n", 1, 100),
    ],
    defaults={
        "n": 1
    }
)
winContext1 = AppContext(executable="javaw", title="Eclipse")
winContext2 = AppContext(executable="eclipse", title="Eclipse")
winContext = winContext1 | winContext2

nixContext = NixAppContext(executable="java", title="Eclipse")


grammar = Grammar("Eclipse", context=DynamicContext(winContext, nixContext))
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
