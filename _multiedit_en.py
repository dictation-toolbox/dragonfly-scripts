#
# A command-module for Dragonfly, for generic editing help.
# A modification of the _multiedit-en.py script at:
# http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

from dragonfly import *  # @UnusedWildImport


release = Key("shift:up, ctrl:up")


def reload_natlink():
    win = Window.get_foreground()
    FocusWindow("natspeak", "Messages from Python Macros").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    win.set_foreground()


config = Config("multi edit")
config.cmd = Section("Language section")
config.cmd.map = Item(
    {
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
         "doc home": Key("c-home"),
         "doc end": Key("c-end"),

         "space": release + Key("space"),
         "space [<n>]": release + Key("space:%(n)d"),
         "enter [<n>]": release + Key("enter:%(n)d"),
         "tab [<n>]": Key("tab:%(n)d"),
         "delete [<n>]": release + Key("del:%(n)d"),
         "delete [<n> | this] (line|lines)": release + Key("home, s-down:%(n)d, del"),  # @IgnorePep8
         "backspace [<n>]": release + Key("backspace:%(n)d"),
         "application key": release + Key("apps"),
         "win key": release + Key("win"),

         "paste": release + Key("c-v"),
         "duplicate <n>": release + Key("c-c, c-v:%(n)d"),
         "copy": release + Key("c-c"),
         "cut": release + Key("c-x"),
         "select all": release + Key("c-a"),
         "undo <n> [times]": release + Key("c-z:%(n)d"),
         "redo": release + Key("c-y"),
         "redo <n> [times]": release + Key("c-y:%(n)d"),
         "[hold] shift": Key("shift:down"),
         "release shift": Key("shift:up"),
         "[hold] control": Key("ctrl:down"),
         "release control": Key("ctrl:up"),
         "release [all]": release,

         "say <text>": release + Text("%(text)s"),
         "mimic <text>": release + Mimic(extra="text"),

         "reload Natlink": Function(reload_natlink)
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)


class KeystrokeRule(MappingRule):

    exported = False

    mapping = config.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Dictation("text2"),
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


grammar = Grammar("Multiedit")  # Create this module's grammar.
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
