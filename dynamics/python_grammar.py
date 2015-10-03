from dragonfly import (
    Function,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

from lib.text import SCText
import lib.format

DYN_MODULE_TYPE = "programming_language"
DYN_MODULE_NAME = "python"
INCOMPATIBLE_MODULES = [
    'java',
    'javascript',
    'ruby',
    'html',
    'css'
]


def define_function(text):
    Text("def ").execute()
    lib.format.snake_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


def define_method(text):
    Text("def ").execute()
    lib.format.snake_case_text(text)
    Text("(self, ):").execute()
    Key("left:2").execute()


def define_class(text):
    Text("class ").execute()
    lib.format.pascal_case_text(text)
    Text("():").execute()
    Key("left:2").execute()


rules = MappingRule(
    mapping={
        # Commands and keywords:
        "and": Text(" and "),
        "as": Text("as "),
        "assign": Text(" = "),
        "assert": Text("assert "),
        "break": Text("break"),
        "comment": Text("# "),
        "class": Text("class "),
        "class <text>": Function(define_class),
        "continue": Text("continue"),
        "del": Text("del "),
        "divided by": Text(" / "),
        "(dict|dictionary) key value": Text("\"\": \"\",") + Key("left:6"),
        "enumerate": Text("enumerate()") + Key("left"),
        "(def|define|definition) [function]": Text("def "),
        "(def|define|definition) [function] <text>": Function(define_function),
        "(def|define|definition) method <text>": Function(define_method),
        "(def|define|definition) init": Text("def __init__("),
        "doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),
        "else": Text("else:") + Key("enter"),
        "except": Text("except "),
        "exec": Text("exec "),
        "(el if|else if)": Text("elif "),
        "(el if|else if) <text>": SCText("elif %(text)s"),
        "equals": Text(" == "),
        "false": Text("False"),
        "finally": Text("finally:") + Key("enter"),
        "for": Text("for "),
        "for <text>": SCText("for %(text)s"),
        "from": Text("from "),
        "from <text>": SCText("from %(text)s"),
        "global ": Text("global "),
        "greater than": Text(" > "),
        "greater [than] equals": Text(" >= "),
        "if": Text("if "),
        "if <text>": SCText("if %(text)s"),
        "in": Text(" in "),
        "in <text>": SCText("in %(text)s"),
        "(int|I N T)": Text("int"),
        "(int|I N T)": Text("int()") + Key("left"),
        "init": Text("init"),
        "import": Text("import "),
        "import <text>": SCText("import %(text)s"),
        "(len|L E N)": Text("len("),
        "lambda": Text("lambda "),
        "less than": Text(" < "),
        "less [than] equals": Text(" <= "),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "not": Text(" not "),
        "not equals": Text(" != "),
        "none": Text("None"),
        "or": Text(" or "),
        "pass": Text("pass"),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "print": Text("print()") + Key("left"),
        "raise": Text("raise"),
        "raise exception": Text("raise Exception()") + Key("left"),
        "return": Text("return"),
        "return <text>": SCText("return %(text)s"),
        "self": Text("self"),
        "(str|S T R)": Text("str"),
        "(str|S T R) paren": Text("str()") + Key("left"),
        "true": Text("True"),
        "try": Text("try:") + Key("enter"),
        "times": Text(" * "),
        "with": Text("with "),
        "while": Text("while "),
        "yield": Text("yield "),
        # Some common modules.
        "datetime": Text("datetime"),
        "(io|I O)": Text("io"),
        "logging": Text("logging"),
        "(os|O S)": Text("os"),
        "(pdb|P D B)": Text("pdb"),
        "(re|R E)": Text("re"),
        "(sys|S Y S)": Text("sys"),
        "S Q lite 3": Text("sqlite3"),
        "subprocess": Text("subprocess"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Python grammar", context=GlobalDynamicContext())
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
