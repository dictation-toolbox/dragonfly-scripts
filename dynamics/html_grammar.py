from dragonfly import (
    Choice,
    MappingRule,
    IntegerRef,
    Grammar,
    Dictation,
    Function
)

from lib.dynamic_aenea import (
    GlobalDynamicContext,
    Key,
    Text,
)

from lib.text import SCText

DYN_MODULE_TYPE = "programming_language"
DYN_MODULE_NAME = "html"
INCOMPATIBLE_MODULES = [
    'python',
    'ruby',
    'java',
    'javascript',
    'css'
]


htmlElements = {
    "(A|anchor)": "a",
    "(abbr|abbreviate|abbreviation)": "abbr",
    "address": "address",
    "area": "area",
    "article": "article",
    "aside": "aside",
    "audio": "audio",
    "(B|bold|boldface)": "b",
    "base": "base",
    "(bdi|B D I|bi-directional isolation)": "bdi",
    "(bdo|B D O|bi-directional override)": "bdo",
    "(blockquote|block quote)": "blockquote",
    "body": "body",
    "(B R|[line] break|newline|new line)": "br",
    "button": "button",
    "canvas": "canvas",
    "caption": "caption",
    "(cite|citation)": "cite",
    "code": "code",
    "(col|C O L|[table] column)": "col",
    "(colgroup|C O L group|[table] column group)": "colgroup",
    "content": "content",
    "data": "data",
    "(datalist|data list)": "datalist",
    "(dd|D D|description)": "dd",
    "decorator": "decorator",
    "(del|D E L|deleted text)": "del",
    "details": "details",
    "(D F N|definition)": "dfn",
    "(div|D I V|[document] division)": "div",
    "(D L|description list)": "dl",
    "(D T|definition term)": "dt",
    "element": "element",
    "(em|E M|emphasis)": "em",
    "embed": "embed",
    "fieldset": "fieldset",
    "(figcaption|fig caption|figure caption)": "figcaption",
    "figure": "figure",
    "footer": "footer",
    "form": "form",
    "(H 1|heading 1)": "h1",
    "(H 2|heading 2)": "h2",
    "(H 3|heading 3)": "h3",
    "(H 4|heading 4)": "h4",
    "(H 5|heading 5)": "h5",
    "(H 6|heading 6)": "h6",
    "head": "head",
    "header": "header",
    "(H R|horizontal rule)": "hr",
    "html": "html",
    "(I|italic)": "i",
    "(I|inline) frame": "iframe",
    "(I M G|image)": "img",
    "input": "input",
    "(I N S|inserted [text])": "ins",
    "(K B D|keyboard [input])": "kbd",
    "(keygen|key gen|key generation)": "keygen",
    "label": "label",
    "legend": "legend",
    "(li|L I|list [item])": "li",
    "link": "link",
    "main": "main",
    "map": "map",
    "mark": "mark",
    "menu": "menu",
    "(menuitem|menu item)": "menuitem",
    "(meta|meta data)": "meta",
    "meter": "meter",
    "(nav|N A V|navigation)": "nav",
    "(noscript|no script)": "noscript",
    "object": "object",
    "(O L|ordered list)": "ol",
    "(optgroup|opt group|(option|options) group)": "optgroup",
    "option": "option",
    "output": "output",
    "(P|paragraph)": "p",
    "(param|parameter)": "param",
    "(pre|P R E|pre-formatted [text])": "pre",
    "progress": "progress",
    "(Q|quote)": "q",
    "R P": "rp",
    "R T": "rt",
    "ruby": "ruby",
    "(S|strike through|strikethrough)": "s",
    "(samp|sample)": "samp",
    "script": "script",
    "section": "section",
    "select": "select",
    "shadow": "shadow",
    "small": "small",
    "source": "source",
    "span": "span",
    "strong": "strong",
    "style": "style",
    "(sub|S U B|sub-script)": "sub",
    "summary": "summary",
    "(sup|S U P|super [script])": "sup",
    "table": "table",
    "(T|table) body": "tbody",
    "(T D|table cell|table data)": "td",
    "template": "template",
    "(textarea|text area)": "textarea",
    "(T|table) foot": "tfoot",
    "(T H|table header) ": "th",
    "(T|table) head": "thead",
    "time": "time",
    "title": "title",
    "(T R|table row)": "tr",
    "track": "track",
    "(U|uderline)": "u",
    "(U L|an ordered list)": "ul",
    "(var|V A R|variable)": "var",
    "video": "video",
    "(W B R|word break [opportunity])": "wbr",
}

voidElements = ['area', 'base', 'br', 'col', 'command', 'embed', 'hr', 'img',
    'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr'
]

