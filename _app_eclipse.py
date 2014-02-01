"""A command module for Dragonfly, for controlling eclipse.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import (
    MappingRule,
    IntegerRef,
    Dictation,
    AppContext,
    Grammar,
    Key,
    Text
)


rules = MappingRule(
    mapping={
        # Commands:
        "save": Key("c-s"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

context = AppContext(executable="eclipse")
grammar = Grammar("Eclipse", context=context)
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
