import re

from dragonfly import Key, Text, Clipboard, Pause
from lib.text import SCText


def camel_case_text(text):
    """Formats dictated text to camel case.

    Example:
    "'camel case my new variable'" => "myNewVariable".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        if newText == '':
            newText = word[:1].lower() + word[1:]
        else:
            newText = '%s%s' % (newText, word.capitalize())
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
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
    "'pascal case my new variable'" => "MyNewVariable".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        newText = '%s%s' % (newText, word.capitalize())
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def snake_case_text(text):
    """Formats dictated text to snake case.

    Example:
    "'snake case my new variable'" => "my_new_variable".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        if newText != "" and newText[-1:].isalnum() and word[-1:].isalnum():
            word = "_" + word  # Adds underscores between normal words.
        newText += word.lower()
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def squash_text(text):
    """Formats dictated text with whitespace removed.

    Example:
    "'squash my new variable'" => "mynewvariable".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        newText = '%s%s' % (newText, word)
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
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
        reg = re.compile(r'[:,%][a-zA-Z0-9_\"\']')
        hit = reg.search(cutText)
        count = 0
        while hit and count < 10:
            cutText = cutText[:hit.start() + 1] + ' ' + \
                cutText[hit.end() - 1:]
            hit = reg.search(cutText)
            count += 1
        reg = re.compile(
            r'([a-zA-Z0-9_\"\'\)][=\+\-\*/\%]|[=\+\-\*/\%][a-zA-Z0-9_\"\'\(])')
        hit = reg.search(cutText)
        count = 0
        while hit and count < 10:
            cutText = cutText[:hit.start() + 1] + ' ' + \
                cutText[hit.end() - 1:]
            hit = reg.search(cutText)
            count += 1
        newText = cutText
        if endSpace:
            newText = newText + ' '
        newText = newText.replace("%", "%%")  # Escape any format chars.
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def uppercase_text(text):
    """Formats dictated text to upper case.

    Example:
    "'upper case my new variable'" => "MY NEW VARIABLE".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        if newText != "" and newText[-1:].isalnum() and word[-1:].isalnum():
            word = " " + word  # Adds spacing between normal words.
        newText += word.upper()
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
        Text(newText).execute()
    else:  # Failed to get text from clipboard.
        Key('c-v').execute()  # Restore cut out text.
    _set_clipboard_text(saveText)


def lowercase_text(text):
    """Formats dictated text to lower case.

    Example:
    "'lower case John Johnson'" => "john johnson".

    """
    newText = ""
    words = str(text).split(" ")
    for word in words:
        if word.startswith("\\backslash"):
            word = "\\"  # Backslash requires special handling.
        elif word.find("\\") > -1:
            word = word[:word.find("\\")]  # Cut ev. spoken form information.
        if newText != "" and newText[-1:].isalnum() and word[-1:].isalnum():
            word = " " + word  # Adds spacing between normal words.
        newText += word.lower()
    SCText("%(text)s").execute({"text": newText})


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
        newText = newText.replace("%", "%%")  # Escape any format chars.
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
    prefixChars = ""
    suffixChars = ""
    if text.startswith("-"):
        prefixChars += "-"
    if text.startswith("_"):
        prefixChars += "_"
    if text.endswith("-"):
        suffixChars += "-"
    if text.endswith("_"):
        suffixChars += "_"
    text = text.strip()
    text = text.replace('-', ' ')
    text = text.replace('_', ' ')
    text = text.replace("'", ' ')
    text = re.sub('[ \t\r\n]+', ' ', text)  # Any whitespaces to one space.
    text = prefixChars + text + suffixChars
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
