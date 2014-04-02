import re

from dragonfly import Text  # @UnusedImport
from dragonfly.actions.keyboard import Keyboard

import lib.format
import lib.config
config = lib.config.get_config()
if config.get("aenea.enabled", False) == True:
    from proxy_nicknames import Text  # @Reimport


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
    "--\dash": "-",
    "-\hyphen": "-",
    "\"\right-double-quote": "\"",
    "\"\left-double-quote": "\"",
}


class SCText(Text):  # Special Characters Text.
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
            if config.get("aenea.enabled", False) == True:
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
