"""A command module for Dragonfly, for generic editing help.

-----------------------------------------------------------------------------
This is a heavily modified version of the _multiedit-en.py script at:
http://dragonfly-modules.googlecode.com/svn/trunk/command-modules/documentation/mod-_multiedit.html  # @IgnorePep8
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""

import re

from dragonfly import Key, Text, Choice, Clipboard, Pause, Window, \
    FocusWindow, Config, Section, Item, Function, Dictation, Mimic, \
    IntegerRef, MappingRule, Alternative, RuleRef, Grammar, Repetition, \
    CompoundRule

import lib.sound as sound

release = Key("shift:up, ctrl:up")


def camel_case_text(text):
    """Formats dictated text to camel case.

    Example:
    "'camel case my new variable'" => "myNewVariable".

    """
    newText = _camelify(text.words)
    Text(newText).execute()


def camel_case_count(n):
    """Formats n words to the left of the cursor to camel case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'camel case 3'" => "myNewVariable".

    """
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
    _set_clipboard_text(saveText)


def _camelify(words):
    """Takes a list of words and returns a string formatted to camel case.

    Example:
    ["my", "new", "variable"] => "myNewVariable".

    """
    newText = ''
    for word in words:
        if newText == '':
            newText = word[:1].lower() + word[1:]
        else:
            newText = '%s%s' % (newText, word.capitalize())
    return newText


def pascal_case_text(text):
    """Formats dictated text to pascal case.

    Example:
    "'pascal case my new variable'" => "PyNewVariable".

    """
    newText = str(text).title()
    Text(newText).execute()


def pascal_case_count(n):
    """Formats n words to the left of the cursor to pascal case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'pascal case 3'" => "MyNewVariable".

    """
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
    _set_clipboard_text(saveText)


def snake_case_text(text):
    """Formats dictated text to snake case.

    Example:
    "'snake case my new variable'" => "my_new_variable".

    """
    newText = '_'.join(text.words)
    Text(newText).execute()


def snake_case_count(n):
    """Formats n words to the left of the cursor to snake case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'snake case 3'" => "my_new_variable".

    """
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
    _set_clipboard_text(saveText)


def squash_text(text):
    """Formats dictated text with whitespace removed.

    Example:
    "'squash my new variable'" => "mynewvariable".

    """
    newText = ''.join(text.words)
    Text(newText).execute()


def squash_count(n):
    """Formats n words to the left of the cursor with whitespace removed.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'squash 3'" => "mynewvariable".
    "'my<tab>new variable' *pause* 'squash 3'" => "mynewvariable".

    """
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
    _set_clipboard_text(saveText)


def expand_count(n):
    """Formats n words to the left of the cursor by adding whitespace in
    certain positions.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example, with to compact code:
    "result=(width1+width2)/2 'expand 9' " => "result = (width1 + width2) / 2"

    """
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
            r'([a-zA-Z0-9_\"\'\)][=\+\-\*/]|[=\+\-\*/][a-zA-Z0-9_\"\'\(])')
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
    _set_clipboard_text(saveText)


def uppercase_text(text):
    """Formats dictated text to upper case.

    Example:
    "'upper case my new variable'" => "MY NEW VARIABLE".

    """
    newText = str(text)
    Text(newText.upper()).execute()


def uppercase_count(n):
    """Formats n words to the left of the cursor to upper case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'my new variable' *pause* 'upper case 3'" => "MY NEW VARIABLE".

    """
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        newText = cutText.upper()
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def lowercase_text(text):
    """Formats dictated text to lower case.

    Example:
    "'lower case John Johnson'" => "john johnson".

    """
    newText = str(text)
    Text(newText.lower()).execute()


def lowercase_count(n):
    """Formats n words to the left of the cursor to lower case.
    Note that word count differs between editors and programming languages.
    The examples are all from Eclipse/Python.

    Example:
    "'John Johnson' *pause* 'lower case 2'" => "john johnson".

    """
    saveText = _get_clipboard_text()
    cutText = _select_and_cut_text(n)
    if cutText:
        newText = cutText.lower()
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def _cleanup_text(text):
    """Cleans up the text before formatting to camel, pascal or snake case.

    Removes dashes, underscores, single quotes (apostrophes) and replaces
    them with a space character. Multiple spaces, tabs or new line characters
    are collapsed to one space character.
    Returns the result as a string.

    """
    text = text.strip()
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace("'", ' ')
    text = re.sub('[ \t\r\n]+', ' ', text)  # Any whitespaces to one space.
    return text


def _get_clipboard_text():
    """Returns the text contents of the system clip board."""
    clipboard = Clipboard()
    return clipboard.get_system_text()


def _select_and_cut_text(wordCount):
    """Selects wordCount number of words to the left of the cursor and cuts
    them out of the text. Returns the text from the system clip board.

    """
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


def _set_clipboard_text(text):
    """Sets the system clip board content."""
    clipboard = Clipboard()
    clipboard.set_text(text)  # Restore previous clipboard text.
    clipboard.copy_to_system()


def cancel_dictation():
    """Used to cancel an ongoing dictation.

    This method does effectively nothing. It only notifies the user that the
    dictation was in fact canceled, with a sound and a message in the Natlink
    feedback window.
    Example:
    "'random mumbling or other noises cancel this'" => No action.
    "'random mumbling or other noises abort dictation'" => No action.

    """
    print("* Dictation canceled, by user command. *")
    sound.play(sound.SND_DING)


def reload_natlink():
    """Reloads Natlink and custom Python modules."""
    win = Window.get_foreground()
    FocusWindow(executable="natspeak",
        title="Messages from Python Macros").execute()
    Pause("10").execute()
    Key("a-f, r").execute()
    Pause("10").execute()
    win.set_foreground()


# For repeating of characters.
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


config = Config("multi edit")
config.cmd = Section("Language section")
config.cmd.map = Item(
    {
        # Navigation keys.
        "up [<n>]": Key("up:%(n)d"),
        "down [<n>]": Key("down:%(n)d"),
        "left [<n>]": Key("left:%(n)d"),
        "right [<n>]": Key("right:%(n)d"),
        "page up [<n>]": Key("pgup:%(n)d"),
        "page down [<n>]": Key("pgdown:%(n)d"),
        "up <n> (page | pages)": Key("pgup:%(n)d"),
        "down <n> (page | pages)": Key("pgdown:%(n)d"),
        "left <n> (word | words)": Key("c-left:%(n)d"),
        "right <n> (word | words)": Key("c-right:%(n)d"),
        "home": Key("home"),
        "end": Key("end"),
        "doc home": Key("c-home"),
        "doc end": Key("c-end"),
        # Functional keys.
        "space": release + Key("space"),
        "space [<n>]": release + Key("space:%(n)d"),
        "enter [<n>]": release + Key("enter:%(n)d"),
        "tab [<n>]": Key("tab:%(n)d"),
        "delete [<n>]": release + Key("del:%(n)d"),
        "delete [<n> | this] (line|lines)": release + Key("home, s-down:%(n)d, del"),  # @IgnorePep8
        "backspace [<n>]": release + Key("backspace:%(n)d"),
        "application key": release + Key("apps"),
        "win key": release + Key("win"),
        "paste": release + Key("c-v"),
        "duplicate <n>": release + Key("c-c, c-v:%(n)d"),
        "copy": release + Key("c-c"),
        "cut": release + Key("c-x"),
        "select all": release + Key("c-a"),
        "undo <n> [times]": release + Key("c-z:%(n)d"),
        "redo": release + Key("c-y"),
        "redo <n> [times]": release + Key("c-y:%(n)d"),
        "[hold] shift": Key("shift:down"),
        "release shift": Key("shift:up"),
        "[hold] control": Key("ctrl:down"),
        "release control": Key("ctrl:up"),
        "release [all]": release,
        # How do I comment this?
        "say <text>": release + Text("%(text)s"),
        "mimic <text>": release + Mimic(extra="text"),
         # Shorthand multiple characters.
        "double <char>": Text("%(char)s%(char)s"),
        "triple <char>": Text("%(char)s%(char)s%(char)s"),
        "double escape": Key("escape, escape"),  # Exiting menus.
         # Formatting.
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
        # Canceling of started sentence.
        # Useful for canceling what inconsiderate loud mouths have started.
        "<text> (cancel|abort) (dictation|sentence|this)": Function(cancel_dictation),  # @IgnorePep8
        # Reload Natlink.
        "reload Natlink": Function(reload_natlink),
    },
    namespace={
        "Key": Key,
        "Text": Text,
    }
)


class KeystrokeRule(MappingRule):
    exported = False
    mapping = config.cmd.map
    extras = [
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("char", charMap),
    ]
    defaults = {
        "n": 1,
    }


alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
single_action = Alternative(alternatives)


sequence = Repetition(single_action, min=1, max=16, name="sequence")


class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "<sequence> [[[and] repeat [that]] <n> times]"
    extras = [
        sequence,  # Sequence of actions defined above.
        IntegerRef("n", 1, 100),  # Times to repeat the sequence.
    ]
    defaults = {
        "n": 1,  # Default repeat count.
    }

    def _process_recognition(self, node, extras):  # @UnusedVariable
        sequence = extras["sequence"]  # A sequence of actions.
        count = extras["n"]  # An integer repeat count.
        for i in range(count):  # @UnusedVariable
            for action in sequence:
                action.execute()
        release.execute()


grammar = Grammar("Generic edit")  # Create this module's grammar.
grammar.add_rule(RepeatRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
