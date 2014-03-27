from dragonfly import AppContext, Grammar, MappingRule, Dictation, Key, Pause, Function, IntegerRef, Text

import lib.format

class CommandRule(MappingRule):
  mapping = {
    # Code execution.
    "run app": Key("shift:down, f10, shift:up"),
    "re-run app": Key("ctrl:down, f5, ctrl:up"),
    "run test": Key("ctrl:down, shift:down, f10, shift:up, ctrl:up"),
    "stop running": Key("ctrl:down, f2, ctrl:up"),

    # Code navigation.
    "open class <text>": Key("c-n/25") + Function(lib.format.pascal_case_text) + Pause("30") + Key("enter"),
    "open class chooser <text>": Key("c-n/25") + Function(lib.format.pascal_case_text) + Pause("30"),
    "open file <text>": Key("ctrl:down, shift:down, n, shift:up, ctrl:up") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
    "open file chooser <text>": Key("ctrl:down, shift:down, n, shift:up, ctrl:up") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
    "open symbol <text>": Key("ctrl:down, alt:down, shift:down, n, shift:up, alt:up, ctrl:up") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30") + Key("enter"),
    "open symbol chooser <text>": Key("ctrl:down, alt:down, shift:down, n, shift:up, alt:up, ctrl:up") + Pause("30") + Function(lib.format.camel_case_text) + Pause("30"),
    "(go to|open) declaration": Key("c-b"),
    "(go to|open) implementation": Key("ctrl:down, alt:down, b, alt:up, ctrl:up"),
    "(go to|open) super": Key("c-u"),
    "(go to|switch to|open) (class|test)": Key("ctrl:down, shift:down, t, shift:up, ctrl:up"),
    "go back": Key("ctrl:down, alt:down, left, alt:up, ctrl:up"),

    # Project settings.
    "switch to project": Key("a-1"),
    "open module settings": Key("f4"),
    "open [project] settings": Key("ctrl:down, alt:down, s, alt:up, ctrl:up"),
    "synchronize files": Key("ctrl:down, alt:down, y, alt:up, ctrl:up"),

    # Terminal.
    "open terminal": Key("a-f12"),

    # Search.
    "find in path": Key("ctrl:down, shift:down, f, shift:up, ctrl:up"),
    "find usages": Key("a-f7"),

    # Edit.
    "save [file|all]": Key("c-s"),

    # Code.
    "show intentions": Key("a-enter"),
    "accept choice": Key("c-enter"),
    "go to line": Key("c-g"),
    "go to line <n>": Key("c-g/25") + Text("%(n)d") + Key("enter"),
    "[go to] start of line": Key("home"),
    "[go to] end of line": Key("end"),

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
    "run rake [task]": Key("ctrl:down, alt:down, r, alt:up, ctrl:up"),
    "run rake spec": Key("ctrl:down, alt:down, r, alt:up, ctrl:up") + Pause("25") + Text("spec") + Key("enter") + Pause("25") + Key("enter"),
    "run rails generator": Key("ctrl:down, alt:down, g, alt:up, ctrl:up"),

    # Custom key mappings.
    "(start SSH session|open SSH console|open remote terminal|open remote console)": Key("a-f11/25, enter"),
  }

  extras = [
    Dictation("text"),
    IntegerRef("n", 1, 50000)
  ]

idea_context = AppContext(executable="idea")
rubymine_context = AppContext(executable="rubymine")
grammar = Grammar("idea_general", context=(idea_context | rubymine_context))
grammar.add_rule(CommandRule())
#grammar.add_rule(NavigationRule())
grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
