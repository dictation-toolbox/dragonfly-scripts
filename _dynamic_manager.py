"""A command module for Dragonfly, for dynamically enabling/disabling
different grammars.

If a grammar is enabled, that is conflicting with a previously enabled grammar,
the previously enabled grammar will be disabled.

-----------------------------------------------------------------------------
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
# import os
import sys
import pkgutil

from dragonfly import CompoundRule, MappingRule, RuleRef, Repetition, \
    Function, IntegerRef, Dictation, Choice, Grammar

import lib.sound as sound
import modules

moduleMapping = {}


def import_dynamic_modules():
    path = modules.__path__
    prefix = modules.__name__ + "."
    print("Loading dynamic grammar modules:")
    for importer, package_name, _ in pkgutil.iter_modules(path, prefix):
        if package_name not in sys.modules:
            module = importer.find_module(package_name).load_module(
                package_name)
            moduleMapping[module.DYN_MODULE_NAME] = module
            print("    %s" % package_name)

import_dynamic_modules()
print(moduleMapping)


def notify_module_enabled(moduleName, useSound=True):
    """Notifies the user that a dynamic module has been enabled."""
    print("--> Module enabled: %s" % moduleName)
    if useSound:
        sound.play(sound.SND_ACTIVATE)


def notify_module_disabled(moduleName, useSound=True):
    """Notifies the user that a dynamic module has been disabled."""
    print("<-- Module disabled: %s" % moduleName)
    if useSound:
        sound.play(sound.SND_DEACTIVATE)


def notify_module_action_aborted(message, useSound=True):
    """Notifies the user, with a custom message, that the action was not
    completed.

    """
    print(message)
    if useSound:
        sound.play(sound.SND_MESSAGE)


def notify(message="", useSound=True):
    """Notifies the user, with a custom message, that the action was not
    completed.

    """
    if message:
        print(message)
    if useSound:
        sound.play(sound.SND_DING)


def enable_module(module):
    """Enables the specified module. Disables conflicting modules."""
    disable_incompatible_modules(module)
    status = module.dynamic_enable()
    moduleName = module.__name__
    if status:
        notify_module_enabled(moduleName)
    else:
        notify_module_action_aborted("Module %s already enabled." % moduleName)


def disable_module(module):
    """Disabled the specified module."""
    status = module.dynamic_disable()
    moduleName = module.__name__
    if status:
        notify_module_disabled(moduleName)
    else:
        notify_module_action_aborted("Module %s was not enabled." % moduleName)


def disable_incompatible_modules(enableModule):
    """Iterates through the list of incompatible modules and disables them."""
    for moduleName in enableModule.INCOMPATIBLE_MODULES:
        module = moduleMapping.get(moduleName)
        if not module:
            print("Error: module %s not found." % moduleName)
        status = module.dynamic_disable()
        if status:
            notify_module_disabled(moduleName, useSound=False)


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
        "(enable|load) <module> grammar": Function(enable_module),
        "(disable|unload) <module> grammar": Function(disable_module),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
        Choice("module", moduleMapping),
    ],
    defaults={
        "n": 1
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar = Grammar("Dynamic manager", context=global_context)
grammar.add_rule(series_rule)
grammar.load()


notify()  # Notify that Dragonfly is loaded (it more or less is...).


def unload():
    """Unload function which will be called at unload time."""
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
