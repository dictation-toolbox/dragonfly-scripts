"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from natlink import setMicState
from dragonfly import (
    Key,  # @UnusedImport
    Text,  # @UnusedImport
    Choice,
    Pause,
    Window,
    FocusWindow,
    Config,
    Section,
    Item,
    Function,
    Dictation,
    IntegerRef,
    MappingRule,
    Alternative,
    RuleRef,
    Grammar,
    Repetition,
    CompoundRule
)

import win32con
from dragonfly.actions.keyboard import Typeable
from dragonfly.actions.typeables import typeables
typeables["Control_R"] = Typeable(code=win32con.VK_RCONTROL, name="Control_R")

import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    from proxy_nicknames import Key, Text  # @Reimport
    import aenea

import lib.sound as sound
import lib.format


release = Key("shift:up, ctrl:up")


def cancel_dictation(text=None, text2=None):
    """Used to cancel an ongoing dictation.

    This method only notifies the user that the dictation was in fact canceled,
    with a sound and a message in the Natlink feedback window.
    Example:
    "'random mumbling or other noises cancel dictation'" => No action.

    """
    print("* Dictation canceled, by user command. *")
    sound.play(sound.SND_DING)


def cancel_and_sleep(text=None, text2=None):
    """Used to cancel an ongoing dictation and puts microphone to sleep.

    This method notifies the user that the dictation was in fact canceled,
    with a sound and a message in the Natlink feedback window.
    Then the the microphone is put to sleep.
    Example:
    "'random mumbling or other noises cancel and sleep'" => Microphone sleep.

    """
    print("* Dictation canceled, by user command. Going to sleep. *")
    sound.play(sound.SND_DING)
    setMicState("sleeping")


def reload_natlink():
    """Reloads Natlink and custom Python modules."""
    win = Window.get_foreground()
    FocusWindow(executable="natspeak",
        title="Messages from Python Macros").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    win.set_foreground()


# For repeating of characters.
specialCharMap = {
    "(bar|vertical bar|pipe)": "|",
    "(dash|minus|hyphen)": "-",
    "(dot|period)": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(star|asterisk)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "at": "@",
    "[double] quote": '"',
    "single quote": "'",
    "hash": "#",
    "dollar": "$",
    "percent": "%",
    "and": "&",
    "slash": "/",
    "equal": "=",
    "plus": "+",
    "space": " "
}

# Modifiers for the press-command.
modifierMap = {
    "alt": "a",
    "control": "c",
    "shift": "s",
    "super": "w",
}

# Modifiers for the press-command, if only the modifier is pressed.
singleModifierMap = {
    "alt": "alt",
    "control": "ctrl",
    "shift": "shift",
    "super": "win",
}

letterMap = {
    "(A|alpha)": "a",
    "(B|bravo) ": "b",
    "(C|charlie) ": "c",
    "(D|delta) ": "d",
    "(E|echo) ": "e",
    "(F|foxtrot) ": "f",
    "(G|golf) ": "g",
    "(H|hotel) ": "h",
    "(I|india|indigo) ": "i",
    "(J|juliet) ": "j",
    "(K|kilo) ": "k",
    "(L|lima) ": "l",
    "(M|mike) ": "m",
    "(N|november) ": "n",
    "(O|oscar) ": "o",
    "(P|papa|poppa) ": "p",
    "(Q|quebec|quiche) ": "q",
    "(R|romeo) ": "r",
    "(S|sierra) ": "s",
    "(T|tango) ": "t",
    "(U|uniform) ": "u",
    "(V|victor) ": "v",
    "(W|whiskey) ": "w",
    "(X|x-ray) ": "x",
    "(Y|yankee) ": "y",
    "(Z|zulu) ": "z",
}

numberMap = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}

controlKeyMap = {
    "left": "left",
    "right": "right",
    "up": "up",
    "down": "down",
    "page up": "pgup",
    "page down": "pgdown",
    "home": "home",
    "end": "end",
    "space": "space",
    "enter": "enter",
    "escape": "escape",
    "tab": "tab"
}

# F1 to F12.
functionKeyMap = {
    'F one': 'f1',
    'F two': 'f2',
    'F three': 'f3',
    'F four': 'f4',
    'F five': 'f5',
    'F six': 'f6',
    'F seven': 'f7',
    'F eight': 'f8',
    'F nine': 'f9',
    'F ten': 'f10',
    'F eleven': 'f11',
    'F twelve': 'f12',
}

pressKeyMap = {}
pressKeyMap.update(letterMap)
pressKeyMap.update(numberMap)
pressKeyMap.update(controlKeyMap)
pressKeyMap.update(functionKeyMap)


