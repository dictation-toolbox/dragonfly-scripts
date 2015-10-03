import aenea, dragonfly, aenea.proxy_actions, lib.config
config = lib.config.get_config()

def should_send_to_aenea():
    """Utility function for determining whether commands should be sent to Aenea.  Commands will be sent if
    Aenea is enabled and the Aenea global context application (the one capturing text on behalf of Aenea) is
    the foreground window."""

    if config.get("aenea.enabled", False) == True:
        win = dragonfly.Window.get_foreground()

        return aenea.ProxyPlatformContext('linux').matches(win.executable, win.title, win.handle)
    else:
        return False

class DynamicContext(dragonfly.Context):
    """A context which matches commands against a configured Aenea context or a Dragonfly context depending
    upon whether Aenea is currently enabled."""
    def __init__(self, dragonfly_context=None, aenea_context=None):
        self._dragonfly_context = dragonfly_context
        self._aenea_context = aenea_context

    def matches(self, executable, title, handle):
        if should_send_to_aenea():
            if self._aenea_context:
                return self._aenea_context.matches(executable, title, handle)

            else:
                # If Aenea is enabled but no context was registered, assume the command is not to be handle by Aenea.
                return False

        else:
            if self._dragonfly_context:
                return self._dragonfly_context.matches(executable, title, handle)

            else:
                # If Aenea is disabled and no context is configured, then the command should apply to all contents,
                # per the invariant for dragonfly.grammar_base.Grammar.
                return True



class GlobalDynamicContext(DynamicContext):
    """A dynamic context implementation that allows commands to be processed in any remote application if Aenea is
    enabled and any local application if Aenea is disabled."""
    def __init__(self):
        DynamicContext.__init__(self, None, aenea.ProxyPlatformContext('linux'))


class DynamicAction:
    """Base class for dynamic proxy actions. It wraps both Aenea's proxy action implementation as well
    as the Dragonfly default.  The proxy will route calls to one of the two wrapped action classes
    depending on whether Aenea is currently enabled."""

    def __init__(self, dragonfly_action, aenea_action):
        self._aenea_action = aenea_action
        self._dragonfly_action = dragonfly_action

    def copy(self):
        return DynamicAction(self._dragonfly_action.copy(), self._aenea_action.copy())

    def __add__(self, other):
        # __add__ is a special case.  Python won't ever call __getattr__ for __add__ and even if it did, we would
        # want to override it.  Unlike most of the calls we proxy, which are called when the rule is executed, __add__
        # is called when the rule is constructed.  Since the Aenea enabled state can change after rule construction,
        # we have to execute the call on both actions so they're in the proper state for later on.


        # We don't need to chain together proxy actions since the object we return will proxy both actions.  So, if we
        # see that this proxy is being added to another proxy, unroll the other one to its composite actions and chain
        # those together.  Otherwise, there's multiple branch points for the Aenea enabled check (one at each step in
        # the chain rather than at the starting link) and there's unnecessary objection copying & duplication due
        # to dragonfly.ActionBase also making copies when __add__ is called.

        if hasattr(other, "_aenea_action"):
            new_copy_aenea_action = self._aenea_action.__add__(other._aenea_action)
            new_copy_dragonfly_action = self._dragonfly_action.__add__(other._dragonfly_action)
        else:
            new_copy_aenea_action = self._aenea_action.__add__(other)
            new_copy_dragonfly_action = self._dragonfly_action.__add__(other)

        return DynamicAction(new_copy_dragonfly_action, new_copy_aenea_action)

    def __getattr__(self, attribute):
        if should_send_to_aenea():
            return getattr(self.__dict__["_aenea_action"], attribute)
        else:
            return getattr(self.__dict__["_dragonfly_action"], attribute)


class Key(DynamicAction):
    def __init__(self, spec=None, static=False):
        DynamicAction.__init__(self, dragonfly.Key(spec, static), aenea.ProxyKey(spec, static))


class Text(DynamicAction):
    def __init__(self, spec=None, static=False, pause=0.02, autofmt=False):
        DynamicAction.__init__(self, dragonfly.Text(spec, static, pause, autofmt), aenea.ProxyText(spec, static))


# This is a gigantic hack.  dragonfly.ActionBase performs an `isinstance` check on the supplied action to make
# sure it is indeed an instance of dragonfly.ActionBase.  Our proxy action implementations do not inherit from
# dragonfly.ActionBase because we would have to override every method in the inheritance hierarchy rather than
# allowing for dynamic dispatch.  So, in order to fool isinstance, we have to override the built-in method.
# The override specifically looks for the case where our proxy actions are compared to dragonfly.ActionBase
# and allows for normal `isinstance` processing in all other situations.
import __builtin__

if not hasattr(__builtin__, "isinstance_orig"):
    isinstance_orig = __builtin__.isinstance
    __builtin__.isinstance_orig = isinstance_orig

    def _isinstance(instance, klass):
        if klass is dragonfly.ActionBase and isinstance_orig(instance,
                DynamicAction):
            return True

        return isinstance_orig(instance, klass)

    __builtin__.isinstance = _isinstance