htmlAttributes = {
    "accept": "accept",
    "accept-charset": "accept-charset",
    "accesskey": "accesskey",
    "action": "action",
    "align": "align",
    "(alt|A L T|alternative)": "alt",
    "(async|asynchronous)": "async",
    "autocomplete": "autocomplete",
    "autofocus": "autofocus",
    "autoplay": "autoplay",
    "buffered": "buffered",
    "challenge": "challenge",
    "charset": "charset",
    "checked": "checked",
    "cite": "cite",
    "class": "class",
    "code": "code",
    "codebase": "codebase",
    "(cols|columns)": "cols",
    "(colspan|column span)": "colspan",
    "content": "content",
    "contenteditable": "contenteditable",
    "contextmenu": "contextmenu",
    "controls": "controls",
    "coords": "coords",
    "data": "data",
    "datetime": "datetime",
    "default": "default",
    "defer": "defer",
    "(dir|direction)": "dir",
    "dirname": "dirname",
    "disabled": "disabled",
    "download": "download",
    "draggable": "draggable",
    "dropzone": "dropzone",
    "(enctype|encoding type)": "enctype",
    "for": "for",
    "form": "form",
    "headers": "headers",
    "height": "height",
    "hidden": "hidden",
    "high": "high",
    "(href|H ref)": "href",
    "(hreflang|H ref lang)": "hreflang",
    "http-equiv": "http-equiv",
    "icon": "icon",
    "(id|I D)": "id",
    "ismap": "ismap",
    "itemprop": "itemprop",
    "keytype": "keytype",
    "kind": "kind",
    "label": "label",
    "lang": "lang",
    "language": "language",
    "list": "list",
    "loop": "loop",
    "low": "low",
    "manifest": "manifest",
    "max": "max",
    "maxlength": "maxlength",
    "media": "media",
    "method": "method",
    "min": "min",
    "multiple": "multiple",
    "name": "name",
    "(novalidate|no validate)": "novalidate",
    "open": "open",
    "optimum": "optimum",
    "pattern": "pattern",
    "ping": "ping",
    "placeholder": "placeholder",
    "poster": "poster",
    "preload": "preload",
    "pubdate": "pubdate",
    "radiogroup": "radiogroup",
    "readonly": "readonly",
    "(rel|R E L|relationship)": "rel",
    "required": "required",
    "reversed": "reversed",
    "rows": "rows",
    "rowspan": "rowspan",
    "sandbox": "sandbox",
    "spellcheck": "spellcheck",
    "scope": "scope",
    "scoped": "scoped",
    "seamless": "seamless",
    "selected": "selected",
    "shape": "shape",
    "size": "size",
    "sizes": "sizes",
    "span": "span",
    "(src|S R C|source)": "src",
    "(S R C |source) doc": "srcdoc",
    "(S R C |source) lang": "srclang",
    "start": "start",
    "step": "step",
    "style": "style",
    "summary": "summary",
    "tabindex": "tabindex",
    "target": "target",
    "title": "title",
    "type": "type",
    "usemap": "usemap",
    "value": "value",
    "width": "width",
    "wrap": "wrap",
}


def start_tag(element):
    if element in voidElements:
        Text("<%s />" % str(element)).execute()
    else:
        Text("<%s>" % str(element)).execute()


def tags(element):
    elementString = str(element)
    if element in voidElements:
        Text("<%s />" % str(element)).execute()
    else:
        Text("<%s></%s>" % (elementString, elementString)).execute()
        Key("left:%s" % (len(elementString) + 3)).execute()


def end_tag(element):
    Text("</%s>" % str(element)).execute()


def attribute_with_content(attribute, text):
    Text(' %(attribute)s=""').execute()
    Key("left").execute()
    SCText(str(text)).execute()


rules = MappingRule(
    mapping={
        # Commands and keywords.
        "[start] tag": Text("<>") + Key("left"),
        "[start] tag <element>": Function(start_tag),
        "tags <element>": Function(tags),
        "end tag": Text("</>") + Key("left"),
        "end tag <element>": Function(end_tag),
        "attribute <attribute>": Text(' %(attribute)s=""') + Key("left"),
        "attribute <attribute> [equals] <text>": Function(attribute_with_content),  # @IgnorePep8
        # Comments.
        "comment": Text("<!--  -->") + Key("left:4"),
        "comment <text>": SCText("<!-- %(text)s -->") + Key("left:4"),
        "(open|left) comment": Text("<!-- "),
        "(open|left) comment <text>": SCText("<!-- %(text)s"),
        "(close|right) comment": Text(" -->"),
        # Doctypes.
        "doctype 5": Text("<!DOCTYPE html>"),
        "doctype 4 [transitional]": Text('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">'),  # @IgnorePep8
        "doctype 4 strict": Text('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'),  # @IgnorePep8
        "doctype X [transitional]": Text('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'),  # @IgnorePep8
        "doctype X strict": Text('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'),  # @IgnorePep8
        # if conditions.
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("element", htmlElements),
        Choice("attribute", htmlAttributes),
    ],
    defaults={
        "n": 1
    }
)


grammar = Grammar("Html grammar", context=GlobalDynamicContext())
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
