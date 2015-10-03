from dragonfly import (
    MappingRule,
    Function,
    Grammar,
    IntegerRef,
    Dictation,
    Choice,
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

from lib.text import SCText
import lib.format

DYN_MODULE_TYPE = "programming_languages"
DYN_MODULE_NAME = "ruby"
INCOMPATIBLE_MODULES = [
    'java',
    'javascript',
    'html',
    'css',
    'python'
]

def define_method(text):
    Text("def ").execute()
    lib.format.snake_case_text(text)
    Text("()").execute()
    Key("left").execute()

def define_class_method(text):
    Text("def self.").execute()
    lib.format.snake_case_text(text)
    Text("()").execute()
    Key("left").execute()

def define_class(text):
    Text("class ").execute()
    lib.format.pascal_case_text(text)

def call_iterator(iterator):
    Text(".").execute()
    lib.format.lowercase_text(iterator)
    Text(" { |x| }").execute()
    Key("left").execute()

iterator = {
    "all": "all?",
    "any": "any?",
    "collect": "collect",
    "each": "each",
    "each with index": "each_with_index",
    "find": "find",
    "find all": "find_all",
    "inject": "inject",
    "reject": "reject",
    "select": "select",
}

rules = MappingRule(
    mapping = {
        # Commands and keywords:
        "and": Text(" && "),
        "and (equal|equals)": Text(" &&= "),
        "(append|stream)": Text(" << "),
        "assign": Text(" = "),
        "(attr|attribute) accessor": Text("attr_accessor :"),
        "(attr|attribute) accessor <text>": Text("attr_accessor :") + Function(lib.format.snake_case_text),
        "(attr|attribute) reader": Text("attr_reader :"),
        "(attr|attribute) reader <text>": Text("attr_reader :") + Function(lib.format.snake_case_text),
        "begin": Text("begin") + Key("enter"),
        "block comment (begin|start)": Text("=begin") + Key("enter"),
        "block comment end": Text("=end") + Key("enter"),
        "block": Text("{ || }") + Key("left:3"),
        "block multi": Text("do ||") + Key("left"),
        "block (param|arg|variable|params|args|variables)": Text("||") + Key("left"),
        "comment": Text("# "),
        "class": Text("class "),
        "class <text>": Function(define_class),
        "divided by": Text(" / "),
        "(def|define|definition) [function|method]": Text("def "),
        "(def|define|definition) [function|method] <text>": Function(define_method),
        "(def|define|definition) class [function|method]": Text("def self."),
        "(def|define|definition) class [function|method] <text>": Function(define_class_method),
        "(def|define|definition) initialize": Text("def initialize()") + Key("left"),
        "do": Text("do ||") + Key("left"),
        "else": Text("else") + Key("enter"),
        "end": Text("end"),
        "exec": Text("exec "),
        "exit": Text("exit") + Key("enter"),
        "(exponent|to the power of)": Text(" ** "),
        "(el if|else if)": Text("elsif "),
        "(el if|else if) <text>": SCText("elsif %(text)s"),
        "end [block]": Text("end") + Key("enter"),
        "ensure": Text("ensure") + Key("enter"),
        "equals": Text(" == "),
        "false": Text("false"),
        "for": Text("for "),
        "for <text>": SCText("for %(text)s"),
        "greater than": Text(" > "),
        "greater [than] equals": Text(" >= "),
        "hash (arrow|operator|rocket)": Text(" => "),
        "hash key": Text(" => ") + Key("left:4"),
        "hash key string": Text("'' => ") + Key("left:5"),
        "hash key symbol": Text(": :") + Key("left:3"),
        "if": Text("if "),
        "if <text>": SCText("if %(text)s"),
        "index": Text("[]") + Key("left"),
        "index string <text>": Text("['") + Function(lib.format.snake_case_text) + Text("']"),
        "index symbol <text>": Text("[:") + Function(lib.format.snake_case_text) + Text("]"),
        "(instance variable|ivar)": Text("@"),
        "(instance variable|ivar) <text>": Text("@") + Function(lib.format.snake_case_text),
        "include [module]": Text("include "),
        "include [module] <text>": Text("include ") + Function(lib.format.pascal_case_text),
        "lambda": Text("lambda "),
        "less than": Text(" < "),
        "less [than] equals": Text(" <= "),
        "loop": Text("loop { "),
        "loop multi": Text("loop do") + Key("enter"),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "(match|matches)": Text(" =~ //") + Key("left"),
        "module": Text("module "),
        "modulo": Key("space") + Key("percent") + Key("space"),
        "next": Text("next"),
        "nil": Text("nil"),
        "not": Text(" ! "),
        "not (equal|equals)": Text(" != "),
        "not (match|matches)": Text(" !~ //") + Key("left"),
        "or": Text(" || "),
        "or (equal|equals)": Text(" ||= "),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "print": Text("p "),
        "private": Text("private") + Key("enter:2"),
        "protected": Text("protected") + Key("enter:2"),
        "question [mark]": Text("?"),
        "raise": Text("raise"),
        "raise exception": Text("raise ''") + Key("left"),
        "rescue": Text("rescue => e"),
        "require": Text("require "),
        "require <text>": SCText("require '%(text)s'"),
        "return": Text("return"),
        "return <text>": SCText("return %(text)s"),
        "self": Text("self."),
        "splat": Text("*"),
        "(string interpolation|interpolate)": Text("#{}") + Key("left:1"),
        "symbol": Text(":"),
        "symbol <text>": Text(":") + Function(lib.format.snake_case_text),
        "true": Text("true"),
        "times": Text(" * "),
        "unless": Text("unless "),
        "while": Text("while "),
        "yield": Text("yield "),

        # Some common vocabulary.
        "gem file": Text("Gemfile"),
        "gem file lock": Text("Gemfile.lock"),
        "gem spec": Text(".gemspec"),

        # Some common operations.
        "is blank": Text(".blank?"),
        "is empty": Text(".empty?"),
        "is nil": Text(".nil?"),
        "to (F|float)": Text(".to_f"),
        "to (I|int|integer)": Text(".to_i"),
        "to (S|string)": Text(".to_s"),
        "time dot now": Text("Time.now"),
        "empty hash": Text("{}"),
        "empty (list|array)": Text("[]"),
        "dot first": Text(".first"),
        "dot last": Text(".last"),
        "dot size": Text(".size"),
        "dot count": Text(".count"),

        # Iterators.
        "iterate <iterator>": Function(call_iterator),

        "log debug": Text("logger.debug {  }") + Key("left:2"),
        "log error": Text("logger.error {  }") + Key("left:2"),
        "log info": Text("logger.info {  }") + Key("left:2"),
        "log warn": Text("logger.warn {  }") + Key("left:2"),

        # Some common modules.
        "assert": Text("assert "),
        "pretty print": Text("pp "),

        "params": Text("params[:]") + Key("left"),

        "(ater|attribute) accessible": Text("attr_accessible :"),
        "(ater|attribute) accessible <text>": Text("attr_accessible :") + Function(lib.format.snake_case_text),
        "(ater|attribute) reader": Text("attr_reader :"),
        "(ater|attribute) reader <text>": Text("attr_reader :") + Function(lib.format.snake_case_text),

        "describe": Text("describe '' do") + Key("left:4"),
        "it should": Text("it 'should ' do") + Key("left:4"),
        "expect": Text("expect()") + Key("left"),
        "to equal": Text(".to eql()") + Key("left"),
        "to receive": Text(".to receive(:)") + Key("left"),

        "E R B (evaluation|interpolation)": Key("langle, percent, equal, space:3, percent, rangle, left:4"),
        "require [(library|gem)]": Text("require ") + Key("squote, squote, left/3"),
        "[bundle exec] rake D B migrate": Text("bundle exec rake db:migrate") + Key("enter"),
        "[bundle exec] rake D B migrate redo": Text("bundle exec rake db:migrate:redo") + Key("enter"),
        "[bundle exec] rake D B test prepare": Text("bundle exec rake db:test:prepare") + Key("enter"),
        "[bundle exec] rake routes": Text("bundle exec rake routes") + Key("enter"),
        "start ruby shell": Text("irb") + Key("enter"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("iterator", iterator),
    ],
    defaults={
        "n": 1
    }
)

grammar = Grammar("Ruby grammar", context=GlobalDynamicContext())
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
