from dragonfly import *  # @UnusedWildImport

from lib.custom_objects import SCText


def directory_up(n):
    repeat = ['..' for i in range(n)]  # @UnusedVariable
    txt = "cd %s\n" % ("/".join(repeat))
    Text(txt).execute()


def control_break():
    try:
        Key("ctrl:down").execute()
        Pause("10").execute()  # Pause needed for Git-bash, Console2, etc.
        Key("c").execute()
    finally:
        Pause("10").execute()  # Pause needed for Git-bash, Console2, etc.
        Key("ctrl:up").execute()


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
        # Keywords:
        "(change (directory|dir)|C D)": Text("cd "),
        "(change (directory|dir)|C D) <text>": SCText("cd %(text)s"),
        "[press] control break": Function(control_break),
        "(copy|C P)": Text("cp "),
        "(copy|C P) recursive": Text("cp -r "),
        "diff": Text("diff "),
        "directory up <n> [times]": Function(directory_up),
        "find": Text("find . -name "),
        "grep": Text("grep "),
        "grep recursive": Text("grep -rn \"\" *") + Key("left:3"),
        "kill (hard|9)": Text("kill -9 "),
        "list files": Text("ls -la\n"),
        "list files time sort": Text("ls -lat\n"),
        "make (directory|dir)": Text("mkdir "),
        "make (directory|dir) <text>": SCText("mkdir %(text)s"),
        "move": Text("mv "),
        "move <text>": SCText("mv %(text)s"),
        "(print working directory|P W D)": Text("pwd\n"),
        "(R M|remove file)": Text("rm "),
        "(R M|remove file) <text>": SCText("rm %(text)s"),
        "remove (directory|dir|folder|recursive)": Text("rm -rf "),
        "remove (directory|dir|folder|recursive) <text>": SCText("rm -rf %(text)s"),  # @IgnorePep8
        "(link|L N)": Text("ln "),
        "soft link": Text("ln -s "),
        "sudo": Text("sudo "),
        "tail": Text("tail "),
        "tail <text>": SCText("tail %(text)s"),
        "tail (F|follow)": Text("tail -f "),
        "tail (F|follow) <text>": SCText("tail -f %(text)s"),
        "touch": Text("touch "),
        "touch <text>": SCText("touch %(text)s"),
        "vim": Text("vim "),
        "vim <text>": SCText("vim %(text)s"),
        "X M L lint": Text("xmllint "),
        "X M L lint <text>": SCText("xmllint %(text)s"),
        "X M L lint format": Text("xmllint -format "),
        "X M L lint format <text>": SCText("xmllint -format %(text)s"),
        "X M L lint schema": Text("xmllint -schema "),
        "X M L lint schema <text>": SCText("xmllint -schema %(text)s"),
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
grammar = Grammar("Python grammar", context=global_context)
grammar.add_rule(special_commands_one)
grammar.load()
grammar.disable()


def dynamic_enable():
    global grammar
    if grammar.enabled:
        return False
    else:
        grammar.enable()
        return True


def dynamic_disable():
    global grammar
    if grammar.enabled:
        grammar.disable()
        return True
    else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
