"""A command module for Dragonfly, for controlling the native HipChat client.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import Config, Section, Item, AppContext, Grammar, MappingRule, IntegerRef, Dictation, Choice

from lib.dynamic_aenea import (
    DynamicContext,
    Key,
    Text,
)

from aenea.proxy_contexts import ProxyAppContext as NixAppContext

hipchat_config = Config("HipChat")
hipchat_config.usernames = Section("Username Mappings")
hipchat_config.usernames.map = Item(
    {
        "All": "all",
        "Here": "here"
    }
)

hipchat_config.load()

class NavigationRule(MappingRule):
    mapping = {
        "move up [<n>]":                                    Key("cs-tab:%(n)d"),
        "move down [<n>]":                                  Key("c-tab:%(n)d"),
        "close tab":                                        Key("c-w"),
        "(join room | private message) <room>":             Key("c-j/25") + Text("%(room)s") + Key("enter"),
        "search [room] history":                            Key("c-f"),
    }

    extras = [
        IntegerRef("n", 1, 10),
        Dictation("room"),
    ]

    defaults = {
        "n": 1,
    }

class ChatRule(MappingRule):
    mapping = {
        "at <user>":     Text("@%(user)s "),
        "send":          Key("enter"),
    }

    extras = [
        Choice("user", hipchat_config.usernames.map),
    ]


nixContext = NixAppContext(executable="hipchat")
winContext = AppContext(executable="hipchat")

grammar = Grammar("hipchat_general", context=DynamicContext(winContext, nixContext))
grammar.add_rule(NavigationRule())
grammar.add_rule(ChatRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None

