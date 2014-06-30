from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
)

import lib.sound as sound


DYN_MODULE_NAME = "vim"
INCOMPATIBLE_MODULES = []


def enable_insert_mode(char):
    global grammarCommand
    global grammarInsert
    grammarCommand.disable()
    grammarInsert.enable()
    print(char)
    Key(char).execute()
    print("Vim: Insert mode")


def enable_command_mode():
    global grammarCommand
    global grammarInsert
    grammarCommand.enable()
    Key("escape").execute()
    print("Vim: Command mode")


def illegal_command(text):
    sound.play(sound.SND_ERROR)
    print("Vim: Illegal command - '%s'" % str(text))


commandMode = MappingRule(
    mapping={
        # Commands and keywords:
        "append [text]": Function(enable_insert_mode, char="a"),
        "append [text] (to|at) end [of line]": Function(enable_insert_mode, char="A"),  # @IgnorePep8
        "copy [(line|lines)]": Key("y, y"),
        "insert ([text [before]]|mode)": Function(enable_insert_mode, char="i"),  # @IgnorePep8
        "insert [text] at beginning [of line]": Function(enable_insert_mode, char="I"),  # @IgnorePep8
        "insert line before": Function(enable_insert_mode, char="O"),
        "insert line after": Function(enable_insert_mode, char="o"),
        "paste [(line|lines)]": Key("p"),
        "save [file]": Key("colon, w, enter"),
        "save and exit": Key("colon, x, space"),
        "save as": Key("colon, w, space"),
        "undo": Function(enable_command_mode) + Key("u"),
        "yank [(line|lines)]": Key("d, d"),
        "<text>": Function(illegal_command),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)


grammarCommand = Grammar("Vim command grammar", context=GlobalDynamicContext())
grammarCommand.add_rule(commandMode)
grammarCommand.load()
grammarCommand.disable()


insertMode = MappingRule(
    mapping={
        # Commands and keywords:
        "(command mode|press escape)": Function(enable_command_mode),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

grammarInsert = Grammar("Vim insert grammar", context=GlobalDynamicContext())
grammarInsert.add_rule(insertMode)
grammarInsert.load()
grammarInsert.disable()


def dynamic_enable():
    global grammarCommand
    global grammarInsert
    if grammarCommand.enabled:
        return False
    else:
        grammarCommand.enable()
        grammarInsert.disable()  # Initially disabled.
        return True


def dynamic_disable():
    global grammarCommand
    global grammarInsert
    if grammarCommand.enabled or grammarInsert.enabled:
        grammarCommand.disable()
        grammarInsert.disable()
        return True
    else:
        return False


def is_enabled():
    global grammarCommand
    global grammarInsert
    if grammarCommand.enabled or grammarInsert.enabled:
        return True
    else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammarCommand
    global grammarInsert
    if grammarCommand:
        grammarCommand.unload()
    grammarCommand = None
    if grammarInsert:
        grammarInsert.unload()
    grammarInsert
