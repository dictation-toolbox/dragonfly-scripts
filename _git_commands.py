
from dragonfly import *  # @UnusedWildImport

config = Config("Git commands")
namespace = config.load()


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


gitcmd = {
    "add": "add",
    "blame": "blame",
    "branch": "branch",
    "(check out|checkout)": "checkout",
    "commit": "commit",
    "config": "config",
    "(diff|difference|differentiate)": "diff",
    "help": "help",
    "(init|initialize)": "init",
    "log": "log",
    "merge": "merge",
    "move": "move",
    "push": "push",
    "rebase": "rebase",
    "remote": "remote",
    "(remove|R M)": "rm",
    "status": "status",
    "tag": "tag",
}

gitopt = {
    "all": "--all",
    "dry run": "--dry-run",
    "delete": "--delete",
    "color": "--color",
    "force": "--force",
    "List": "--list",
    "no (check out|checkout)": "--no-checkout",
    "no color": "--no-color",
    "no tags": "--no-tags",
    "message": "--message",
    "patch": "--patch",
    "porcelain": "--porcelain",
    "quiet": "--quiet",
    "short": "--short",
    "tags": "--tags",
    "track": "--track",
    "verbose": "--verbose",
    "version": "--version",
}

series_rule = SeriesMappingRule(
    mapping={
        "git add": Text("git add "),
        "git add <text>": Text("git add %(text)s"),
        "git add all": Text("git add .\n"),
        "git blame": Text("git blame "),
        "git branch": Text("git branch\n"),
        "git branch track": Text("git branch -- track "),
        "git branch new <text>": Text("git branch %(text)s"),
        "git branch delete <text>": Text("git branch -d %(text)s"),
        "git (check out|checkout)": Text("git checkout "),
        "git (check out|checkout) <text>": Text("git checkout %(text)s"),
        "git commit": Text("git commit -m \"\"") + Key("left:1"),
        "git commit all tracked": Text("git commit -a -m \"\"") + Key("left:1"),  # @IgnorePep8
        "git config": Text("git config "),
        "git config add": Text("git config --add "),
        "git config add <text>": Text("git config --add %(text)s "),
        "git config list": Text("git config --list\n"),
        "git (diff|difference|differentiate)": Text("git diff\n"),
        "git help": Text("git --help \n"),
        "git help <gitcmd>": Text("git --help %(gitcmd)s\n"),
        "git (init|initialize)": Text("git init\n"),
        "git (init|initialize) bare": Text("git init --bare\n"),
        "git log": Text("git log\n"),
        "git log limit <n>": Text("git log -n %(n)d\n"),
        "git log graph": Text("git log --graph --oneline --decorate --all\n"),
        "git log graph limit <n>": Text("git log --graph --oneline --decorate --all -n %(n)d\n"),  # @IgnorePep8
        "git merge": Text("git merge "),
        "git merge <text>": Text("git merge %(text)s"),
        "git (move|M V)": Text("git mv "),
        "git (move|M V) <text>": Text("git mv %(text)s"),
        "git push": Text("git push\n"),
        "git push all": Text("git push --all\n"),
        "git push origin <text>": Text("git push origin %(text)s"),
        "git push tags": Text("git push --tags\n"),
        "git (rebase|re-base)": Text("git rebase "),
        "git (rebase|re-base) <text>": Text("git rebase %(text)s"),
        "git remote add": Text("git remote add "),
        "git remote show": Text("git remote show "),
        "git remote rename": Text("git remote rename "),
        "git remote (remove|R M) <text>": Text("git remote rm %(text)s"),
        "git (remove|R M)": Text("git rm "),
        "git (remove|R M) <text>": Text("git rm %(text)s"),
        "git (status|S T)": Text("git status\n"),
        "git (status|S T) <gitopt>": Text("git status %(gitopt)s\n"),
        "git tag": Text("git tag "),

        "git command <gitcmd>": Text("git %(gitcmd)s"),
        "git option <gitopt>": Text(" %(gitopt)s"),

        "git <gitcmd>": Text("git %(gitcmd)s "),
        "git <gitcmd> <gitopt>": Text("git %(gitcmd)s %(gitopt)s "),
        "git <gitcmd> <text>": Text("git %(gitcmd)s %(text)s "),
        "git <gitcmd> <gitopt> <text>": Text("git %(gitcmd)s %(gitopt)s %(text)s"),  # @IgnorePep8
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("gitcmd", gitcmd),
        Choice("gitopt", gitopt),
    ],
    defaults={
        "n": 1
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Git commands", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
