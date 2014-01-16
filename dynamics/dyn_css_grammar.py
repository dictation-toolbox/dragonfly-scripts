from dragonfly import (Text, Key, Choice, MappingRule, IntegerRef, Grammar,
    Dictation)

from lib.text import SCText

DYN_MODULE_TYPE = "programming_language"
DYN_MODULE_NAME = "css"
INCOMPATIBLE_MODULES = [
    'python',
    'javascript',
    'html'
]


cssProperties = {
    "animation": "animation",
    "appearance": "appearance",
    "backface-visibility": "backface-visibility",
    "background": "background",
    "background-attachment": "background-attachment",
    "background-color": "background-color",
    "background-image": "background-image",
    "background-position": "background-position",
    "background-repeat": "background-repeat",
    "background-clip": "background-clip",
    "background-origin": "background-origin",
    "background-size": "background-size",
    "border": "border",
    "border-bottom": "border-bottom",
    "border-bottom-color": "border-bottom-color",
    "border-bottom-style": "border-bottom-style",
    "border-bottom-width": "border-bottom-width",
    "border-collapse": "border-collapse",
    "border-color": "border-color",
    "border-left": "border-left",
    "border-left-color": "border-left-color",
    "border-left-style": "border-left-style",
    "border-left-width": "border-left-width",
    "border-right": "border-right",
    "border-right-color": "border-right-color",
    "border-right-style": "border-right-style",
    "border-right-width": "border-right-width",
    "border-spacing": "border-spacing",
    "border-style": "border-style",
    "border-top": "border-top",
    "border-top-color": "border-top-color",
    "border-top-style": "border-top-style",
    "border-top-width": "border-top-width",
    "border-width": "border-width",
    "border-bottom-left-radius": "border-bottom-left-radius",
    "border-bottom-right-radius": "border-bottom-right-radius",
    "border-image": "border-image",
    "border-image-outset": "border-image-outset",
    "border-image-repeat": "border-image-repeat",
    "border-image-slice": "border-image-slice",
    "border-image-source": "border-image-source",
    "border-image-width": "border-image-width",
    "border-radius": "border-radius",
    "border-top-left-radius": "border-top-left-radius",
    "border-top-right-radius": "border-top-right-radius",
    "bottom": "bottom",
    "box": "box",
    "box-align": "box-align",
    "box-direction": "box-direction",
    "box-flex": "box-flex",
    "box-flex-group": "box-flex-group",
    "box-lines": "box-lines",
    "box-ordinal-group": "box-ordinal-group",
    "box-orient": "box-orient",
    "box-pack": "box-pack",
    "box-sizing": "box-sizing",
    "box-shadow": "box-shadow",
    "caption-side": "caption-side",
    "clear": "clear",
    "clip": "clip",
    "color": "color",
    "column": "column",
    "column-count": "column-count",
    "column-fill": "column-fill",
    "column-gap": "column-gap",
    "column-rule": "column-rule",
    "column-rule-color": "column-rule-color",
    "column-rule-style": "column-rule-style",
    "column-rule-width": "column-rule-width",
    "column-span": "column-span",
    "column-width": "column-width",
    "columns": "columns",
    "content": "content",
    "counter-increment": "counter-increment",
    "counter-reset": "counter-reset",
    "cursor": "cursor",
    "direction": "direction",
    "display": "display",
    "empty-cells": "empty-cells",
    "float": "float",
    "font": "font",
    "font": "font",
    "font-family": "font-family",
    "font-size": "font-size",
    "font-style": "font-style",
    "font-variant": "font-variant",
    "font-weight": "font-weight",
    "font-face": "@font-face",
    "font-size-adjust": "font-size-adjust",
    "font-stretch": "font-stretch",
    "grid-columns": "grid-columns",
    "grid-rows": "grid-rows",
    "hanging-punctuation": "hanging-punctuation",
    "height": "height",
    "icon": "icon",
    "keyframes": "@keyframes",
    "left": "left",
    "letter-spacing": "letter-spacing",
    "line-height": "line-height",
    "list-style": "list-style",
    "list-style": "list-style",
    "list-style-image": "list-style-image",
    "list-style-position": "list-style-position",
    "list-style-type": "list-style-type",
    "margin": "margin",
    "margin": "margin",
    "margin-bottom": "margin-bottom",
    "margin-left": "margin-left",
    "margin-right": "margin-right",
    "margin-top": "margin-top",
    "max-height": "max-height",
    "max-width": "max-width",
    "min-height": "min-height",
    "min-width": "min-width",
    "nav": "nav",
    "nav-down": "nav-down",
    "nav-index": "nav-index",
    "nav-left": "nav-left",
    "nav-right": "nav-right",
    "nav-up": "nav-up",
    "opacity": "opacity",
    "outline": "outline",
    "outline": "outline",
    "outline-color": "outline-color",
    "outline-offset": "outline-offset",
    "outline-style": "outline-style",
    "outline-width": "outline-width",
    "overflow": "overflow",
    "overflow-x": "overflow-x",
    "overflow-y": "overflow-y",
    "padding": "padding",
    "padding": "padding",
    "padding-bottom": "padding-bottom",
    "padding-left": "padding-left",
    "padding-right": "padding-right",
    "padding-top": "padding-top",
    "page-break": "page-break",
    "page-break-after": "page-break-after",
    "page-break-before": "page-break-before",
    "page-break-inside": "page-break-inside",
    "perspective": "perspective",
    "perspective-origin": "perspective-origin",
    "position": "position",
    "punctuation-trim": "punctuation-trim",
    "quotes": "quotes",
    "resize": "resize",
    "right": "right",
    "rotation": "rotation",
    "rotation-point": "rotation-point",
    "table-layout": "table-layout",
    "target": "target",
    "target": "target",
    "target-name": "target-name",
    "target-new": "target-new",
    "target-position": "target-position",
    "text": "text",
    "text-align": "text-align",
    "text-decoration": "text-decoration",
    "text-indent": "text-indent",
    "text-justify": "text-justify",
    "text-outline": "text-outline",
    "text-overflow": "text-overflow",
    "text-shadow": "text-shadow",
    "text-transform": "text-transform",
    "text-wrap": "text-wrap",
    "top": "top",
    "transform": "transform",
    "transform": "transform",
    "transform-origin": "transform-origin",
    "transform-style": "transform-style",
    "transition": "transition",
    "transition": "transition",
    "transition-property": "transition-property",
    "transition-duration": "transition-duration",
    "transition-timing-function": "transition-timing-function",
    "transition-delay": "transition-delay",
    "vertical-align": "vertical-align",
    "visibility": "visibility",
    "width": "width",
    "white-space": "white-space",
    "word-spacing": "word-spacing",
    "word-break": "word-break",
    "word-wrap": "word-wrap",
    "z-index": "z-index",
}


rules = MappingRule(
    mapping={
        # Commands and keywords.
        "class <text>": SCText(".%(text)s {"),
        "close comment": Text(" */"),
        "comment": Text("/*  */") + Key("left:3"),
        "<prop>": Text("%(prop)s: "),
#         "<prop> <text>": SCText("%(prop)s: %(text)s"),
        "open comment": Text("/* "),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("prop", cssProperties),
    ],
    defaults={
        "n": 1
    }
)

global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Css grammar", context=global_context)
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


# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
