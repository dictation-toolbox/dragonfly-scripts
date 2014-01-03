"""A command module for Dragonfly, for controlling the mouse using a grid.

This is still a experimental functionality. It may contain several bugs,
and it may be heavily modified.

Apart from the normal mouse grid, this grid is made to support multiple
monitors, ctrl-click and shift-click.
So far this is only tested on a dual screen setup.

-----------------------------------------------------------------------------
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""

# import threading
#
# import datetime

from dragonfly import MappingRule, Function, IntegerRef, Choice, Dictation, \
    Grammar, AppContext, Rectangle

import grid_base

GRID_WINDOWS = {}
MONITORS = {}
MONITOR_SELECTED = None
MOUSE_MARK_POSITION = None
# POLLING_THREAD = None
# POLLING_COUNT = 0


def _poll_grids():
    global GRID_WINDOWS
#     global POLLING_THREAD
#     global POLLING_COUNT
#     POLLING_COUNT += 1
#     print("Polling: %s - %s" % (POLLING_COUNT, datetime.datetime.now()))
    viewables = 0
    for win in GRID_WINDOWS.values():
        if win.winfo_viewable():
            win.update()
            viewables += 1
    if viewables == 0:
        _stop_polling()
    elif POLLING_COUNT >= 20:
        for win in GRID_WINDOWS.values():
            if win.winfo_viewable():
                win.withdraw()


def _stop_polling():
    global POLLING_COUNT
#     global POLLING_THREAD
#     print("Stopping polling.")
#     POLLING_THREAD.cancel()
    POLLING_COUNT = 0


def mouse_grid(pos1=None, pos2=None, pos3=None, pos4=None, pos5=None,
               pos6=None, pos7=None, pos8=None, pos9=None, action=None):
    """Creates new or reuses grid windows. Can also delegate positioning."""
    global GRID_WINDOWS
    global MONITORS
    global MONITOR_SELECTED
    # Hide any existing grid windows.
    for win in GRID_WINDOWS.values():
        if win.winfo_viewable():
            win.withdraw()
#     global POLLING_THREAD
    if len(MONITORS) == 1 and pos1 == None:
        pos1 = 1
    if pos1 and pos1 <= len(MONITORS):
        index = pos1 - 1
        monitor = MONITORS[str(pos1)]
        MONITOR_SELECTED = pos1
        if not index in GRID_WINDOWS.keys():
            r = monitor.rectMonitor
            if len(MONITORS) == 1:
                monitorNum = None
            else:
                monitorNum = str(pos1)
            grid = grid_base.GridConfig(positionX=int(r.x),
                positionY=int(r.y), width=int(r.dx), height=int(r.dy),
                monitorNum=monitorNum)
            win = grid_base.TransparentWin(grid)
            if action == None:
                win.refresh(MONITOR_SELECTED)
            GRID_WINDOWS[index] = win
        else:
            win = GRID_WINDOWS[index]
            win.get_grid().reset()
            if action == None:
                win.refresh(MONITOR_SELECTED)
        if pos2:  # Continue using other given positions.
            mouse_pos(pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9,
                      action=None)
    else:
        MONITOR_SELECTED = None
        for index, monitor in MONITORS.items():
            if not index in GRID_WINDOWS.keys():
                r = monitor.rectMonitor
                grid = grid_base.GridConfig(positionX=int(r.x),
                    positionY=int(r.y), width=int(r.dx), height=int(r.dy),
                    monitorNum=str(index))
                win = grid_base.TransparentWin(grid)
                win.refresh(MONITOR_SELECTED)
                GRID_WINDOWS[int(index) - 1] = win
            else:
                win = GRID_WINDOWS[int(index) - 1]
                win.get_grid().reset()
                win.refresh(MONITOR_SELECTED)
#     POLLING_THREAD = threading.Timer(.5, _poll_grids)


def hide_grids(excludePosition=None):
    """Hides the grids, optionally excluding one grid.

    Grids are not closed but instead hidden, so they can be reused later.
    If excludePosition matches the position of a grid, it is not hidden.

    """
    global GRID_WINDOWS
    global MONITOR_SELECTED
    count = 0
    for index, win in GRID_WINDOWS.items():
        if excludePosition and str(excludePosition) == index:
            continue
        if win.winfo_viewable():
            win.withdraw()
        count += 1
    if count == len(GRID_WINDOWS):
        MONITOR_SELECTED = None
#         _stop_polling()


def mouse_pos(pos1, pos2=None, pos3=None, pos4=None, pos5=None, pos6=None,
              pos7=None, pos8=None, pos9=None, action=None):
    """Selects monitor (if not already selected), then repositions the grid.

    Takes multiple positions in sequence. If a monitor is not already selected,
    the first position variable is used to select monitor.
    The position variables are treated in sequence to select sections that the
    grid is moved into.

    """
    global GRID_WINDOWS
    global MONITOR_SELECTED
    monitorSelected = MONITOR_SELECTED
    # Hide any existing grid windows.
    for win in GRID_WINDOWS.values():
        if win.winfo_viewable():
            win.withdraw()
    if monitorSelected != None:
        variables = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
    else:
        variables = [pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9]
        monitorSelected = pos1
        hide_grids(excludePosition=pos1)
    win = GRID_WINDOWS[monitorSelected - 1]
    sections = [var for var in variables if var != None]
    for section in sections:
        _reposition_grid(win, section)
    if action:
        call_action(action, monitorSelected)
        monitorSelected = None
    else:
        win.refresh(monitorSelected)
    MONITOR_SELECTED = monitorSelected


def _reposition_grid(win, section):
    """Repositions the grid window to a specified section in the grid.

    If the grid is smaller than 25 pixels across, the grid is not repositioned
    into a section, but instead moved one section width in the direction of
    the selected section.

    """
    grid = win.get_grid()
    if grid.width > 25:
        grid.recalculate_to_section(section)
        grid.calculate_axis()
    else:
        grid.move_to_section(section)


def _init_mouse_action():
    """Gets the selected grid's coordinates, then hides the grid."""
    global GRID_WINDOWS
    global MONITOR_SELECTED
    if MONITOR_SELECTED != None:
        win = GRID_WINDOWS[MONITOR_SELECTED - 1]
        (positionX, positionY) = win.get_grid().get_absolute_centerpoint()
        # Hide the grid so mouse actions can reach the applications below.
        hide_grids()
        return (positionX, positionY)
    else:  # Can happen when all grids are visible.
        hide_grids()
        return (None, None)


