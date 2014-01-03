# import threading
#
# import datetime

from dragonfly import *  # @UnusedWildImport

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
    global GRID_WINDOWS
    global MONITORS
    global MONITOR_COUNT
    global MONITOR_SELECTED
    # Hide any existing grid windows.
    for win in GRID_WINDOWS.values():
        if win.winfo_viewable():
            win.withdraw()
#     global POLLING_THREAD
    if MONITOR_COUNT == 1 and pos1 == None:
        pos1 = 1
    if pos1 and pos1 <= MONITOR_COUNT:
        index = pos1 - 1
        monitor = MONITORS[str(pos1)]
        MONITOR_SELECTED = pos1
        if not index in GRID_WINDOWS.keys():
            r = monitor.rectangle
            if MONITOR_COUNT == 1:
                monitorNum = None
            else:
                monitorNum = str(pos1)
            grid = grid_base.Grid(positionX=int(r.x),
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
                r = monitor.rectangle
                grid = grid_base.Grid(positionX=int(r.x),
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


def close_grid(exclude=None):
    global GRID_WINDOWS
    global MONITOR_SELECTED
    count = 0
    for index, win in GRID_WINDOWS.items():
        if exclude and str(exclude) == index:
            continue
        if win.winfo_viewable():
            win.withdraw()
        count += 1
    if count == len(GRID_WINDOWS):
        MONITOR_SELECTED = None
#         _stop_polling()


def mouse_pos(pos1, pos2=None, pos3=None, pos4=None, pos5=None, pos6=None,
              pos7=None, pos8=None, pos9=None, action=None):
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
        close_grid(exclude=pos1)
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
    grid = win.get_grid()
    if grid.width > 25:
        grid.recalculate_to_section(section)
        grid.calculate_axis()
    else:
        grid.move_to_section(section)


def _init_mouse_action():
    global GRID_WINDOWS
    global MONITOR_SELECTED
    if MONITOR_SELECTED != None:
        win = GRID_WINDOWS[MONITOR_SELECTED - 1]
        (positionX, positionY) = win.get_grid().get_absolute_centerpoint()
        close_grid()
        return (positionX, positionY)
    else:
        close_grid()


def go():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)


def left_click():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)
    grid_base.left_click_mouse(positionX, positionY)


def right_click():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)
    grid_base.right_click_mouse(positionX, positionY)


def double_click():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)
    grid_base.double_click_mouse(positionX, positionY)


def control_click():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)
    grid_base.control_click(positionX, positionY)


def shift_click():
    (positionX, positionY) = _init_mouse_action()
    grid_base.move_mouse(positionX, positionY)
    grid_base.shift_click(positionX, positionY)


def mouse_mark():
    global MOUSE_MARK_POSITION
    MOUSE_MARK_POSITION = _init_mouse_action()
    (positionX, positionY) = MOUSE_MARK_POSITION
    grid_base.move_mouse(positionX, positionY)
    mouse_grid()


def mouse_drag():
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
    global MONITOR_SELECTED
    MONITOR_SELECTED = monitorSelected
    action()


init_rule = MappingRule(
    mapping={
        "[mouse] grid [<pos1>] [<pos2>] [<pos3>] [<pos4>] [<pos5>] [<pos6>] [<pos7>] [<pos8>] [<pos9>] [<action>]": Function(mouse_grid),  # @IgnorePep8
        # In case focus on the grid/grids has been lost.
        "(close|cancel|stop|abort) [mouse] grid": Function(close_grid),  # @IgnorePep8
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
        "(close|cancel|stop|abort) [[mouse] grid]": Function(close_grid),  # @IgnorePep8
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


# Unload function which will be called at unload time.
def unload():
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
# from dragonfly import Rectangle, Monitor
from dragonfly.windows.monitor import _rect_t, _monitor_info_t, callback_t


def _callback(
              hMonitor,     # Handle to display monitor
              hdcMonitor,   # Handle to monitor DC
              lprcMonitor,  # Intersection rectangle of monitor
              dwData        # Data
             ):
    global MONITORS
    info = _monitor_info_t()
    info.cbSize = ctypes.sizeof(_monitor_info_t)
    info.rcMonitor = _rect_t()
    info.rcWork = _rect_t()
    # Retrieves monitor info.
    res = ctypes.windll.user32.GetMonitorInfoA(hMonitor,  # @UnusedVariable
        ctypes.byref(info))
    # Store monitor info.
    handle = int(hMonitor)
    r = info.rcMonitor
    rectangle = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
    monitor = Monitor(handle, rectangle)
    Monitor._log.debug("Found monitor %s with geometry %s."
                       % (monitor, rectangle))
    MONITORS[str(len(MONITORS) + 1)] = monitor

    return True  # Continue enumerating monitors.


# Enumerate monitors and build a monitor list when this module is loaded.
res = ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback_t(_callback), 0)
# ----------------------------------------------------------------------------
# End of the modified Dragonfly callback method.
# ----------------------------------------------------------------------------

MONITOR_COUNT = len(MONITORS)


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

# Open grid on all monitors, select monitor 2bowl.
    mouse_grid()
    time.sleep(2)
    mouse_pos(pos1=1)
    time.sleep(2)
    mouse_pos(pos1=2)
    time.sleep(2)
    go()

    time.sleep(3)

# Open grid on all monitors, select monitor 2.
    mouse_grid()
    time.sleep(2)
    mouse_pos(pos1=2)
    time.sleep(2)
    mouse_pos(pos1=2)
    time.sleep(2)
    go()

    time.sleep(3)

# Quick select monitor grid, on monitor 1.
    mouse_grid(1)
    time.sleep(2)
    mouse_pos(pos1=2)
    time.sleep(2)
    mouse_pos(pos1=5)
    time.sleep(2)
    left_click()

    time.sleep(3)

# Quick select monitor grid, and monitor 2.
    mouse_grid(2)
    time.sleep(2)
    mouse_pos(pos1=2)
    time.sleep(2)
    mouse_pos(pos1=5)
    time.sleep(2)
    left_click()

# Mouse mark and mouse drag.
#     mouse_grid()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     mouse_pos(pos1=5)
#     time.sleep(1)
#     mouse_mark()

#     mouse_grid()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(2)
#     mouse_pos(pos1=1)
#     time.sleep(1)
#     mouse_drag()
#     time.sleep(1)

    pass

if __name__ == '__main__':
    __run__()
