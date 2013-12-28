from dragonfly import *  # @UnusedWildImport


class SeriesMappingRule(CompoundRule):

    def __init__(self, mapping, extras=None, defaults=None):
        mapping_rule = MappingRule(mapping=mapping, extras=extras,
            defaults=defaults, exported=False)
        single = RuleRef(rule=mapping_rule)
        series = Repetition(single, min=1, max=16, name="series")

        compound_spec = "<series>"
        compound_extras = [series]
        CompoundRule.__init__(self, spec=compound_spec,
            extras=compound_extras, exported=True)

    def _process_recognition(self, node, extras):  # @UnusedVariable
        series = extras["series"]
        for action in series:
            action.execute()


special_commands_two = SeriesMappingRule(
    mapping={
        # Keywords:
        "and": Text(" && "),
        "or": Text(" || "),
        "comment": Text("// "),
        "open comment": Text("/* "),
        "close comment": Text(" */"),
        "equals": Text(" == "),
        "equals (strict|strictly|exact|exactly)": Text(" === "),
        "else": Text("else"),
        "else if": Text("else if("),
        "if": Text("if("),
        "for": Text("for("),
        "false": Text("false"),
        "function": Text("function "),
        "(jQuery (variable|var)|dollar paren)": Text("$()") + Key("left"),
        "new": Text("new "),
        "not equals": Text(" != "),
        "not (strict|strictly|exact|exactly) equals": Text(" !== "),
        "return": Text("return "),
        "throw": Text("throw"),
        "true": Text("true"),
        "(variable|var)": Text("var"),
        "assign": Text(" = "),
        "(plus|add)": Text(" + "),
        "(plus|add) equals": Text(" += "),
        "(minus|subtract)": Text(" - "),
        "(minus|subtract) equals": Text(" -= "),
        "less than": Text(" < "),
        "less equals": Text(" <= "),
        "greater than": Text(" > "),
        "greater equals": Text(" >= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("JavaScript grammar", context=global_context)
grammar.add_rule(special_commands_two)
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


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
