import os
import winsound

from dragonfly import *  # @UnusedWildImport


WORKING_PATH = os.path.dirname(os.path.abspath(__file__))
SOUND_PATH = os.path.join(WORKING_PATH, "resources/sound/")
SOUND_NOTIFY_LOADED = os.path.join(SOUND_PATH, "notify_load.wav")
SOUND_NOTIFY_UNLOADED = os.path.join(SOUND_PATH, "notify_unload.wav")


def notify_module_loaded():
    print("--> Module loaded: Special Commands One")
    play_sound(SOUND_NOTIFY_LOADED)


def notify_module_unloaded():
    print("<-- Module unloaded: Special Commands One")
    play_sound(SOUND_NOTIFY_UNLOADED)


def play_sound(sound):
    flags = winsound.SND_FILENAME | winsound.SND_NODEFAULT | winsound.SND_ASYNC
    winsound.PlaySound(sound, flags)


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
        # Experimentation:
        "show me the money": Text("$ONE$\n"),
        "notify me": Function(notify_module_loaded),
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
grammar = Grammar("special_commands_one", context=global_context)
grammar.add_rule(special_commands_one)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar:
        grammar.enable()
        notify_module_loaded()


def dynamic_disable():
    global grammar
    if grammar:
        grammar.disable()
        notify_module_unloaded()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
