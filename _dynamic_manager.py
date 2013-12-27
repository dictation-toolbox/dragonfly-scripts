"""

"""

from dragonfly import *  # @UnusedWildImport

import dyn_special_commands_one
import dyn_special_commands_two

dynamicLoaded = None


def load_one():
    global dynamicLoaded
    print("Loading one...")
    if dynamicLoaded == "one":
        print("One already loaded.")
        return
    if dynamicLoaded == "two":
        dyn_special_commands_two.dynamic_disable()
    dyn_special_commands_one.dynamic_enable()
    dynamicLoaded = "one"


def unload_one():
    global dynamicLoaded
    dyn_special_commands_one.dynamic_disable()
    dynamicLoaded = None


def load_two():
    global dynamicLoaded
    print("Loading two...")
    if dynamicLoaded == "two":
        print("Two already loaded.")
        return
    if dynamicLoaded == "one":
        dyn_special_commands_one.dynamic_disable()
    dyn_special_commands_two.dynamic_enable()
    dynamicLoaded = "two"


def unload_two():
    global dynamicLoaded
    dyn_special_commands_two.dynamic_disable()
    dynamicLoaded = None


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
        "load special commands one": Function(load_one),
        "unload special commands one": Function(unload_one),
        "load special commands two": Function(load_two),
        "unload special commands two": Function(unload_two),
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
grammar = Grammar("Dynamic loader", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
