from dragonfly import AppContext, Grammar, CompoundRule, MappingRule, Dictation, Key, Pause, Function

import lib.format

class CommandRule(MappingRule):
  mapping = {
    # Code execution.
    "run app": Key("shift:down, f10, shift:up"),
    "re-run app": Key("ctrl:down, f5, ctrl:up"),
    "stop running": Key("ctrl:down, f2, ctrl:up"),

    # Code navigation.
    "open class <text>": Key("c-n/25") + Function(lib.format.pascal_case_text) + Pause("30") + Key("enter"),
    "open class chooser <text>": Key("c-n/25") + Function(lib.format.pascal_case_text) + Pause("30"),
    "find usages": Key("a-f7"),
    "(go to|open) declaration": Key("c-b"),
    "(go to|open) implementation": Key("ctrl:down, alt:down, b, alt:up, ctrl:up"),
    "(go to|open) super": Key("c-u"),
    "(go to|switch to|open) test": Key("ctrl:down, shift:down, t, shift:up, ctrl:up"),

    # Project settings.
    "switch to project": Key("a-1"),
    "open module settings": Key("f4"),
    "open [project] settings": Key("ctrl:down, alt:down, s, alt:up, ctrl:up"),
    "synchronize files": Key("ctrl:down, alt:down, y, alt:up, ctrl:up"),

    # Terminal
    "open terminal": Key("a-f12"),
    }

  extras = [
    Dictation("text"),
  ]

#class NavigationRule(CompoundRule):
#  spec = "open class <class_text>"
#  extras = [Dictation("class_text")]
#
#  def _process_recognition(self, node, extras):
#    class_text = extras["class_text"]
#    print "Fuck off: %s" % format_class(class_text.words)
#    Key("c-n/25").execute()
#    Text(format_class(class_text.words), pause=0.1).execute()
#    Key("enter").execute()

#class NavigationRule(MappingRule):
#  mapping = {
#    "open class <class_text>": Key("c-n/25") + Text(class_name(class_text), True) + Key("enter"),
#  }
#
#  extras = [
#    Dictation("class_text"),
#  ]

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
