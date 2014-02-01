import os
import sys

from dragonfly import (Function, MappingRule, IntegerRef, Grammar, Dictation,
    Choice)

# import lib.config
aeneaPath = r"E:\dev\projects\aenea\util"


def init():
    if not aeneaPath in sys.path:
        sys.path.insert(0, aeneaPath)
#     config = lib.config.get_config()
#     print(str(config))
#     cfg = config.get("aenea", {"enabled": False})
#     if cfg["enabled"] == True:
#         path = cfg.get("path")
#         if not path:
#             print("Aenea utilities path not set.")
#         else:  # Set up path to Aenea.
#             print(path)
#             if not path in sys.path:
#                 sys.path.insert(0, path)

init()


# try:
from proxy_nicknames import Key
from proxy_actions import communication
import aenea


def notify_host(text):
    communication.server.notify_host(message=str(text))


def workspace_direction(direction1, direction2=None):
    try:
        Key("Control_R").execute()  # Release VirtualBox keyboard capture.
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
        "write text": Key("A, B, C"),
        "linux test": Key("s-a"),
        "notify host <text>": Function(notify_host),
        "workspace <direction1> [<direction2>]": Function(workspace_direction),
#         "workspace <direction1> ": Function(workspace_direction),
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

grammar = Grammar("Aenea test grammar", context=aenea.global_context)
grammar.add_rule(rules)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
