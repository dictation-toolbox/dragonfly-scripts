
try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *  # @UnusedWildImport


def directory_up(n):
    repeat = ['..' for i in range(n)]  # @UnusedVariable
    txt = "cd %s\n" % ("/".join(repeat))
    Text(txt).execute()


config = Config("Bash commands")
config.cmd = Section("Language section")
config.cmd.map = Item(
    {
        "(change (directory|dir)|C D)": Text("cd "),
        "(change (directory|dir)|C D) <text>": Text("cd %(text)s"),
        "(copy|C P)": Text("cp "),
        "(copy|C P) recursive": Text("cp -r "),
        "diff": Text("diff "),
        "directory up <n> [times]": Function(directory_up),
        "grep": Text("grep "),
        "grep recursive": Text("grep -rn \"\" *") + Key("left:3"),
        "list files": Text("ls -la\n"),
        "list files time sort": Text("ls -lat\n"),
        "make (directory|dir)": Text("mkdir "),
        "make (directory|dir) <text>": Text("mkdir %(text)s"),
        "move": Text("mv "),
        "move <text>": Text("mv %(text)s"),
        "(print working directory|P W D)": Text("pwd\n"),
        "(remove|remove file|R M)": Text("rm "),
        "(remove|remove file|R M) <text>": Text("rm %(text)s"),
        "remove (directory|dir|folder|recursive)": Text("rm -rf "),
        "remove (directory|dir|folder|recursive) <text>": Text("rm -rf %(text)s"),  # @IgnorePep8
        "sudo": Text("sudo "),
        "touch": Text("touch "),
        "touch <text>": Text("touch %(text)s"),
    },
    namespace={
        "Key": Key,
        "Text": Text,
        "Function": Function,
})


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
