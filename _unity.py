import sys

from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation,
    Choice
)

aeneaPath = r"E:\dev\projects\aenea\util"  # ToDo: move to configuration.
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
        "show hud": Key("win"),
        "toggle panel menu": Key("a-f10"),
        "toggle desktop": Key("cw-d"),
        "toggle spread mode": Key("w-w"),
        "toggle expo mode": Key("w-s"),
        # Window control
        "close window": Key("a-f4"),
        "minimize window": Key("ca-np0"),
        "maximize window": Key("cw-up"),
        "restore window": Key("cw-down"),
        # Window placement.
        # Numpad keys doesn't seem to work?
        "place window top left": Key("ca-np7"),
        "place window top": Key("ca-np8"),
        "place window top right": Key("ca-np9"),
        "place window left": Key("ca-np4"),
        "place window middle": Key("ca-np5"),
        "place window right": Key("ca-np6"),
        "place window bottom left": Key("ca-np1"),
        "place window bottom": Key("ca-np2"),
        "place window bottom right": Key("ca-np3"),
#         "": Key(""),
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
