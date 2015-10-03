"""A command module for Dragonfly, for controlling the Terminator Linux application:

http://gnometerminator.blogspot.com/p/introduction.html

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import AppContext, Function, Grammar, IntegerRef, Key, MappingRule

import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    from aenea import Key  # @Reimport
    from aenea.proxy_contexts import ProxyAppContext as NixAppContext

rules = MappingRule(
    mapping = {
        # Miscellaneous.
        "[start|exit] full screen": Key("f11"),
        "search": Key("cs-f"),
        "(toggle|show|hide) (scroll|scrollbar)": Key("cs-s"),

        # Window management.
        "new window": Key("cs-i"),
        "close window": Key("cs-q"),

        # Tab management.
        "new tab": Key("cs-t"),
        "close tab": Key("cs-w"),
        "rename tab": Key("c-r"),
        "[switch to] next tab": Key("c-pgdown"),
        "[switch to] previous tab": Key("c-pgup"),
        "move tab left": Key("cs-pgup"),
        "move tab right": Key("cs-pgdown"),

        # View management.
        "split horizontally": Key("cs-o"),
        "split vertically": Key("cs-e"),
        "close view": Key("cs-w"),
        "[switch to] next view": Key("c-tab"),
        "[switch to] previous view": Key("cs-tab"),
        "[switch to] left view": Key("a-left"),
        "[switch to] right view": Key("a-right"),
        "[switch to] top view": Key("a-up"),
        "[switch to] bottom view": Key("a-down"),
        "clear (view|tab|window|terminal)": Key("cs-g"),
        "resize left [<n>]": Key("cs-left:%(n)d"),
        "resize right [<n>]": Key("cs-right:%(n)d"),
        "resize up [<n>]": Key("cs-up:%(n)d"),
        "resize down [<n>]": Key("cs-down:%(n)d"),

        # Zoom.
        "(zoom|focus|unzoom|unfocus) (view|tab|terminal)": Key("cs-z"),
        "zoom (100 percent|reset|normal)": Key("c-0"),
        "zoom in": Key("c-plus"),
        "zoom out": Key("c-minus"),

        # Cursor grouping.
        "group all": Key("w-g"),
        "ungroup all": Key("ws-g"),
        "group tab": Key("w-t"),
        "ungroup tab": Key("ws-t"),

        # Copy & paste.
        "copy [that]": Key("cs-c"),
        "paste [that]": Key("cs-v"),
        },

    extras=[
        IntegerRef("n", 1, 100),
    ],
)

# This is a Linux-only application, so only enable the grammar if Aenea is enabled.
if config.get("aenea.enabled", False) == True:
    context = NixAppContext(executable="python")

    grammar = Grammar("Terminator general", context=context)
    grammar.add_rule(rules)
    grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None