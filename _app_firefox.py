from dragonfly import AppContext, Grammar, MappingRule, Dictation, Key, Pause, Function, IntegerRef, Text

import lib.format

class CommandRule(MappingRule):
    mapping = {
        "new tab": Key("c-t"),
        "close tab": Key("c-w"),
        "[go to] address bar": Key("a-l"),
    }

    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 50000)
    ]


firefox_context = AppContext(executable="firefox")
grammar = Grammar("firefox_general", context=firefox_context)
grammar.add_rule(CommandRule())
#grammar.add_rule(NavigationRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
