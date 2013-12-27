from dragonfly import *  # @UnusedWildImport


def directory_up(n):
    repeat = ['..' for i in range(n)]  # @UnusedVariable
    txt = "cd %s\n" % ("/".join(repeat))
    Text(txt).execute()


def control_break():
    try:
        Key("ctrl:down").execute()
        Pause("10").execute()
        Key("c").execute()
    finally:
        Pause("10").execute()
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
        "(change (directory|dir)|C D) <text>": Text("cd %(text)s"),
        "control break": Function(control_break),
        "(copy|C P)": Text("cp "),
        "(copy|C P) recursive": Text("cp -r "),
        "diff": Text("diff "),
        "directory up <n> [times]": Function(directory_up),
        "grep": Text("grep "),
        "grep recursive": Text("grep -rn \"\" *") + Key("left:3"),
        "kill (hard|9)": Text("kill -9 "),
        "list files": Text("ls -la\n"),
        "list files time sort": Text("ls -lat\n"),
        "make (directory|dir)": Text("mkdir "),
        "make (directory|dir) <text>": Text("mkdir %(text)s"),
        "move": Text("mv "),
        "move <text>": Text("mv %(text)s"),
        "(print working directory|P W D)": Text("pwd\n"),
        "(R M|remove file)": Text("rm "),
        "(R M|remove file) <text>": Text("rm %(text)s"),
        "remove (directory|dir|folder|recursive)": Text("rm -rf "),
        "remove (directory|dir|folder|recursive) <text>": Text("rm -rf %(text)s"),  # @IgnorePep8
        "(link|L N)": Text("ln "),
        "soft link": Text("ln -s "),
        "sudo": Text("sudo "),
        "tail": Text("tail "),
        "tail <text>": Text("tail %(text)s"),
        "tail (F|follow)": Text("tail -f "),
        "tail <text> (F|follow)": Text("tail -f %(text)s"),
        "touch": Text("touch "),
        "touch <text>": Text("touch %(text)s"),
        "vim": Text("vim "),
        "vim <text>": Text("vim %(text)s"),
        "X M L lint": Text("xmllint "),
        "X M L lint <text>": Text("xmllint %(text)s"),
        "X M L lint format": Text("xmllint -format "),
        "X M L lint format <text>": Text("xmllint -format %(text)s"),
        "X M L lint schema": Text("xmllint -schema "),
        "X M L lint schema <text>": Text("xmllint -schema %(text)s"),
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
