from dragonfly import Config, Section, Item, MappingRule, Grammar, Text, Key, Function, Dictation

import lib.format

config = Config("capistrano")
config.cmd = Section("helpers")
config.cmd.map = Item(
    {
        "cap deploy [with] migrations to <text>": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations"),
        "cap deploy [with] migrations to <text> with filter": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER="),
        "cap deploy [with] migrations to <text> with filter roles": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER_ROLES="),
        "cap deploy [with] migrations to <text> with assets": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations"),
        "cap deploy [with] migrations to <text> with assets with filter": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER="),
        "cap deploy [with] migrations to <text> with assets with filter roles": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy:migrations FILTER_ROLES="),

        "cap deploy to <text>": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy"),
        "cap deploy to <text> with filter": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER="),
        "cap deploy to <text> with filter roles": Text("SKIP_ASSETS=true RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER_ROLES="),
        "cap deploy to <text> with assets": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy"),
        "cap deploy to <text> with assets with filter": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER="),
        "cap deploy to <text> with assets with filter roles": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap deploy FILTER_ROLES="),

        "cap invoke to <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap invoke COMMAND=\"\"") + Key("left:1"),
        "cap invoke to <text> with filter": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap invoke COMMAND=\"\" FILTER="),
        "cap invoke to <text> with filter roles": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap invoke COMMAND=\"\" FILTER_ROLES="),

        "cap rubber reboot <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:reboot ALIAS=") + Function(lib.format.lowercase_text),
        "cap rubber bootstrap <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:bootstrap FILTER=") + Function(lib.format.lowercase_text),
        "cap rubber set up security groups <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:setup_security_groups FILTER=") + Function(lib.format.lowercase_text),
        "cap rubber set up local aliases <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:setup_local_aliases"),
        "cap rubber set up remote aliases <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:setup_remote_aliases"),
        "cap rubber set up D N S aliases <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:setup_dns_aliases"),
        "cap rubber add role to <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:roles:add ROLES= ALIAS=") + Function(lib.format.lowercase_text),
        "cap rubber create staging <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:create_staging"),
        "cap rubber destroy staging <text>": Text("RUBBER_ENV=") + Function(lib.format.lowercase_text) + Text(" cap rubber:destroy_staging"),
        "cap rubber monit start": Text("cap rubber:monit:start RUBBER_ENV="),
        "cap rubber monit stop": Text("cap rubber:monit:stop RUBBER_ENV="),
        "cap rubber (postgres|PostgreSQL) start": Text("cap rubber:postgresql:start RUBBER_ENV="),
        "cap rubber (postgres|PostgreSQL) stop": Text("cap rubber:postgresql:stop RUBBER_ENV="),
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