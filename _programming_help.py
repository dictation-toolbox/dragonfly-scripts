"""
Notice: These helping macros are mainly focused on the programming languages
        that I use.
        (That is Python, JavaScript, HTML, CSS and unfortunately VBScript)

"""
import re

from dragonfly import *  # @UnusedWildImport


def camel_case_text(text):
    newText = _camelify(text.words)
    Text(newText).execute()


def camel_case_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        endSpace = cutText.endswith(' ')
        text = _cleanup_text(cutText)
        newText = _camelify(text.split(' '))
        if endSpace:
            newText = newText + ' '
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def _camelify(words):
    newText = ''
    for word in words:
        if newText == '':
            newText = word[:1].lower() + word[1:]
        else:
            newText = '%s%s' % (newText, word.capitalize())
    return newText


def pascal_case_text(text):
    newText = str(text).title()
    Text(newText).execute()


def pascal_case_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        endSpace = cutText.endswith(' ')
        text = _cleanup_text(cutText)
        newText = text.title().replace(' ', '')
        if endSpace:
            newText = newText + ' '
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def snake_case_text(text):
    newText = '_'.join(text.words)
    Text(newText).execute()


def snake_case_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        endSpace = cutText.endswith(' ')
        text = _cleanup_text(cutText.lower())
        newText = '_'.join(text.split(' '))
        if endSpace:
            newText = newText + ' '
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def squash_text(text):
    newText = ''.join(text.words)
    Text(newText).execute()


def squash_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        endSpace = cutText.endswith(' ')
        text = _cleanup_text(cutText)
        newText = ''.join(text.split(' '))
        if endSpace:
            newText = newText + ' '
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def expand_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        endSpace = cutText.endswith(' ')
        reg = re.compile(r'[:,][a-zA-Z0-9_\"\']')
        hit = reg.search(cutText)
        count = 0
        while hit and count < 10:
            cutText = cutText[:hit.start() + 1] + ' ' + cutText[hit.end() - 1:]
            hit = reg.search(cutText)
            count += 1
        reg = re.compile(
            r'([a-zA-Z0-9_\"\'][=\+\-\*/]|[=\+\-\*/][a-zA-Z0-9_\"\'])')
        hit = reg.search(cutText)
        count = 0
        while hit and count < 10:
            cutText = cutText[:hit.start() + 1] + ' ' + cutText[hit.end() - 1:]
            hit = reg.search(cutText)
            count += 1
        newText = cutText
        if endSpace:
            newText = newText + ' '
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def uppercase_text(text):
    newText = ''.join(text.words)
    Text(newText.upper()).execute()


def uppercase_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        newText = cutText.upper()
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def lowercase_text(text):
    newText = ''.join(text.words)
    Text(newText.lower()).execute()


def lowercase_count(n):
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        newText = cutText.lower()
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _restore_clipboard(saveText)


def _cleanup_text(text):
    text = text.strip()
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace("'", ' ')
    text = re.sub('[ \t\r\n]+', ' ', text)  # Any whitespaces to one space.
    return text


def _get_clipboard_text():
    clipboard = Clipboard()
    return clipboard.get_system_text()


def _select_and_cut_text(wordCount):
    clipboard = Clipboard()
    clipboard.set_system_text('')
    try:  # Try selecting n number of words.
        Key('ctrl:down, shift:down').execute()
        Key('left:%s' % wordCount).execute()
        Key('shift:up').execute()
    finally:
        # It is important to make sure that the buttons are released.
        # Otherwise you get stuck in an unpleasant situation.
        Key('shift:up, ctrl:up').execute()
    Pause("10").execute()
    Key('c-x').execute()  # Cut out the selected words.
    Pause("20").execute()
    return clipboard.get_system_text()


def _restore_clipboard(text):
    clipboard = Clipboard()
    clipboard.set_text(text)  # Restore previous clipboard text.
    clipboard.copy_to_system()


