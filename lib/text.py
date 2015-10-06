import re

from dragonfly.actions.keyboard import Keyboard

from lib.dynamic_aenea import (
    should_send_to_aenea,
    Text,
)

import lib.format
import lib.config
config = lib.config.get_config()

specialCharacterTranslations = {
    "?\\question-mark": "?",
    ":\\colon": ":",
    ";\\semicolon": ";",
    "*\\asterisk": "*",
    "~\\tilde": "~",
    ",\\comma": ",",
    ".\\period": ".",
    ".\\dot": ".",
    "/\\slash": "/",
    "_\\underscore": "_",
    "!\\exclamation-mark": "!",
    "@\\at-sign": "@",
    "\\backslash": "\\",
    "(\\left-parenthesis": "(",
    ")\\right-parenthesis": ")",
    "[\\left-square-bracket": "[",
    "]\\right-square-bracket": "]",
    "{\\left-curly-bracket": "{",
    "}\\right-curly-bracket": "}",
    "<\\left-angle-bracket": "<",
    ">\\right-angle-bracket": ">",
    "|\\vertical-bar": "|",
    "$\\dollar-sign": "$",
    "=\\equals-sign": "=",
    "+\\plus-sign": "+",
    "-\\minus-sign": "-",
    "--\\dash": "-",
    "\x96\\dash": "-",
    "-\\hyphen": "-",
    "\"\\right-double-quote": "\"",
    "\"\\left-double-quote": "\"",
}

specialCharacterTranslationsRe = re.compile('|'.join(re.escape(key) for key in specialCharacterTranslations.keys()))

class SCText(Text):  # Special Characters Text.
    def __init__(self, spec=None, static=False, pause=0.02, autofmt=False):
        Text.__init__(self, spec, static, pause, autofmt)

        # Since we're not actually part of the Dragonfly Action hierarchy and dynamically dispatch to one of two
        # Action implementations, we can't simply subclass and rely on polymorphism to call the correct method.
        # That's because this class is a subclass of the container, not of the Action itself.  So, in order to ensure
        # our overridden method is called on the correct Action, we must add an unbound copy of the method to each
        # of the Actions.
        setattr(self._dragonfly_action, "_parse_spec", self._parse_spec)
        setattr(self._aenea_action, "_parse_spec", self._parse_spec)

    def _parse_spec(self, spec):
        """Overrides the normal Text class behavior. To handle dictation of
        special characters like / . _
        Unfortunately, I have not found a better place to solve this.

        """
        events = []
        try:
            parts = re.split("\%\([a-z_0-9]+\)s", self._spec)
            if len(parts) > 2:
                raise Exception("SCText only supports one variable, yet.")
            start = len(parts[0])
            end = len(spec) - len(parts[1])
            words = spec[start:end]
            words = lib.format.strip_dragon_info(words)
            newText = ""
            for word in words:
                if (newText != "" and newText[-1:].isalnum() and
                        word[-1:].isalnum()):
                    word = " " + word  # Adds spacing between normal words.
                newText += word
            spec = parts[0] + newText + parts[1]
            if should_send_to_aenea():
                return spec
            for character in spec:
                if character in self._specials:
                    typeable = self._specials[character]
                else:
                    typeable = Keyboard.get_typeable(character)
                events.extend(typeable.events(self._pause))
        except Exception as e:
            print self._spec, parts
            print("Error: %s" % e)
        return events
