from dragonfly import *  # @UnusedWildImport

from lib.text import SCText


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
    "fetch": "fetch",
    "grep": "grep",
    "help": "help",
    "(init|initialize)": "init",
    "log": "log",
    "merge": "merge",
    "move": "move",
    "push": "push",
    "rebase": "rebase",
    "remote": "remote",
    "reset": "reset",
    "(remove|R M)": "rm",
    "revert": "revert",
    "show": "show",
    "status": "status",
    "tag": "tag",
}

gitopt = {
    "all": "--all",
    "base": "--base",
    "dry run": "--dry-run",
    "delete": "--delete",
    "cache": "--cache",
    "color": "--color",
    "continue": "--continue",
    "force": "--force",
    "hard": "--hard",
    "list": "--list",
    "no (check out|checkout)": "--no-checkout",
    "no color": "--no-color",
    "no tags": "--no-tags",
    "message": "--message",
    "ours": "--ours",
    "patch": "--patch",
    "porcelain": "--porcelain",
    "quiet": "--quiet",
    "remote": "--remote",
    "short": "--short",
    "skip": "--skip",
    "tags": "--tags",
    "theirs": "--theirs",
    "track": "--track",
    "verbose": "--verbose",
    "version": "--version",
}

series_rule = SeriesMappingRule(
    mapping={
        "git add": Text("git add "),
        "git archive": Text("git archive --format=tar "),
        "git add <text>": SCText("git add %(text)s"),
        "git add (all|period|dot)": Text("git add .\n"),
        "git blame": Text("git blame "),
        "git branch": Text("git branch\n"),
        "git branch track": Text("git branch -- track "),
        "git branch <text>": SCText("git branch %(text)s"),
        "git branch delete ": Text("git branch -d "),
        "git branch delete <text>": SCText("git branch -d %(text)s"),
        "git (check out|checkout)": Text("git checkout "),
        "git (check out|checkout) <text>": SCText("git checkout %(text)s"),
        "git clone": Text("git clone "),
        "git clone <text>": SCText("git clone %(text)s"),
        "git commit": Text("git commit -m \"\"") + Key("left:1"),
        "git commit all tracked": Text("git commit -a -m \"\"") + Key("left:1"),  # @IgnorePep8
        "git config": Text("git config "),
        "git config add": Text("git config --add "),
        "git config add <text>": SCText("git config --add %(text)s "),
        "git config list": Text("git config --list\n"),
        "git (diff|difference|differentiate)": Text("git diff "),
        "git (diff|difference|differentiate) <text>": SCText("git diff %(text)s"),  # @IgnorePep8
        "git fetch": Text("git fetch\n"),
        "git fetch <text>": SCText("git fetch %(text)s "),
        "git grep": Text("git grep \"\"") + Key("left:1"),
        "git help": Text("git --help\n"),
        "git help <gitcmd>": Text("git --help %(gitcmd)s\n"),
        "git (init|initialize)": Text("git init\n"),
        "git (init|initialize) bare": Text("git init --bare\n"),
        "git log": Text("git log\n"),
        "git log limit <n>": Text("git log -n %(n)d\n"),
        "git log graph": Text("git log --graph --oneline --decorate --all\n"),
        "git log graph limit <n>": Text("git log --graph --oneline --decorate --all -n %(n)d\n"),  # @IgnorePep8
        "git merge": Text("git merge "),
        "git merge <text>": SCText("git merge %(text)s"),
        "git merge (no (fast forward|F F))": Text("git merge --no-ff "),
        "git merge (no (fast forward|F F)) <text>": SCText("git merge --no-ff %(text)s"),  # @IgnorePep8
        "git (move|M V)": Text("git mv "),
        "git (move|M V) <text>": SCText("git mv %(text)s"),
        "git pull": Text("git pull\n"),
        "git pull origin <text>": SCText("git pull origin %(text)s"),
        "git push": Text("git push\n"),
        "git push all": Text("git push --all\n"),
        "git push origin ": Text("git push origin "),
        "git push origin <text>": SCText("git push origin %(text)s"),
        "git push tags": Text("git push --tags\n"),
        "git (rebase|re-base)": Text("git rebase "),
        "git (rebase|re-base) <text>": SCText("git rebase %(text)s"),
        "git remote": Text("git remote\n"),
        "git remote add": Text("git remote add "),
        "git remote add <text>": SCText("git remote add %(text)s"),
        "git remote show": Text("git remote show "),
        "git remote show <text>": SCText("git remote show %(text)s"),
        "git remote rename": Text("git remote rename "),
        "git remote rename <text>": SCText("git remote rename %(text)s"),
        "git remote (remove|R M)": Text("git remote rm "),
        "git remote (remove|R M) <text>": SCText("git remote rm %(text)s"),
        "git (remove|R M)": Text("git rm "),
        "git (remove|R M) <text>": SCText("git rm %(text)s"),
        "git reset hard": Text("git reset --hard"),
        "git revert": Text("git revert "),
        "git revert head": Text("git revert HEAD"),
        "git show": Text("git show "),
        "git (status|S T)": Text("git status\n"),
        "git (status|S T) <gitopt>": Text("git status %(gitopt)s\n"),
        "git tag": Text("git tag "),
        "git tag (annotate|annotated)": Text("git tag -a  -m \"\"") + Key("left:6"),  # @IgnorePep8
        "git tag delete": Text("git tag -d "),

        "git command <gitcmd>": Text("git %(gitcmd)s "),
        "git option <gitopt>": Text(" %(gitopt)s"),
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
