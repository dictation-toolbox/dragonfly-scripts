#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for **taskbar** and icon tray access
===================================================
This file implements commands for controlling tasks on the
taskbar and icons in the icon tray.

Commands
--------

Command: **"[open | switch to] task <number>"**
    Open the specified task on the taskbar.
    The *<number>* extra is a number (1, 2, ...) designating which
    task to activate.  The application on the taskbar which is
    closest to the "Start" button is task *number 1*.  The next
    is *number 2*, and so on.  This works for both horizontal and
    vertical taskbars.

Command: **"<action> task <number>"**
    Similar to the command above, but performs some action
    under specified task.  The following actions are available:

     - **"(menu | pop up)"** -- show the pop-up menu of the task,
       as if a right-click was done on the taskbar.
     - **"(maximize | max)"** -- maximize the task.
     - **"(minimize | min)"** -- minimize the task.
     - **"restore"** -- restore the task.
     - **"close"** -- close the task.

Command: **"[open] icon <number>"**
    Open the specified icon in the icon tray.
    The *<number>* extra is a number (1, 2, ...) designating which
    icon to activate.  The numbering is similar to that explained
    above for tasks on the taskbar.

Command: **"(menu | pop up) icon <number>"**
    Pop-up the menu for the specified icon in the icon tray.

Usage examples
--------------

Several concrete usage examples of the commands described above:

 - Say **"task 4"** to bring the fourth application on the taskbar
   to the foreground.
 - Say **"close task 2"** to close the second application on
   the taskbar.
 - Say **"icon 1"** to activate the first icon visible in the
   icon tray, as if it was double-clicked.
 - Say **"pop up icon 3"** to bring up the menu of the third
   icon visible in the icon tray, as if it was right-clicked.

"""


from dragonfly import *  # @UnusedWildImport


#---------------------------------------------------------------------------
# This rule controls tasks on the taskbar.

class TaskRule(MappingRule):

    mapping = {
               "[open | switch to] task <n>":  Key("space"),
               "(menu | pop up) task <n>":     Key("apps"),
               "close task <n>":               Key("apps/10, c"),
               "restore task <n>":             Key("apps/10, r"),
               "(minimize | min) task <n>":    Key("apps/10, n"),
               "(maximize | max) task <n>":    Key("apps/10, x"),
              }
    extras = [IntegerRef("n", 1, 50)]

    def _process_recognition(self, value, extras):
        count = extras["n"] - 1
        action = Key("w-b/10, s-tab/10, right:%d/10" % count) + value
        action.execute()


#---------------------------------------------------------------------------
# This rule controls icons in the icon tray.

class IconRule(MappingRule):

    mapping = {
               "[open] icon <n>":              Key("enter"),
               "(menu | pop up) icon <n>":     Key("apps"),
              }
    extras = [IntegerRef("n", 1, 12)]

    def _process_recognition(self, value, extras):
        count = extras["n"] - 1
        action = Key("w-b/10, right:%d/10" % count) + value
        action.execute()


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar = Grammar("taskbar")
grammar.add_rule(TaskRule())
grammar.add_rule(IconRule())
grammar.load()


# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
