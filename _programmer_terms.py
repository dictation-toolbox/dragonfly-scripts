
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

prot = "protocol "

series_rule = SeriesMappingRule(
    mapping={
        # File extensions.
        "dot (py|pie|P Y)": Text(".py"),
        "dot T X T": Text(".txt"),
        "dot S H": Text(".sh"),
        # Web url extensions.
        "dot S E": Text(".se"),
        # Protocols.
        prot + "H T T P": Text("http://"),
        prot + "H T T P S": Text("https://"),
        prot + "(git|G I T)": Text("git://"),
        prot + "F T P": Text("ftp://"),
        prot + "S S H": Text("ssh://"),
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
grammar = Grammar("Programming terms", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
