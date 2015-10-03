"""A command module for Dragonfly, for controlling IntelliJ IDEA-based IDEs.

-----------------------------------------------------------------------------
Licensed under the LGPL3.

"""

from dragonfly import AppContext, Grammar, MappingRule, Dictation, Pause, Function, IntegerRef

from lib.dynamic_aenea import (
    DynamicAction,
    DynamicContext,
    Key,
    Text,
)

import lib.format

from aenea.proxy_contexts import ProxyAppContext as NixAppContext

mapping = {
    # Code execution.
    "run app": Key("s-f10"),
    "re-run app": Key("c-f5"),
    "run test": Key("cs-f10"),
    "stop running": Key("c-f2"),

    # Code navigation.
    "navigate to class <text>": Key("c-n") + Pause("30") + Function(lib.format.pascal_case_text) + Pause("30") + Key("enter"),
    "navigate to class chooser <text>": Key("c-n") + Pause("30") + Function(lib.format.pascal_case_text) + Pause("30"),
    "navigate to file <text>": Key("cs-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
    "navigate to file chooser <text>": Key("cs-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
    "navigate to symbol <text>": Key("cas-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
    "navigate to symbol chooser <text>": Key("cas-n") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
    "go to declaration": Key("c-b"),
    "go to implementation": Key("ca-b"),
    "go to super": Key("c-u"),
    "go to (class|test)": Key("cs-t"),
    "go back": DynamicAction(Key("ca-left"), Key("as-left")),

    # Project settings.
    "go to project window": Key("a-1"),
    "go to module settings": Key("f4"),
    "go to [project] settings": Key("ca-s"),
    "synchronize files": Key("ca-y"),

    # Terminal.
    "run terminal": Key("a-f12"),

    # Search.
    "find text": Key("c-f"),
    "find in path": Key("cs-f"),
    "find usages": DynamicAction(Key("a-f7"), Key("as-7")),

    # Edit.
    "save [file|all]": Key("c-s"),

    # Code.
    "show intentions": Key("a-enter"),
    "accept choice": Key("c-enter"),
    "go to line": Key("c-g"),
    "go to line <n>": Key("c-g/25") + Text("%(n)d") + Key("enter"),
    "[go to] start of line": Key("home"),
    "[go to] end of line": Key("end"),
    "implement method": Key("c-i"),
    "override method": Key("c-o"),

    # Window handling.
    "next tab": Key("a-right"),
    "previous tab": Key("a-left"),
    "close tab": Key("c-f4"),

    # Version control.
    "show diff": Key("c-d"),

    # Refactoring.
    "(refactor|re-factor) (this|choose)": Key("cas-t"),
    "(refactor|re-factor) rename": Key("s-f6"),
    "(refactor|re-factor) change signature": Key("c-f6"),
    "(refactor|re-factor) move": Key("f6"),
    "(refactor|re-factor) copy": Key("f5"),
    "(refactor|re-factor) safe delete": Key("a-del"),
    "(refactor|re-factor) extract variable": Key("ca-v"),
    "(refactor|re-factor) extract constant": Key("ca-c"),
    "(refactor|re-factor) extract field": Key("ca-f"),
    "(refactor|re-factor) extract parameter": Key("ca-p"),
    "(refactor|re-factor) extract variable": Key("ca-v"),
    "(refactor|re-factor) extract method": Key("ca-m"),
    "(refactor|re-factor) (in line|inline)": Key("ca-n"),

    # Ruby specific.
    "run rake [task]": Key("ca-r"),
    "run rake spec": Key("ca-r") + Pause("25") + Text("spec") + Key("enter") + Pause("25") + Key("enter"),
    "run rails generator": Key("ca-g"),

    # Custom key mappings.
    "(run SSH session|run SSH console|run remote terminal|run remote console)": Key("a-f11/25, enter"),
}

idea_context = NixAppContext(executable="java", title="IntelliJ")
rubymine_context = NixAppContext(executable="java", title="RubyMine")
nixContext = idea_context | rubymine_context

idea_context = AppContext(executable="idea")
rubymine_context = AppContext(executable="rubymine")
winContext = idea_context | rubymine_context

class CommandRule(MappingRule):
    mapping = mapping

    extras = [
        Dictation("text"),
        IntegerRef("n", 1, 50000)
    ]

grammar = Grammar("idea_general", context=DynamicContext(winContext, nixContext))
grammar.add_rule(CommandRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
