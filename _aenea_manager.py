"""A command module for Dragonfly, for dynamically enabling/disabling
Aenea integration.

-----------------------------------------------------------------------------
Licensed under LGPL3

"""
from dragonfly import Function, Grammar, MappingRule

import lib.config
config = lib.config.get_config()

import lib.sound as sound

def enable_aenea():
    if config.get("aenea.enabled", False) == False:
        config["aenea.enabled"] = True

        print "\n==> Enabled aenea"
        sound.play(sound.SND_ACTIVATE)
    else:
        print "\nAenea already enabled"
        sound.play(sound.SND_MESSAGE)



def disable_aenea():
    if config.get("aenea.enabled", False) == True:
        config["aenea.enabled"] = False

        print "\n==> Disabled aenea"
        sound.play(sound.SND_DEACTIVATE)
    else:
        print "\nAeena already disabled"
        sound.play(sound.SND_MESSAGE)

def show_aenea_status():
    if config.get("aenea.enabled", False) == True:
        print "\nAenea is enabled"
    else:
        print "\nAenea is disabled"

rules = MappingRule(
    mapping = {
        "enable (aenea|linux mode)": Function(enable_aenea),
        "disable (aenea|linux mode)": Function(disable_aenea),
        "show (aenea|linux mode) status": Function(show_aenea_status),
    }
)

show_aenea_status()

context = None
grammar = Grammar("Aenea manager", context=context)
grammar.add_rule(rules)
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
