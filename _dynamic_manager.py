"""

"""
import os
import winsound

from dragonfly import *  # @UnusedWildImport

import dyn_python_grammar
import dyn_javascript_grammar

dynamicLoaded = None


moduleMapping = {
    "python": dyn_python_grammar,
    "javascript": dyn_javascript_grammar,
}

incompatibleModules = {
    dyn_python_grammar: [
        dyn_javascript_grammar
    ],
    dyn_javascript_grammar: [
        dyn_python_grammar
    ]
}


WORKING_PATH = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = os.path.join(WORKING_PATH, "resources/sound/")
SOUND_NOTIFY_ACTIVATE = os.path.join(SOUND_PATH, "notify_activate.wav")
SOUND_NOTIFY_DEACTIVATE = os.path.join(SOUND_PATH, "notify_deactivate.wav")
SOUND_NOTIFY_MESSAGE = os.path.join(SOUND_PATH, "notify_message.wav")


def notify_module_enabled(moduleName, sound=True):
    print("--> Module enabled: %s" % moduleName)
    if sound:
        play_sound(SOUND_NOTIFY_ACTIVATE)


def notify_module_disabled(moduleName, sound=True):
    print("<-- Module disabled: %s" % moduleName)
    if sound:
        play_sound(SOUND_NOTIFY_DEACTIVATE)


def notify_module_already_enabled(moduleName, sound=True):
    print("Module already enabled.")
    if sound:
        play_sound(SOUND_NOTIFY_MESSAGE)


def play_sound(sound):
    flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT | winsound.SND_ASYNC
    winsound.PlaySound(sound, flags)


def enable_module(module):
    global dynamicLoaded
    disable_incompatible_modules(module)
    status = module.dynamic_enable()
    moduleName = module.__name__
    if status:
        notify_module_enabled(moduleName)
    else:
        notify_module_already_enabled(moduleName)


def disable_module(module):
    moduleName = module.__name__
    global dynamicLoaded
    notify_module_disabled(moduleName)


def disable_incompatible_modules(enableModule):
    for module in incompatibleModules[enableModule]:
        status = module.dynamic_disable()
        if status:
            notify_module_disabled(module.__name__, sound=False)





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
grammar = Grammar("Dynamic loader", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
