from dragonfly import (
    CompoundRule,
    MappingRule,
    RuleRef,
    Repetition,
    IntegerRef,
    Grammar,
    Choice,
    Dictation
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

from lib.text import SCText

DYN_MODULE_NAME = "subversion"
INCOMPATIBLE_MODULES = []


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


svncmd = {
    "add": "add",
    "blame": "blame",
    "(check out|checkout)": "checkout",
    "commit": "commit",
    "delete": "delete",
    "(diff|difference|differentiate)": "diff",
    "help": "help",
    "log": "log",
    "list": "list",
    "move": "move",
    "status": "status",
    "update": "update",
}

svnopt = {
    "force": "--force",
    "help": "--help",
    "message": "--message",
    "non-recursive": "--non-recursive",
    "password": "--password",
    "quiet": "--quiet",
    "revision": "--revision",
    "username": "--username",
    "verbose": "--verbose",
    "version": "--version",
}

svn = "(subversion|S V N) "

series_rule = SeriesMappingRule(
    mapping={
        # Subversion commands.
        svn + "add": Text("svn add "),
        svn + "add <text>": SCText("svn add %(text)s"),
        svn + "add (all|period|dot)": Text("svn add .") + Key("enter"),
        svn + "blame": Text("svn blame "),
        svn + "(check out|checkout)": Text("svn checkout "),
        svn + "(check out|checkout) <text>": SCText("svn checkout %(text)s"),
        svn + "commit": Text("svn commit -m ") + Key("dquote/3") + Key("dquote/3, left/3"),  # @IgnorePep8
        svn + "delete": Text("svn delete "),
        svn + "delete <text>": SCText("svn delete %(text)s"),\
        svn + "(diff|difference|differentiate)": Text("svn diff "),
        svn + "(diff|difference|differentiate) <text>": SCText("svn diff %(text)s"),  # @IgnorePep8
        svn + "help": Text("svn --help") + Key("enter"),
        svn + "help <svncmd>": Text("svn --help %(svncmd)s") + Key("enter"),
        svn + "log": Text("svn log "),
        svn + "log <text>": SCText("svn log %(text)s"),
        svn + "log limit <n>": Text("svn log -l %(n)d "),
        svn + "(list [files]|L S)": Text("svn ls "),
        svn + "(move|M V)": Text("svn move "),
        svn + "(move|M V) <text>": SCText("svn move %(text)s"),
        svn + "(status|S T)": Text("svn st") + Key("enter"),
        svn + "(status|S T) <svnopt>": Text("svn status %(svnopt)s") + Key("enter"),  # @IgnorePep8
        svn + "(update|up)": Text("svn update "),
        svn + "(update|up) <text>": SCText("svn update %(text)s"),
        # Special access to commands and options.
        svn + "command <svncmd>": Text("svn %(svncmd)s "),
        svn + "option <svnopt>": Text(" %(svnopt)s"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("svncmd", svncmd),
        Choice("svnopt", svnopt),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Subversion commands", context=GlobalDynamicContext())
grammar.add_rule(series_rule)
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


def is_enabled():
    global grammar
    if grammar.enabled:
        return True
    else:
        return False


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
