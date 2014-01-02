"""

"""
from dragonfly import *  # @UnusedWildImport

import lib.sound as sound
import dyn_lang_python_grammar
import dyn_lang_javascript_grammar
import dyn_appl_bash_grammar


moduleMapping = {
    "python": dyn_lang_python_grammar,
    "javascript": dyn_lang_javascript_grammar,
    "bash": dyn_appl_bash_grammar
}

incompatibleModules = {
    dyn_lang_python_grammar: [
        dyn_lang_javascript_grammar
    ],
    dyn_lang_javascript_grammar: [
        dyn_lang_python_grammar
    ]
}


def notify_module_enabled(moduleName, useSound=True):
    print("--> Module enabled: %s" % moduleName)
    if useSound:
        sound.play(sound.NOTIFY_ACTIVATE)


def notify_module_disabled(moduleName, useSound=True):
    print("<-- Module disabled: %s" % moduleName)
    if useSound:
        sound.play(sound.NOTIFY_DEACTIVATE)


def notify_module_action_aborted(message, useSound=True):
    print(message)
    if useSound:
        sound.play(sound.NOTIFY_MESSAGE)


def enable_module(module):
    disable_incompatible_modules(module)
    status = module.dynamic_enable()
    moduleName = module.__name__
    if status:
        notify_module_enabled(moduleName)
    else:
        notify_module_action_aborted("Module %s already enabled." % moduleName)


def disable_module(module):
    status = module.dynamic_disable()
    moduleName = module.__name__
    if status:
        notify_module_disabled(moduleName)
    else:
        notify_module_action_aborted("Module %s was not enabled." % moduleName)


def disable_incompatible_modules(enableModule):
    for module in incompatibleModules.get(enableModule, {}):
        status = module.dynamic_disable()
        moduleName = module.__name__
        if status:
            notify_module_disabled(moduleName, useSound=False)
        else:
            notify_module_action_aborted(
                "Module %s was not enabled." % moduleName, useSound=False)


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
        "enable <module> grammar": Function(enable_module),
        "disable <module> grammar": Function(disable_module),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("module", moduleMapping),
    ],
    defaults={
        "n": 1
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Dynamic manager", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
