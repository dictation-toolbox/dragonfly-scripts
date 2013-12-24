from dragonfly import *  # @UnusedWildImport


def notification():
    print("Dynamic module two loaded.")
    import winsound
#     winsound.MessageBeep(winsound.MB_OK)
    winsound.PlaySound("SystemExit", winsound.SND_APPLICATION)


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
        # Experimentation:
        "show me the money": Text("$$TWO$$\n"),
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
grammar = Grammar("special_commands_two", context=global_context)
grammar.add_rule(special_commands_two)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar:
        grammar.enable()
        print('...two loaded.')


def dynamic_disable():
    global grammar
    if grammar:
        grammar.disable()
        print('...two unloaded.')


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
