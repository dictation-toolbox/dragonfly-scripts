from dragonfly import Config, Section, Item, MappingRule, Grammar, Text, Function, Dictation

import lib.format

config = Config("capistrano")
config.cmd = Section("helpers")
config.cmd.map = Item(
    {
        "cap deploy migrations to <text>": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations"),
        "cap deploy migrations to <text> with filter": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER="),
        "cap deploy migrations to <text> with filter roles": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER_ROLES="),
        "cap deploy migrations to <text> with assets": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations"),
        "cap deploy migrations to <text> with assets with filter": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER="),
        "cap deploy migrations to <text> with assets with filter roles": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER_ROLES="),

        "cap deploy to <text>": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy"),
        "cap deploy to <text> with filter": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER="),
        "cap deploy to <text> with filter roles": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER_ROLES="),
        "cap deploy to <text> with assets": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy"),
        "cap deploy to <text> with assets with filter": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER="),
        "cap deploy to <text> with assets with filter roles": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER_ROLES="),
    }
)

class MyCommandsRule(MappingRule):
    mapping = config.cmd.map

    extras = [
        Dictation("text"),
    ]

global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Capistrano commands", context=global_context)  # Create this module's grammar.
grammar.add_rule(MyCommandsRule())  # Add the top-level rule.
grammar.load()  # Load the grammar.


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None