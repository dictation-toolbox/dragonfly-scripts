import dragonfly, proxy_actions, lib.config
config = lib.config.get_config()

class ProxyBase:
    """Base class for dynamic proxy actions. It wraps both Aenea's proxy action implementation as well
    as the Dragonfly default.  The proxy will route calls to one of the two wrapped action classes
    depending on whether Aenea is currently enabled."""

    def __add__(self, other):
        # __add__ is a special case.  Python won't ever call __getattr__ for __add__ and even if it did, we would
        # want to override it.  Unlike most of the calls we proxy, which are called when the rule is executed, __add__
        # is called when the rule is constructed.  Since the Aenea enabled state can change after rule construction,
        # we have to execute the call on both actions so they're in the proper state for later on.
        #
        # Finally, dragonfly.ActionBase's implementation (the one we're ultimately delegating to) returns a new
        # object with the chained actions, so we need to store that newly created action if we appear on the LHS
        # of __add__.  We return a copy so if our action ends up being added with other actions multiple times,
        # each addition is independent and idempotent.  I.e., this operation should not modify the callee.
        new_copy = self.copy()

        # We don't need to chain together proxy actions since new_copy itself will proxy both actions.  So, if we
        # see that this proxy is being added to another proxy, unroll the other one to its composite actions and chain
        # those together.  Otherwise, there's multiple branch points for the Aenea enabled check (one at each step in
        # the chain rather than at the starting link) and there's unnecessary objection copying & duplication due
        # to dragonfly.ActionBase also making copies when __add__ is called.
        if hasattr(other, "_aenea_action"):
            new_copy._aenea_action = self._aenea_action.__add__(other._aenea_action)
            new_copy._dragonfly_action = self._dragonfly_action.__add__(other._dragonfly_action)
        else:
            new_copy._aenea_action = self._aenea_action.__add__(other)
            new_copy._dragonfly_action = self._dragonfly_action.__add__(other)

        return new_copy

    def __getattr__(self, attribute):
        print "\n\nCalling %s" % attribute
        import traceback, sys

        if attribute == "__deepcopy__":
            traceback.print_stack(file=sys.stdout)

        if config.get("aenea.enabled", False) == True:
            return getattr(self.__dict__["_aenea_action"], attribute)
        else:
            return getattr(self.__dict__["_dragonfly_action"], attribute)


class Key(ProxyBase):
    def __init__(self, spec=None, static=False):
        self._spec = spec
        self._static = static

        self._aenea_action = proxy_actions.ProxyKey(spec, static)
        self._dragonfly_action = dragonfly.Key(spec, static)

    def copy(self):
        print "Copying Key"

        new_copy = Key(self._spec, self._static)
        new_copy._aenea_action = self._aenea_action.copy()
        new_copy._dragonfly_action = self._dragonfly_action.copy()

        return new_copy


class Text(ProxyBase):
    def __init__(self, spec=None, static=False, pause=0.02, autofmt=False):
        self._spec = spec
        self._static = static
        self._pause = pause
        self._autofmt = autofmt

        self._aenea_action = proxy_actions.ProxyText(spec, static)
        self._dragonfly_action = dragonfly.Text(spec, static, pause, autofmt)

    def copy(self):
        print "Copying Text"

        new_copy = Text(self._spec, self._static, self._pause, self._autofmt)
        new_copy._aenea_action = self._aenea_action.copy()
        new_copy._dragonfly_action = self._dragonfly_action.copy()

        return new_copy

# This is a gigantic hack.  dragonfly.ActionBase performs an `isinstance` check on the supplied action to make
# sure it is indeed an instance of dragonfly.ActionBase.  Our proxy action implementations do not inherit from
# dragonfly.ActionBase because we would have to override every method in the inheritance hierarchy rather than
# allowing for dynamic dispatch.  So, in order to fool isinstance, we have to override the built-in method.
# The override specifically looks for the case where our proxy actions are compared to dragonfly.ActionBase
# and allows for normal `isinstance` processing in all other situations.

import __builtin__

if not hasattr(__builtin__, "isinstance_orig"):
    def _isinstance(instance, klass):
        if klass is dragonfly.ActionBase and isinstance_orig(instance, ProxyBase):
            return True

        return isinstance_orig(instance, klass)

    __builtin__.isinstance_orig = __builtin__.isinstance
    __builtin__.isinstance = _isinstance