def go():
    """Places the mouse at the grid coordinates. Hides the grid."""
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)


def left_click():
    """Places the mouse the grid coordinates and clicks the left mouse
    button.

    """
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        grid_base.left_click_mouse(positionX, positionY)


def right_click():
    """Places the mouse the grid coordinates and clicks the the right mouse
    button.

    """
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        grid_base.right_click_mouse(positionX, positionY)


def double_click():
    """Places the mouse the grid coordinates and double clicks the left mouse
    button.

    """
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        grid_base.double_click_mouse(positionX, positionY)


def control_click():
    """Places the mouse the grid coordinates and holds down the CTRL-key while
    clicking the left mouse button.

    """
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        grid_base.control_click(positionX, positionY)


def shift_click():
    """Places the mouse the grid coordinates and holds down the SHIFT-key while
    clicking the left mouse button.

    """
    (positionX, positionY) = _init_mouse_action()
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        grid_base.shift_click(positionX, positionY)


def mouse_mark():
    """Remembers the grid coordinates, to be used as a start position for
    mouse drag.

    """
    global MOUSE_MARK_POSITION
    MOUSE_MARK_POSITION = _init_mouse_action()
    (positionX, positionY) = MOUSE_MARK_POSITION
    if positionX != None and positionY != None:
        grid_base.move_mouse(positionX, positionY)
        mouse_grid()
    else:
        MOUSE_MARK_POSITION = None