grammarCfg = Config("multi edit")
grammarCfg.cmd = Section("Language section")
grammarCfg.cmd.map = Item(
    {
        # Navigation keys.
        "up [<n>]": Key("up:%(n)d"),
        "down [<n>]": Key("down:%(n)d"),
        "left [<n>]": Key("left:%(n)d"),
        "right [<n>]": Key("right:%(n)d"),
        "page up [<n>]": Key("pgup:%(n)d"),
        "page down [<n>]": Key("pgdown:%(n)d"),
        "up <n> (page | pages)": Key("pgup:%(n)d"),
        "down <n> (page | pages)": Key("pgdown:%(n)d"),
        "left <n> (word | words)": Key("c-left:%(n)d"),
        "right <n> (word | words)": Key("c-right:%(n)d"),
        "home": Key("home"),
        "end": Key("end"),
        "doc home": Key("c-home/3"),
        "doc end": Key("c-end/3"),
        # Functional keys.
        "space": release + Key("space"),
        "space [<n>]": release + Key("space:%(n)d"),
        "enter [<n>]": release + Key("enter:%(n)d"),
        "tab [<n>]": Key("tab:%(n)d"),
        "delete [<n>]": release + Key("del:%(n)d/5"),
        "delete [<n> | this] (line|lines)": release + Key("home, s-down:%(n)d, del"),  # @IgnorePep8
        "backspace [<n>]": release + Key("backspace:%(n)d"),
        "application key": release + Key("apps/3"),
        "win key": release + Key("win/3"),
        "paste [that]": release + Key("c-v/3"),
        "copy [that]": release + Key("c-c/3"),
        "cut [that]": release + Key("c-x/3"),
        "select all": release + Key("c-a/3"),
        "undo": release + Key("c-z/3"),
        "undo <n> [times]": release + Key("c-z/3:%(n)d"),
        "redo": release + Key("c-y/3"),
        "redo <n> [times]": release + Key("c-y/3:%(n)d"),
        "[(hold|press)] alt": Key("alt:down/3"),
        "release alt": Key("alt:up"),
        "[(hold|press)] shift": Key("shift:down/3"),
        "release shift": Key("shift:up"),
        "[(hold|press)] control": Key("ctrl:down/3"),
        "release control": Key("ctrl:up"),
        "release [all]": release,
        # Type written form of "that which would otherwise not be written".
        "say <text>": release + Text("%(text)s"),
#         "mimic <text>": release + Mimic(extra="text"),
         # Shorthand multiple characters.
        "double <char>": Text("%(char)s%(char)s"),
        "triple <char>": Text("%(char)s%(char)s%(char)s"),
        "double escape": Key("escape, escape"),  # Exiting menus.
        # Keypresses, to get that working in Linux.
        "press right control": Key("Control_R"),
#         "press <modifierSingle>": Key("%(modifierSingle)s"),
#         "press <modifier1> <pressKey> [<n>]": Key("%(modifier1)s-%(pressKey)s:%(n)d"),  # @IgnorePep8
#         "press <modifier1> <modifier2> <pressKey> [<n>]": Key("%(modifier1)s%(modifier2)s-%(pressKey)s:%(n)d"),  # @IgnorePep8
         # Formatting.
        "camel case <text>": Function(lib.format.camel_case_text),
        "camel case <n> [words]": Function(lib.format.camel_case_count),
        "pascal case <text>": Function(lib.format.pascal_case_text),
        "pascal case <n> [words]": Function(lib.format.pascal_case_count),
        "snake case <text>": Function(lib.format.snake_case_text),
        "snake case <n> [words]": Function(lib.format.snake_case_count),
        "squash <text>": Function(lib.format.squash_text),
        "squash <n> [words]": Function(lib.format.squash_count),
        "expand <n> [words]": Function(lib.format.expand_count),
        "uppercase <text>": Function(lib.format.uppercase_text),
        "uppercase <n> [words]": Function(lib.format.uppercase_count),
        "lowercase <text>": Function(lib.format.lowercase_text),
        "lowercase <n> [words]": Function(lib.format.lowercase_count),
        # Text corrections.
        "(add|fix) missing space": Key("a-left, space, a-right"),
        "(delete|remove) (double|extra) (space|whitespace)": Key("a-left, backspace, a-right"),  # @IgnorePep8
        "(delete|remove) (double|extra) (type|char|character)": Key("a-left, del, a-right"),  # @IgnorePep8
        # Canceling of started sentence.
        # Useful for canceling what inconsiderate loud mouths have started.
        "<text> cancel dictation": Function(cancel_dictation),
        "<text> cancel dictation <text2>": Function(cancel_dictation),
        "[<text>] cancel and sleep": Function(cancel_and_sleep),
        "[<text>] cancel and sleep [<text2>]": Function(cancel_and_sleep),
        # Reload Natlink.
        "reload Natlink": Function(reload_natlink),
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)


class KeystrokeRule(MappingRule):
    exported = False
    mapping = grammarCfg.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Dictation("text2"),
        Choice("char", specialCharMap),
        Choice("modifier1", modifierMap),
        Choice("modifier2", modifierMap),
        Choice("modifierSingle", singleModifierMap),
        Choice("pressKey", pressKeyMap),
    ]
    defaults = {
        "n": 1,
    }


alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
single_action = Alternative(alternatives)


sequence = Repetition(single_action, min=1, max=16, name="sequence")


class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
        release.execute()

context = None
if config.get("aenea.enabled", False) == True:
    context = aenea.global_context
grammar = Grammar("Generic edit", context=context)
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
