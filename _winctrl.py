#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for moving and controlling **windows**
=====================================================

This command-module offers commands for naming windows, bringing
named windows to the foreground, and positioning and resizing
windows.

Commands
--------

The following voice commands are available:

Command: **"name window <dictation>"**
    Assigns the given name to the current foreground window.

Command: **"focus <window name>"** or **"bring <window name> to the foreground"**
    Brings the named window to the foreground.

Command: **"focus title <window title>"**
    Brings a window with the given word(s) in the title to the foreground.

Command: **"place <window> <position> [on <monitor>]"**
    Relocates the target window to the given position.

Command: **"stretch <window> <position>"**
    Stretches the target window to the given position.

Usage examples
--------------

 - Say **"place window left"** to relocate the foreground window
   to the left side of the monitor it's on.
 - Say **"place Firefox top right on monitor 2"** to relocate
   the window which was previously named "Firefox" to the top right
   corner of the second display monitor.

"""

#import pkg_resources
#pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r76")

import time
from dragonfly import (Grammar, Alternative, RuleRef, DictListRef,
                       Dictation, Compound, Integer, Rule, CompoundRule,
                       DictList, Window, Rectangle, monitors,
                       Config, Section, Item, FocusWindow, ActionError)


#---------------------------------------------------------------------------
# Set up this module's configuration.

config = Config("Window control")
config.lang                = Section("Language section")
config.lang.name_win       = Item("name (window | win) <name>",
                                  doc="Command to give the foreground window a name; must contain the <name> extra.")
config.lang.focus_win      = Item("focus <win_selector> | bring <win_selector> to [the] (top | foreground)",
                                  doc="Command to bring a named window to the foreground.")
config.lang.focus_title    = Item("focus title <text>",
                                  doc="Command to bring a window with the given title to the foreground.")
config.lang.translate_win  = Item("place <win_selector> <position> [on <mon_selector>]",
                                  doc="Command to translate a window.")
config.lang.resize_win     = Item("place <win_selector> [from] <position> [to] <position> [on <mon_selector>]",
                                  doc="Command to move and resize a window.")
config.lang.stretch_win    = Item("stretch <win_selector> [to] <position>",
                                  doc="Command to stretch a window.")
config.lang.win_selector   = Item("window | win | [window] <win_names>",
                                  doc="Partial command for specifying a window; must contain the <win_names> extra.")
config.lang.mon_selector   = Item("(this | current) monitor | [monitor] <mon_names>",
                                  doc="Partial command for specifying a monitor; must contain the <mon_names> extra.")
config.lang.left           = Item("left", doc="Word for left side of monitor.")
config.lang.right          = Item("right", doc="Word for right side of monitor.")
config.lang.top            = Item("top", doc="Word for top side of monitor.")
config.lang.bottom         = Item("bottom", doc="Word for bottom side of monitor.")
config.settings            = Section("Settings section")
config.settings.grid       = Item(10, doc="The number of grid divisions a monitor is divided up into when placing windows.")
config.settings.defaults   = Item({"fire": ("firefox", None)}, doc="Default window names.  Maps spoken-forms to (executable, title) pairs.")
#config.generate_config_file()
config.load()


#===========================================================================
# Create this module's main grammar object.

grammar = Grammar("window control")


#---------------------------------------------------------------------------
# Dictionary list of window and monitor names.

win_names     = DictList("win_names")
win_names_ref = DictListRef("win_names", win_names)
mon_names     = DictList("mon_names")
mon_names_ref = DictListRef("mon_names", mon_names)

# Populate monitor names.
for i, m in enumerate(monitors):
    mon_names[str(i+1)] = m


#---------------------------------------------------------------------------
# Default window names handling.

default_names = config.settings.defaults

# Pre-populate the win_names mapping with the given default names.
for key in default_names.keys():
    win_names[key] = key

# Helper function to search for a default-name window.
def get_default_window(name):
    executable, title = default_names[name]
    if executable: executable = executable.lower()
    if title: title = title.lower()
    windows = Window.get_all_windows()
    for window in windows:
        if not window.is_visible:
            continue
        elif executable and window.executable.lower().find(executable) == -1:
            continue
        elif title and window.title.lower().find(title) == -1:
            continue
        window.name = name
        win_names[name] = window
        return window
    return None


#---------------------------------------------------------------------------
# Internal window selector rule and element.

class WinSelectorRule(CompoundRule):

    spec = config.lang.win_selector
    extras = [win_names_ref]
    exported = False

    def value(self, node):
        if node.has_child_with_name("win_names"):
            window = node.get_child_by_name("win_names").value()
            if not isinstance(window, Window):
                window = get_default_window(window)
            return window
        return Window.get_foreground()

win_selector = RuleRef(WinSelectorRule(), name="win_selector")


#---------------------------------------------------------------------------
# Internal monitor selector rule and element.

class MonSelectorRule(CompoundRule):

    spec = config.lang.mon_selector
    extras = [mon_names_ref]
    exported = False

    def value(self, node):
        if node.has_child_with_name("mon_names"):
            return node.get_child_by_name("mon_names").value()
        return None

mon_selector = RuleRef(MonSelectorRule(), name="mon_selector")


#---------------------------------------------------------------------------
# Exported window naming rule.

class NameWinRule(CompoundRule):

    spec = config.lang.name_win
    extras = [Dictation("name")]

    def _process_recognition(self, node, extras):
        name = str(extras["name"])
        window = Window.get_foreground()
        window.name = name
        win_names[name] = window
        self._log.debug("%s: named foreground window '%s'." % (self, window))

grammar.add_rule(NameWinRule())


#---------------------------------------------------------------------------
# Exported window focusing rule; brings named windows to the foreground.

class FocusWinRule(CompoundRule):

    spec = config.lang.focus_win
    extras = [win_selector]

    def _process_recognition(self, node, extras):
        window = extras["win_selector"]
        if not window:
            self._log.warning("No window with that name found.")
            return
        self._log.debug("%s: bringing window '%s' to the foreground."
                        % (self, window))
        for attempt in range(4):
            try:
                window.set_foreground()
            except Exception, e:
                self._log.warning("%s: set_foreground() failed: %s."
                                  % (self, e))
                time.sleep(0.2)
            else:
                break

grammar.add_rule(FocusWinRule())


#---------------------------------------------------------------------------
# Exported window focusing rule; brings named windows to the foreground.

class FocusTitleRule(CompoundRule):

    spec = config.lang.focus_title
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        title = str(extras["text"])
        action = FocusWindow(title=title)
        try:
            action.execute()
        except ActionError:
            self._log.warning("No window with that name found.")

grammar.add_rule(FocusTitleRule())


#---------------------------------------------------------------------------
# Internal fraction rule.

class FractionRule(Rule):

    sections = config.settings.grid

    def __init__(self):
        Rule.__init__(self,
                      name="fraction",
                      element=Integer("_frac", 0, self.sections + 1),
                      exported=False)

    def value(self, node):
        value = node.get_child_by_name("_frac").value()
        return float(value) / self.sections

fraction_rule = FractionRule()


#---------------------------------------------------------------------------

horz_left    = Compound(config.lang.left,   name="horz", value=0.0)
horz_right   = Compound(config.lang.right,  name="horz", value=1.0)
vert_top     = Compound(config.lang.top,    name="vert", value=0.0)
vert_bottom  = Compound(config.lang.bottom, name="vert", value=1.0)
horz_frac    = RuleRef(fraction_rule, name="horz")
vert_frac    = RuleRef(fraction_rule, name="vert")

horz_expl    = Alternative([horz_left, horz_right],  name="horz_expl")
horz_all     = Alternative([horz_expl, horz_frac],   name="horz_all")
vert_expl    = Alternative([vert_top,  vert_bottom], name="vert_expl")
vert_all     = Alternative([vert_expl, vert_frac],   name="vert_all")


#---------------------------------------------------------------------------

position_element = Compound(
              spec="   <horz_expl>"              # 1D, horizontal
                   " | <vert_expl>"              # 1D, vertical
                   " | <horz_all> <vert_all>"    # 2D, horizontal-vertical
                   " | <vert_expl> <horz_all>"   # 2D, vertical-horizontal
                   " | <vert_all> <horz_expl>",  # 2D, vertical-horizontal
              extras=[horz_expl, horz_all, vert_expl, vert_all],
             )
position_rule = Rule(
                     name="position_rule",
                     element=position_element,
                     exported=False,
                    )
position = RuleRef(position_rule, name="position")


#---------------------------------------------------------------------------

class TranslateRule(CompoundRule):

    spec = config.lang.translate_win
    extras = [
              win_selector,                  # Window selector element
              mon_selector,                  # Monitor selector element
              position,                      # Position element
             ]

    def _process_recognition(self, node, extras):
        # Determine which window to place on which monitor.
        window = extras["win_selector"]
        if "mon_selector" in extras:
            monitor = extras["mon_selector"].rectangle
        else:
            monitor = window.get_containing_monitor().rectangle

        # Calculate available area within monitor.
        pos = window.get_position()
        m_x1 = monitor.x1 + pos.dx / 2
        m_dx = monitor.dx - pos.dx
        m_y1 = monitor.y1 + pos.dy / 2
        m_dy = monitor.dy - pos.dy

        # Get spoken position and calculate how far to move.
        horizontal = node.get_child_by_name("horz")
        vertical = node.get_child_by_name("vert")
        if horizontal: dx = m_x1 + horizontal.value() * m_dx - pos.center.x
        else:          dx = 0
        if vertical:   dy = m_y1 + vertical.value() * m_dy - pos.center.y
        else:          dy = 0

        # Translate and move window.
        pos.translate(dx, dy)
        window.set_position(pos)

grammar.add_rule(TranslateRule())


#---------------------------------------------------------------------------

class ResizeRule(CompoundRule):

    spec = config.lang.resize_win
    extras = [
              win_selector,                  # Window selector element
              mon_selector,                  # Monitor selector element
              position,                      # Position element
             ]

    def _process_recognition(self, node, extras):
        # Determine which window to place on which monitor.
        window = extras["win_selector"]
        pos = window.get_position()
        monitor = window.get_containing_monitor().rectangle

        # Determine horizontal positioning.
        nodes = node.get_children_by_name("horz")
        horizontals = [(monitor.x1 + n.value() * monitor.dx) for n in nodes]
        if len(horizontals) == 1:
            horizontals.extend([pos.x1, pos.x2])
        elif len(horizontals) != 2:
            self._log.error("%s: Internal error."  % self)
            return
        x1, x2 = min(horizontals), max(horizontals)

        # Determine vertical positioning.
        nodes = node.get_children_by_name("vert")
        verticals = [(monitor.y1 + n.value() * monitor.dy) for n in nodes]
        if len(verticals) == 1:
            verticals.extend([pos.y1, pos.y2])
        elif len(verticals) != 2:
            self._log.error("%s: Internal error."  % self)
            return
        y1, y2 = min(verticals), max(verticals)

        # Move window.
        pos = Rectangle(x1, y1, x2-x1, y2-y1)
        window.set_position(pos)

grammar.add_rule(ResizeRule())


#---------------------------------------------------------------------------

class StretchRule(CompoundRule):

    spec = config.lang.stretch_win
    extras = [
              win_selector,                  # Window selector element
              position,                      # Position element
             ]

    def _process_recognition(self, node, extras):
        # Determine which window to place.
        window = extras["win_selector"]
        pos = window.get_position()
        monitor = window.get_containing_monitor().rectangle

        # Determine horizontal positioning.
        horizontals = [pos.x1, pos.x2]
        child = node.get_child_by_name("horz")
        if child: horizontals.append(monitor.x1 + child.value() * monitor.dx)
        x1, x2 = min(horizontals), max(horizontals)

        # Determine vertical positioning.
        verticals = [pos.y1, pos.y2]
        child = node.get_child_by_name("vert")
        if child: verticals.append(monitor.y1 + child.value() * monitor.dy)
        y1, y2 = min(verticals), max(verticals)

        # Move window.
        pos = Rectangle(x1, y1, x2-x1, y2-y1)
        window.set_position(pos)

grammar.add_rule(StretchRule())




grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
