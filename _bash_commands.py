
try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *  # @UnusedWildImport


config = Config("Bash commands")
config.cmd = Section("Language section")
config.cmd.map = Item({
        "(break|control C)": Key("c-c"),
        "cat": Text("cat "),
        "cat <text>": Text("cat %(text)s"),
        "(change (directory|dir)|C D)": Text("cd "),
        "(change (directory|dir)|C D) <text>": Text("cd %(text)s"),
        "(copy|C P)": Text("cp "),
        "(copy|C P) recursive": Text("cp -r "),
        "diff": Text("diff "),
        "directory up [one]": Text("cd ..\n"),
        "directory up two": Text("cd ../..\n"),
        "directory up three": Text("cd ../../..\n"),
        "directory up four": Text("cd ../../../..\n"),
        "directory up five": Text("cd ../../../../..\n"),
        "directory up six": Text("cd ../../../../../..\n"),
        "directory up seven": Text("cd ../../../../../../..\n"),
        "directory up eight": Text("cd ../../../../../../../..\n"),
        "directory up nine": Text("cd ../../../../../../../../..\n"),
        "directory up ten": Text("cd ../../../../../../../../../..\n"),
        "grep": Text("grep "),
        "grep recursive": Text("grep -rn \"\" *") + Key("left:3"),
        "list files": Text("ls -la\n"),
        "list files time sort": Text("ls -lat\n"),
        "make (directory|dir)": Text("mkdir "),
        "make (directory|dir) <text>": Text("mkdir %(text)s"),
        "move": Text("mv "),
        "move <text>": Text("mv %(text)s"),
        "(remove|remove file|R M)": Text("rm "),
        "(remove|remove file|R M) <text>": Text("rm %(text)s"),
        "remove (directory|dir)": Text("rm -rf "),
        "remove (directory|dir) <text>": Text("rm -rf %(text)s"),
        "sudo": Text("sudo "),
        "touch": Text("touch "),
        "touch <text>": Text("touch %(text)s"),
        
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
    extras = [sequence, IntegerRef("n", 1, 100)]
    defaults = {"n": 1}

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()


grammar = Grammar("Bash commands")
grammar.add_rule(RepeatRule())
grammar.load()


def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
