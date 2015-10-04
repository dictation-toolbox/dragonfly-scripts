"""Module for controlling Unity desktop in Linux.

The contents of this module will only be loaded if the configuration file
config.json says that Aenea is enabled.

------------------------------------------------------------------------------
Licensed under LGPL3

"""
import lib.config
config = lib.config.get_config()

DYN_MODULE_TYPE = "window_manager"
DYN_MODULE_NAME = "unity"
INCOMPATIBLE_MODULES = []

if config.get("aenea.enabled", False) == True:
    from dragonfly import (
        Function,
        MappingRule,
        IntegerRef,
        Grammar,
        Dictation,
        Choice
    )

    from aenea import Key, Mouse
    #from proxy_actions import communication
    import aenea

    def window_direction(winDirection):
        try:
            Key("ctrl:down, alt:down").execute()
            Key("%s/5" % winDirection).execute()
        finally:  # Make sure to release the modifier keys.
            Key("alt:up, ctrl:up").execute()

    windowDirections = {
        "(top|up) left": "KP_Home",
        "(top|up)": "KP_Up",
        "(top|up) right": "KP_Prior",
        "left": "KP_Left",
        "(middle|center)": "KP_Begin",
        "right": "KP_Right",
        "(bottom|down) left": "KP_End",
        "(bottom|down)": "KP_Down",
        "(bottom|down) right": "KP_Next",
    }

    def workspace_direction(direction1, direction2=None):
        try:
            Key("ctrl:down, alt:down, %s/5" % direction1).execute()
            if direction2:
                Key("%s/5" % direction2).execute()
        finally:  # Make sure to release the modifier keys.
            Key("alt:up, ctrl:up").execute()

    def mouse_direction(direction1, n1, direction2=None, n2=0):
        dir1 = {
            "up": (0, -n1),
            "down": (0, n1),
            "right": (n1, 0),
            "left": (-n1, 0)
        }
        Mouse("<%s %s>" % dir1[direction1]).execute()
        if direction2:
            dir2 = {
                "up": (0, -n2),
                "down": (0, n2),
                "right": (n2, 0),
                "left": (-n2, 0)
            }
            Mouse("<%s %s>" % dir2[direction2]).execute()

    def mouse_double_direction(direction1, direction2, n1):
        dir1 = {
            "up": (0, -n1),
            "down": (0, n1),
            "right": (n1, 0),
            "left": (-n1, 0)
        }
        dir2 = {
            "up": (0, -n1),
            "down": (0, n1),
            "right": (n1, 0),
            "left": (-n1, 0)
        }
        directions = (dir1[direction1][0], dir1[direction1][1],
            dir2[direction2][0], dir2[direction2][1])
        Mouse("<%s %s>, <%s %s>" % directions).execute()

    basicDirections = {
        "up": "up",
        "down": "down",
        "right": "right",
        "left": "left"
    }

    def toggle_host_server():
        communication.toggle_server()

    def switch_to_window(text):
        txt = str(text).lower()
        communication.server.switch_to_window(txt)

    rules = MappingRule(
        mapping={
            # Overall navigation.
            "workspace <direction1> [<direction2>]": Function(workspace_direction),  # @IgnorePep8
            "go to launcher": Key("a-f1"),
            "go to hud": Key("win"),
            "go to run": Key("a-f2"),
            "go to spread view": Key("w-w"),
            "go to expo view": Key("w-s"),
            "show panel menu": Key("a-f10"),
            "show window menu": Key("a-space"),
            # Window control
            "close window": Key("a-f4"),
            #"minimize window": Key("ca-KP_Insert"),
            "maximize window": Key("cw-up"),
            "restore window": Key("cw-down"),
            "move window": Key("a-f7"),
            "resize window": Key("a-f8"),
            "place window <winDirection>": Function(window_direction),
            "switch to <text>": Function(switch_to_window),
            "toggle desktop": Key("cw-d"),
            # Mouse commands.
            "mouse [left] click": Mouse("left"),
            "mouse shift [left] click": Key("shift:down/3") + Mouse("left") + Key("shift:up/3"),  # @IgnorePep8
            "mouse control [left] click": Key("ctrl:down/3") + Mouse("left") + Key("ctrl:up/3"),  # @IgnorePep8
            "mouse right click": Mouse("right"),
            "mouse shift right click": Key("shift:down/3") + Mouse("right") + Key("shift:up/3"),  # @IgnorePep8
            "mouse control right click": Key("ctrl:down/3") + Mouse("right") + Key("ctrl:up/3"),  # @IgnorePep8
            "mouse <direction1> <n1> [<direction2> <n2>]": Function(mouse_direction),  # @IgnorePep8
            "mouse <direction1> <direction2> <n1>": Function(mouse_double_direction),  # @IgnorePep8
            # Starting applications.
            "start terminal": Key("ca-t"),
            # Development option only.
            "toggle host server": Function(toggle_host_server),
        },
        extras=[
            IntegerRef("n1", 1, 5000),
            IntegerRef("n2", 1, 5000),
            Dictation("text"),
            Choice("direction1", basicDirections),
            Choice("direction2", basicDirections),
            Choice("winDirection", windowDirections),
        ],
        defaults={
            "n": 1
        }
    )

    grammar = Grammar("Unity desktop grammar", context=aenea.ProxyPlatformContext('linux'))
    grammar.add_rule(rules)
    grammar.load()
    grammar.disable()

    def dynamic_enable():
        global grammar
        if grammar.enabled:
            return False
        else:
            grammar.enable()
            return True


    def dynamic_disable():
        global grammar
        if grammar.enabled:
            grammar.disable()
            return True
        else:
            return False


    def is_enabled():
        global grammar
        if grammar.enabled:
            return True
        else:
            return False

    # Unload function which will be called at unload time.
    def unload():
        global grammar
        if grammar:
            grammar.unload()
        grammar = None
