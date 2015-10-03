from dragonfly import (
    Function,
    MappingRule,
    Grammar,
    Dictation,
    IntegerRef
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

import lib.format
from lib.text import SCText

DYN_MODULE_TYPE = "programming_language"
DYN_MODULE_NAME = "java"
INCOMPATIBLE_MODULES = [
    'python',
    'ruby',
    'html',
    'css',
    'javascript'
]


def define_function(text):
    Text("function ").execute()
    lib.format.camel_case_text(text)
    Text("() {").execute()
    Key("left:3").execute()


rules = MappingRule(
    mapping={
        # Keywords:
        "abstract": Text("abstract "),
        "and": Text(" && "),
        "assign": Text(" = "),
        "(bool|boolean)": Text("boolean "),
        "break": Text("break"),
        "case": Text("case "),
        "case <text>": SCText("case %(text)s"),
        "catch": Text("catch () {") + Key("left:3"),
        "class": Text("class "),
        "comment": Text("// "),
        "comment <text>": SCText("// %(text)s"),
        "continue": Text("continue"),
        "close comment": Text(" */"),
        "do": Text("do {"),
        "equals": Text(" == "),
        "else": Text("else"),
        "else if": Text("else if () {") + Key("left:3"),
        "extends ": Text("extends "),
        "final": Text("final "),
        "for": Text("for () {") + Key("left:3"),
        "for <text>": SCText("for (%(text)s) {") + Key("left:3"),
        "false": Text("false"),
        "finally": Text("finally {") + Key("enter"),
        "greater than": Text(" > "),
        "greater equals": Text(" >= "),
        "if": Text("if ("),
        "if <text>": Text("if (%(text)s) {") + Key("left:3"),
        "instanceof": Text("instanceof "),
        "(int|I N T)": Text("int "),
        "(int|I N T) <text>": SCText("int %(text)s"),
        "less than": Text(" < "),
        "less equals": Text(" <= "),
        "(line end|end line)": Key("end") + Text(";") + Key("enter"),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "new": Text("new "),
        "not (equal|equals) [to]": Text(" != "),
        "null": Text("null"),
        "open comment": Text("/* "),
        "or": Text(" || "),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "private": Text("private "),
        "protected": Text("protected "),
        "public": Text("public "),
        "return": Text("return "),
        "return <text>": SCText("return %(text)s"),
        "static": Text("static "),
        "string": Text("String"),
        "switch": Text("switch () {") + Key("left:3"),
        "switch <text>": SCText("switch (%(text)s) {") + Key("left:3"),
        "this": Text("this"),
        "throw": Text("throw "),
        "true": Text("true"),
        "try": Text("try {") + Key("enter"),
        "toString": Text("toString()") + Key("left"),
        "while": Text("while () {") + Key("left:3"),
        "while <text>": SCText("while (%(text)s) {") + Key("left:3"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Java grammar", context=GlobalDynamicContext())
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
