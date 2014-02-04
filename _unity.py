import sys

from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation,
    Choice
)

aeneaPath = r"E:\dev\projects\aenea\util"
if not aeneaPath in sys.path:
    sys.path.insert(0, aeneaPath)

try:
    from proxy_nicknames import Key
#     from proxy_actions import communication
    import aenea
except:
    pass


def workspace_direction(direction1, direction2=None):
    try:
#         Key("Control_R").execute()  # Release VirtualBox keyboard capture.
        Key("ctrl:down, alt:down, %s/5" % direction1).execute()
        if direction2:
            Key("%s/5" % direction2).execute()
    finally:  # Make sure to release the modifier keys.
        Key("alt:up, ctrl:up").execute()


directions = {
    "up": "up",
    "down": "down",
    "right": "right",
    "left": "left"
}


rules = MappingRule(
    mapping={
        # Commands and keywords:
        "workspace <direction1> [<direction2>]": Function(workspace_direction),
        "show launcher": Key("a-f1"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("direction1", directions),
        Choice("direction2", directions)
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Unity desktop contrl grammar", context=aenea.global_context)
grammar.add_rule(rules)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