def mouse_drag():
    """Holds down the left mouse button while moving the mouse mouse from a
    previous position to the current position.

    """
    global MOUSE_MARK_POSITION
    if MOUSE_MARK_POSITION:
        (startX, startY) = MOUSE_MARK_POSITION
        (targetX, targetY) = _init_mouse_action()
        grid_base.mouse_drag(startX, startY, targetX, targetY)
        MOUSE_MARK_POSITION = None
    else:
        print("Mouse drag failed, no start position marked.")


actions = {
    "[left] click": left_click,
    "right click": right_click,
    "double click": double_click,
    "control click": control_click,
    "shift click": shift_click,
    "mark": mouse_mark,
    "drag": mouse_drag,
    "go": go,
}


def call_action(action, monitorSelected):
    """Calls a action function, depending on the spoken action."""
    global MONITOR_SELECTED
    MONITOR_SELECTED = monitorSelected
    action()


init_rule = MappingRule(
    mapping={
        "[mouse] grid [<pos1>] [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>] [<action>]": Function(mouse_grid),  # @IgnorePep8
        # In case focus on the grid/grids has been lost.
        "(close|cancel|stop|abort) [mouse] grid": Function(hide_grids),  # @IgnorePep8
        "go": Function(go)
    },
    extras=[
        IntegerRef("pos1", 1, 10),
        IntegerRef("pos2", 1, 10),
        IntegerRef("pos3", 1, 10),
        IntegerRef("pos4", 1, 10),
        IntegerRef("pos5", 1, 10),
        IntegerRef("pos6", 1, 10),
        IntegerRef("pos7", 1, 10),
        IntegerRef("pos8", 1, 10),
        IntegerRef("pos9", 1, 10),
        Dictation("text"),
        Choice("action", actions),
    ],
    defaults={
        "pos1": None
    }
)
global_context = None  # Context is None, so grammar will be globally active.
grammar1 = Grammar("Grid init", context=global_context)
grammar1.add_rule(init_rule)
grammar1.load()


navigate_rule = MappingRule(
    mapping={
        "<pos1> [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>] [<action>]": Function(mouse_pos),  # @IgnorePep8
        "[left] click": Function(left_click),
        "right click": Function(right_click),
        "double click": Function(double_click),
        "control click": Function(control_click),
        "shift click": Function(shift_click),
        "mark": Function(mouse_mark),
        "drag": Function(mouse_drag),
        "(close|cancel|stop|abort) [[mouse] grid]": Function(hide_grids),  # @IgnorePep8
        "go": Function(go),
    },
    extras=[  # Interval 1-9.
        IntegerRef("pos1", 1, 10),
        IntegerRef("pos2", 1, 10),
        IntegerRef("pos3", 1, 10),
        IntegerRef("pos4", 1, 10),
        IntegerRef("pos5", 1, 10),
        IntegerRef("pos6", 1, 10),
        IntegerRef("pos7", 1, 10),
        IntegerRef("pos8", 1, 10),
        IntegerRef("pos9", 1, 10),
        Dictation("text"),
        Choice("action", actions),
    ],
    defaults={
        "pos1": 1
    }
)

context = AppContext(executable="natspeak", title="Grid overlay")
grammar2 = Grammar("Grid navigation", context=context)
grammar2.add_rule(navigate_rule)  # Add the top-level rule.
grammar2.load()  # Load the grammar.


def unload():
    """Unload function which will be called at unload time."""
    global grammar1
    if grammar1:
        grammar1.unload()
    grammar1 = None
    global grammar2
    if grammar2:
        grammar2.unload()
    grammar2 = None


# ----------------------------------------------------------------------------
# The following callback method is picked right out of Dragonfly, but modified
# to get the full size rectangle of the monitor.
# The original code only saves the rectangle excluding the taskbar.
# ----------------------------------------------------------------------------
import ctypes
from dragonfly.windows.monitor import _rect_t, _monitor_info_t, callback_t


