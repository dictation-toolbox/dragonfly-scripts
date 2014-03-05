"""A command module for Dragonfly, for controlling the browsers
Firefox and Chrome (and Chromium).

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

import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    from proxy_nicknames import Key  # @Reimport
    import aenea
    from proxy_nicknames import AppContext as NixAppContext


mapping = {
   "go back [<n>]": Key("a-left/15:%(n)d"),
   "go forward [<n>]": Key("a-right/15:%(n)d"),
   "[open] new window": Key("c-n"),
   "[open] new tab": Key("c-t"),
   "close tab": Key("c-w"),
   "close <n> tabs": Key("c-w/20:%(n)d"),
   "next tab [<n>]": Key("c-tab:%(n)d"),
   "previous tab [<n>]": Key("cs-tab:%(n)d"),
   "go to search [bar]": Key("c-k"),
   "go to address [bar]": Key("a-d"),
   "go to top": Key("home"),
   "go to bottom": Key("end"),
   "copy address": Key("a-d/10, c-c/10"),
   "paste address": Key("a-d/10, c-v/10"),
   "go home": Key("a-home"),
   "stop loading": Key("escape"),
   "reload [page]": Key("f5"),

   "bookmark [this] page": Key("c-d"),

   "normal text size": Key("c-0"),
   "decrease text size [<n>]": Key("c-minus:%(n)d"),
   "increase text size [<n>]": Key("cs-plus:%(n)d"),

   "find in page": Key("c-f"),
   "close find": Key("escape"),
   "find previous [<n>]": Key("s-f3/10:%(n)d"),
   "find next [<n>]": Key("f3/10:%(n)d"),
}


context = None
if config.get("aenea.enabled", False) == True:
    mapping.update({
        "go to tab [<n>]": Key("a-%(n)d"),  # Uses alt-key.
    })
    gt = aenea.global_context
    nixContext1 = NixAppContext(executable="firefox", title="Firefox") & gt
    nixContext2 = NixAppContext(executable="chrome", title="Chrome") & gt
    nixContext3 = NixAppContext(executable="chrome", title="Chromium") & gt
    context = nixContext1 | nixContext2 | nixContext3
else:
    mapping.update({
        "go to tab [<n>]": Key("c-%(n)d"),  # Uses ctrl-key.
    })
    winContext1 = AppContext(executable="firefox", title="Firefox")
    winContext2 = AppContext(executable="chrome", title="Chrome")
    winContext3 = AppContext(executable="chrome", title="Chromium")
    context = winContext1 | winContext2 | winContext3


rules = MappingRule(
    mapping=mapping,
    extras=[
        IntegerRef("n", 1, 100),
    ],
    defaults={
        "n": 1
    }
)


grammar = Grammar("FF and Chrome", context=context)
grammar.add_rule(rules)
grammar.load()


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
