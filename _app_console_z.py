"""A command module for Dragonfly, for controlling ConsoleZ.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""
from dragonfly import (
    MappingRule,
    AppContext,
    IntegerRef,
    Grammar,
    Key,  # @UnusedImport
)

rules = MappingRule (
    mapping = {
        # Miscellaneous.
        "open settings": Key("c-s"),
        "[start|exit] full screen": Key("f11"),

        # Tab management.
        "[open] new tab": Key("c-f1"),
        "close tab": Key("c-w"),
        "rename tab": Key("c-r"),
        "[switch to] new tab": Key("c-tab"),
        "[switch to] previous tab": Key("cs-tab"),
        "(switch to|go to) tab <n>": Key("c-%(n)d"),

        # View management.
        "split horizontally": Key("cs-o"),
        "split vertically": Key("cs-e"),
        "close view": Key("cs-w"),
        "[switch to] next view": Key("c-pgdown"),
        "[switch to] previous view": Key("c-pgup"),
        "[switch to] left view": Key("a-left"),
        "[switch to] right view": Key("a-right"),
        "[switch to] top view": Key("a-up"),
        "[switch to] bottom view": Key("a-down"),

        # Zoom.
        "zoom 100 percent": Key("c-np0"),
        "zoom in": Key("c-npadd"),
        "zoom out": Key("c-npsub"),

        # Cursor grouping.
        "group all": Key("c-g"),
        "ungroup all": Key("cs-g"),
        "group tab": Key("c-t"),
        "ungroup tab": Key("cs-t"),

        # Copy & paste.
        "select all": Key("c-a"),
        "clear selection": Key("c-del"),
        #"copy (selection|that)": Key("c-insert"),
        #"paste (that)": Key("s-insert"),
        "dump screen buffer": Key("cs-f1"),
    },

    extras=[
        IntegerRef("n", 1, 100),
    ],
)

context = AppContext(executable="console")
grammar = Grammar("ConsoleZ", context=context)
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None