class Monitor(object):
    """Holds the handle and rectangle information for a monitor."""
    def __init__(self, handle, rectWork, rectMonitor):
        assert isinstance(handle, int)
        self._handle = handle
        assert isinstance(rectWork, Rectangle)
        self._rectWork = rectWork
        assert isinstance(rectMonitor, Rectangle)
        self._rectMonitor = rectMonitor

    def __str__(self):
        return "%s(%d)" % (self.__class__.__name__, self._handle)

    def _set_handle(self, handle):
        assert isinstance(handle, int)
        self._handle = handle
    handle = property(fget=lambda self: self._handle,
                      fset=_set_handle,
                      doc="Protected access to handle attribute.")

    def _set_rect_work(self, rectangle):
        assert isinstance(rectangle, Rectangle)
        self._rectWork = rectangle
    rectWork = property(fget=lambda self: self._rectWork,
                      fset=_set_rect_work,
                      doc="Protected access to rectangle attribute.")

    def _set_rect_monitor(self, rectangle):
        assert isinstance(rectangle, Rectangle)
        self._rectMonitor = rectangle
    rectMonitor = property(fget=lambda self: self._rectMonitor,
                      fset=_set_rect_monitor,
                      doc="Protected access to rectangle attribute.")


def _callback(
              hMonitor,     # Handle to display monitor
              hdcMonitor,   # Handle to monitor DC
              lprcMonitor,  # Intersection rectangle of monitor
              dwData        # Data
             ):
    """Collects the information from a monitor and stores it in a list of
    monitor objects.

    """
    global MONITORS
    info = _monitor_info_t()
    info.cbSize = ctypes.sizeof(_monitor_info_t)
    info.rcMonitor = _rect_t()
    info.rcWork = _rect_t()
    # Retrieve monitor info.
    res = ctypes.windll.user32.GetMonitorInfoA(hMonitor,  # @UnusedVariable
        ctypes.byref(info))
    # Store monitor info.
    handle = int(hMonitor)
    r = info.rcMonitor
    rectMonitor = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
    rectWork = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
    monitor = Monitor(handle, rectWork, rectMonitor)
    MONITORS[str(len(MONITORS) + 1)] = monitor

    return True  # Continue enumerating monitors.


# Enumerate monitors and build a monitor list when this module is loaded.
res = ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback_t(_callback), 0)
# ----------------------------------------------------------------------------
# End of the modified Dragonfly callback method.
# ----------------------------------------------------------------------------


def __run__():
    import time

#     grid = grid_base.Grid(positionX=10, positionY=400, width=400,
#                                 height=400, monitorNum="1")
#     win = grid_base.TransparentWin(grid)
#     win.draw_grid()
#     win.update()
#     win.deiconify()
#     win.lift()
#     win.focus_force()
#     # Reposition
#     grid = win.get_grid()
#     grid.recalculate_to_section(5)
#     grid.calculate_axis()
#     win.refresh()
#     pass
#     win.mainloop()  # Needed to handle internal events.

# Tip for testing:
# Open a draw application, like MS Paint, and expand it over multiple screens.

    time.sleep(3)

# Open grid on all monitors, select monitor 2.
    mouse_grid()
    time.sleep(1)
    mouse_pos(pos1=1)
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    left_click()

    time.sleep(3)

# Open grid on all monitors again, select monitor 2.
    mouse_grid()
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    left_click()

    time.sleep(3)

# Quick select monitor grid, monitor 1.
    mouse_grid(1)
    time.sleep(1)
    mouse_pos(pos1=5)
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    left_click()

    time.sleep(3)

# Quick select monitor grid, monitor 2.
    mouse_grid(2)
    time.sleep(1)
    mouse_pos(pos1=5)
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    left_click()

# Mouse mark and mouse drag.
    mouse_grid()
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(1)
    mouse_pos(pos1=8)
    time.sleep(1)
    mouse_mark()
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(2)
    mouse_pos(pos1=7)
    time.sleep(1)
    mouse_drag()
    time.sleep(1)

# Quick monitor select, mouse mark and mouse drag across 2 monitors.
    mouse_grid(1)
    time.sleep(1)
    mouse_pos(pos1=3)
    time.sleep(1)
    mouse_mark()
    time.sleep(1)
    mouse_pos(pos1=2)
    time.sleep(2)
    mouse_pos(pos1=7)
    time.sleep(1)
    mouse_drag()
    time.sleep(1)

if __name__ == '__main__':
    __run__()
