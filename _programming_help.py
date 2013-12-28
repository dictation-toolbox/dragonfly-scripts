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

series_rule = SeriesMappingRule(
    mapping={
        # Html specific.
        "open html comment": Text("<!-- "),
        "close html comment": Text(" -->"),
        # VBScript specific.
        "variable (dimension|dim)": Text("dim "),
        "foobar": Text("foobar"),
        "foo": Text("foo"),
        "bar": Text("bar"),
        "baz": Text("baz"),
        "qux": Text("qux"),
        # Lorem ipsum.
        "Lorem ipsum [short]": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit."),  # @IgnorePep8
        "Lorem ipsum medium": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),  # @IgnorePep8
        "Lorem ipsum long": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),  # @IgnorePep8
        # File extensions.
        "dot (py|pie|P Y)": Text(".py"),
        "dot T X T": Text(".txt"),
        "dot S H": Text(".sh"),
        # Web url extensions.
        "dot S E": Text(".se"),
        # Protocols.
        "protocol H T T P": Text("http://"),
        "protocol H T T P S": Text("https://"),
        "protocol (git|G I T)": Text("git://"),
        "protocol F T P": Text("ftp://"),
        "protocol S S H": Text("ssh://"),
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
grammar = Grammar("Programming help", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