charMap = {
    "(bar|vertical bar)": "|",
    "(dash|minus|hyphen)": "-",
    "(dot|period)": ".",
    "comma": ",",
    "backslash": "\\",
    "underscore": "_",
    "(star|asterisk)": "*",
    "colon": ":",
    "(semicolon|semi-colon)": ";",
    "at": "@",
    "[double] quote": '"',
    "single quote": "'",
    "hash": "#",
    "dollar": "$",
    "percent": "%",
    "and": "&",
    "slash": "/",
    "equal": "=",
    "plus": "+",
    "space": " "
}


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

series_rule = SeriesMappingRule(
    mapping={
        # Shorthand multiple characters.
        "double <char>": Text("%(char)s%(char)s"),
        "triple <char>": Text("%(char)s%(char)s%(char)s"),
        "double escape": Key("escape, escape"),  # Exiting menus.
        # Code formatting.
        "camel case <text>": Function(camel_case_text),
        "camel case <n> [words]": Function(camel_case_count),
        "pascal case <text>": Function(pascal_case_text),
        "pascal case <n> [words]": Function(pascal_case_count),
        "snake case <text>": Function(snake_case_text),
        "snake case <n> [words]": Function(snake_case_count),
        "squash <text>": Function(squash_text),
        "squash <n> [words]": Function(squash_count),
        "expand <n> [words]": Function(expand_count),
        "uppercase <text>": Function(uppercase_text),
        "uppercase <n> [words]": Function(uppercase_count),
        "lowercase <text>": Function(lowercase_text),
        "lowercase <n> [words]": Function(lowercase_count),
        # Text corrections.
        "(add|fix) missing space": Key("c-left, space, c-right"),
        "(delete|remove) (double|extra) (space|whitespace)": Key("c-left, backspace, c-right"),  # @IgnorePep8
        "(delete|remove) (double|extra) (type|char|character)": Key("c-left, del, c-right"),  # @IgnorePep8
        # Html specific.
        "open html comment": Text("<!-- "),
        "close html comment": Text(" -->"),
        # JavaScript specific
#         "open JavaScript comment": Text("/* "),
#         "close JavaScript comment": Text(" */"),
#         "JavaScript comment": Text("// "),
#         "variable (declare|declaration)": Text("var "),
#         "JavaScript and": Text(" && "),
#         "JavaScript or": Text(" || "),
#         "JavaScript equals": Text(" === "),
#         "jQuery variable": Text("$()") + Key("left:1"),
        # Python specific / generic programming languages.
#         "python comment": Text("# "),
#         "python separator": Text("# --------------------------------------------------"),  # @IgnorePep8
#         "python doc string": Text('"""Doc string."""') + Key("left:14, s-right:11"),  # @IgnorePep8
#         "python (def|define|definition)": Text("def "),
#         "variable assign": Text(" = "),
#         "variable (plus|add)": Text(" + "),
#         "variable (plus|add) equals": Text(" += "),
#         "variable (minus|subtract)": Text(" - "),
#         "variable (minus|subtract) equals": Text(" -= "),
#         "variable (equals|compare)": Text(" == "),
#         "variable not equals": Text(" != "),
#         "variable less than": Text(" < "),
#         "variable less equals": Text(" <= "),
#         "variable greater than": Text(" > "),
#         "variable greater equals": Text(" >= "),
#         "modulo": Key("space") + Key("percent") + Key("space"),
#         "raise exception": Text("raise Exception("),
        # VBScript specific.
        "variable (dimension|dim)": Text("dim "),
        "foobar": Text("foobar"),
        "foo": Text("foo"),
        "bar": Text("bar"),
        "baz": Text("baz"),
        "qux": Text("qux"),
        # Lorem ipsum.
        "Lorem ipsum [short]": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit."),  # @IgnorePep8
        "Lorem ipsum medium": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."),  # @IgnorePep8
        "Lorem ipsum long": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),  # @IgnorePep8
        "Lorem ipsum long fast": Text("Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),  # @IgnorePep8
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("char", charMap),
    ],
    defaults={
        "n": 1
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Programming help", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
