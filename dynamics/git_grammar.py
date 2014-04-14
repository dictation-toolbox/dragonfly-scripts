from dragonfly import (
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation,
    CompoundRule,
    RuleRef,
    Repetition,
    Choice
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)


from lib.text import SCText

DYN_MODULE_NAME = "git"
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
    "add": "--add",
    "all": "--all",
    "amend": "--amend",
    "base": "--base",
    "cache": "--cache",
    "cached": "--cached",
    "color": "--color",
    "continue": "--continue",
    "decorate": "--decorate",
    "delete": "--delete",
    "dry run": "--dry-run",
    "force": "--force",
    "format": "--format",
    "graph": "--graph",
    "hard": "--hard",
    "help": "--help",
    "list": "--list",
    "no (check out|checkout)": "--no-checkout",
    "no color": "--no-color",
    "no fast forward": "--no-ff",
    "no tags": "--no-tags",
    "message": "--message",
    "ours": "--ours",
    "(one line|oneline)": "--oneline",
    "patch": "--patch",
    "porcelain": "--porcelain",
    "quiet": "--quiet",
    "remote": "--remote",
    "short": "--short",
    "skip": "--skip",
    "tags": "--tags",
    "staged": "--staged",
    "theirs": "--theirs",
    "track": "--track",
    "verbose": "--verbose",
    "version": "--version",
}

series_rule = SeriesMappingRule(
    mapping={
        # Git commands.
        "git add": Text("git add "),
        "git add <text>": SCText("git add %(text)s"),
        "git add patch": Text("git add --patch "),
        "git add patch <text>": SCText("git add --patch %(text)s"),
        "git add (all|period|dot)": Text("git add .") + Key("enter"),
        "git archive": Text("git archive --format=tar "),
        "git blame": Text("git blame "),
        "git branch": Text("git branch") + Key("enter"),
        "git branch track": Text("git branch -- track "),
        "git branch <text>": SCText("git branch %(text)s"),
        "git branch delete ": Text("git branch -d "),
        "git branch delete <text>": SCText("git branch -d %(text)s"),
        "git (check out|checkout)": Text("git checkout "),
        "git (check out|checkout) <text>": SCText("git checkout %(text)s"),
        "git (check out|checkout) branch": Text("git checkout -b "),
        "git (check out|checkout) branch <text>": SCText("git checkout -b %(text)s"),  # @IgnorePep8
        "git (check out|checkout) force": Text("git checkout -f "),
        "git (check out|checkout) force <text>": SCText("git checkout -f %(text)s"),  # @IgnorePep8
        "git clone": Text("git clone "),
        "git clone <text>": SCText("git clone %(text)s"),
        "git cherry-pick": Text("git cherry-pick "),
        "git commit": Text("git commit -m ") + Key("dquote/3, dquote/3, left/3"),  # @IgnorePep8
        "git commit all tracked": Text("git commit -a -m ") + Key("dquote/3, dquote/3, left/3"),  # @IgnorePep8
        "git commit amend": Text("git commit --amend -m "),
        "git config": Text("git config "),
        "git config add": Text("git config --add "),
        "git config add <text>": SCText("git config --add %(text)s "),
        "git config list": Text("git config --list") + Key("enter"),
        "git diff": Text("git diff "),
        "git diff <text>": SCText("git diff %(text)s"),
        "git diff cached": Text("git diff --cached "),
        "git diff cached <text>": SCText("git diff --cached %(text)s"),
        "git diff staged": Text("git diff --staged "),
        "git diff staged <text>": SCText("git diff --staged %(text)s"),
        "git fetch": Text("git fetch") + Key("enter"),
        "git fetch <text>": SCText("git fetch %(text)s "),
        "git fetch prune": Text("git fetch -p"),  # Remove local refs to deleted remote branches.  # @IgnorePep8
        "git grep": Text("git grep \"\"") + Key("left:1"),
        "git help": Text("git --help") + Key("enter"),
        "git help <gitcmd>": Text("git --help %(gitcmd)s") + Key("enter"),
        "git (init|initialize)": Text("git init") + Key("enter"),
        "git (init|initialize) bare": Text("git init --bare") + Key("enter"),
        "git log": Text("git log") + Key("enter"),
        "git log limit <n>": Text("git log -n %(n)d") + Key("enter"),
        "git log graph": Text("git log --graph --oneline --decorate --all") + Key("enter"),  # @IgnorePep8
        "git log graph limit <n>": Text("git log --graph --oneline --decorate --all -n %(n)d") + Key("enter"),  # @IgnorePep8
        "git merge": Text("git merge "),
        "git merge <text>": SCText("git merge %(text)s"),
        "git merge (no (fast forward|F F))": Text("git merge --no-ff "),
        "git merge (no (fast forward|F F)) <text>": SCText("git merge --no-ff %(text)s"),  # @IgnorePep8
        "git (move|M V)": Text("git mv "),
        "git (move|M V) <text>": SCText("git mv %(text)s"),
        "git pull": Text("git pull "),
        "git pull origin <text>": SCText("git pull origin %(text)s"),
        "git push": Text("git push"),
        "git push all": Text("git push --all") + Key("enter"),
        "git push origin ": Text("git push origin "),
        "git push origin <text>": SCText("git push origin %(text)s"),
        "git push origin <gitopt>": SCText("git push origin %(gitopt)s"),
        "git push tags": Text("git push --tags") + Key("enter"),
        "git (rebase|re-base)": Text("git rebase "),
        "git (rebase|re-base) <text>": SCText("git rebase %(text)s"),
        "git remote": Text("git remote") + Key("enter"),
        "git remote <gitopt>": Text("git remote %(gitopt)s"),
        "git remote add": Text("git remote add "),
        "git remote add <text>": SCText("git remote add %(text)s"),
        "git remote show": Text("git remote show "),
        "git remote show <text>": SCText("git remote show %(text)s"),
        "git remote rename": Text("git remote rename "),
        "git remote prune ": Text("git remote prune "),
        "git remote prune <text>": SCText("git remote prune %(text)s"),
        "git remote rename <text>": SCText("git remote rename %(text)s"),
        "git remote (remove|R M)": Text("git remote rm "),
        "git remote (remove|R M) <text>": SCText("git remote rm %(text)s"),
        "git (remove|R M)": Text("git rm "),
        "git (remove|R M) <text>": SCText("git rm %(text)s"),
        "git reset hard": Text("git reset --hard"),
        "git revert": Text("git revert "),
        "git revert head": Text("git revert HEAD"),
        "git show": Text("git show "),
        "git stash": Text("git stash") + Key("enter"),
        "git stash pop": Text("git stash pop") + Key("enter"),
        "git (status|S T)": Text("git status") + Key("enter"),
        "git (status|S T) <gitopt>": Text("git status %(gitopt)s") + Key("enter"),  # @IgnorePep8
        "git tag": Text("git tag "),
        "git tag (annotate|annotated)": Text("git tag -a  -m ") + Key("dquote/3, dquote/3, left/3:6"),  # @IgnorePep8
        "git tag delete": Text("git tag -d "),
        # Special access to commands and options.
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

grammar = Grammar("Git commands", context=GlobalDynamicContext())
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
