from dragonfly import (
    Function,
    MappingRule,
    Grammar,
    Dictation
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

DYN_MODULE_TYPE = "framework"
DYN_MODULE_NAME = "rubber"
INCOMPATIBLE_MODULES = [
    'javascript',
    'html',
    'css',
    'python'
]

def template_preamble():
    Key("langle, percent").execute()
    Key("enter").execute()
    Text("  @path = \"\"", static=True).execute()
    Key("enter").execute()
    Key("backspace, backspace, percent, rangle").execute()
    Key("enter, enter").execute()

rules = MappingRule(
    mapping = {
        "new (header|template) preamble": Function(template_preamble),
        "rubber (environment|E N V)": Text("rubber_env."),
        "rubber (environment|E N V) variable": Text("RUBBER_ENV"),
        "host internal IP": Text("rubber_instances[rubber_env.host].internal_ip"),
        "define namespace <text>": Text("namespace :%(text)s do"),
    },

    extras = [
        Dictation("text"),
    ],
)

grammar = Grammar("Rubber grammar", context=GlobalDynamicContext())
grammar.add_rule(rules)
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
