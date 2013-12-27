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


special_commands_one = SeriesMappingRule(
    mapping={
        # Keywords:
        "and": Text(" and "),
        "or": Text(" or "),
        "comment": Text("# "),
        "(def|define|definition)": Text("def "),
        "doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),
        "else": Text("else:\n"),
        "(el if|else if)": Text("elif "),
        "equals": Text(" == "),
        "false": Text("False"),
        "for": Text("for"),
        "if": Text("if"),
        "import": Text("import"),
        "not equals": Text(" != "),
        "raise exception": Text("raise Exception()") + Key("left"),
        "return": Text("return"),
        "true": Text("True"),
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
grammar = Grammar("Python grammar", context=global_context)
grammar.add_rule(special_commands_one)
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
