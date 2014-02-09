"""A command module for Dragonfly, for controlling the mouse using a grid.

This is still an experimental functionality. It may contain several bugs,
and it may be heavily modified.

Apart from the normal mouse grid, this grid is made to support multiple
monitors, ctrl-click and shift-click.
So far this is only tested on a dual screen setup.

-----------------------------------------------------------------------------
Licensed under the LGPL, see http://www.gnu.org/licenses/

"""
from dragonfly import (
    MappingRule,
    Function,
    IntegerRef,
    Choice,
    Dictation,
    Grammar,
    AppContext,
)

from lib.grid_base import (
    left_click,
    right_click,
    double_click,
    control_click,
    shift_click,
    mouse_mark,
    mouse_drag,
    go,
    mouse_grid,
    hide_grids,
    mouse_pos
)


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
#     global MONITORS
#     global GRID_WINDOWS
    global grammar1
    if grammar1:
        grammar1.unload()
    grammar1 = None
    global grammar2
    if grammar2:
        grammar2.unload()
    grammar2 = None
#     for win in GRID_WINDOWS.values():
#         win.destroy()
#         win = None
#     MONITORS = None


# # ----------------------------------------------------------------------------
# # The following callback method is picked right out of Dragonfly, but modified
# # to get the full size rectangle of the monitor.
# # The original code only saves the rectangle excluding the taskbar.
# # ----------------------------------------------------------------------------
# import ctypes
# from dragonfly.windows.monitor import _rect_t, _monitor_info_t, callback_t
# 
# 
# class Monitor(object):
#     """Holds the handle and rectangle information for a monitor."""
#     def __init__(self, handle, rectWork, rectMonitor):
#         assert isinstance(handle, int)
#         self._handle = handle
#         assert isinstance(rectWork, Rectangle)
#         self._rectWork = rectWork
#         assert isinstance(rectMonitor, Rectangle)
#         self._rectMonitor = rectMonitor
# 
#     def __str__(self):
#         return "%s(%d)" % (self.__class__.__name__, self._handle)
# 
#     def _set_handle(self, handle):
#         assert isinstance(handle, int)
#         self._handle = handle
#     handle = property(fget=lambda self: self._handle,
#                       fset=_set_handle,
#                       doc="Protected access to handle attribute.")
# 
#     def _set_rect_work(self, rectangle):
#         assert isinstance(rectangle, Rectangle)
#         self._rectWork = rectangle
#     rectWork = property(fget=lambda self: self._rectWork,
#                       fset=_set_rect_work,
#                       doc="Protected access to rectangle attribute.")
# 
#     def _set_rect_monitor(self, rectangle):
#         assert isinstance(rectangle, Rectangle)
#         self._rectMonitor = rectangle
#     rectMonitor = property(fget=lambda self: self._rectMonitor,
#                       fset=_set_rect_monitor,
#                       doc="Protected access to rectangle attribute.")
# 
# 
# def _callback(
#               hMonitor,     # Handle to display monitor
#               hdcMonitor,   # Handle to monitor DC
#               lprcMonitor,  # Intersection rectangle of monitor
#               dwData        # Data
#              ):
#     """Collects the information from a monitor and stores it in a list of
#     monitor objects.
# 
#     """
#     global MONITORS
#     info = _monitor_info_t()
#     info.cbSize = ctypes.sizeof(_monitor_info_t)
#     info.rcMonitor = _rect_t()
#     info.rcWork = _rect_t()
#     # Retrieve monitor info.
#     res = ctypes.windll.user32.GetMonitorInfoA(hMonitor,  # @UnusedVariable
#         ctypes.byref(info))
#     # Store monitor info.
#     handle = int(hMonitor)
#     r = info.rcMonitor
#     rectMonitor = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
#     rectWork = Rectangle(r.left, r.top, r.right - r.left, r.bottom - r.top)
#     monitor = Monitor(handle, rectWork, rectMonitor)
#     MONITORS[str(len(MONITORS) + 1)] = monitor
# 
#     return True  # Continue enumerating monitors.
# 
# 
# # Enumerate monitors and build a monitor list when this module is loaded.
# res = ctypes.windll.user32.EnumDisplayMonitors(0, 0, callback_t(_callback), 0)
# # ----------------------------------------------------------------------------
# # End of the modified Dragonfly callback method.
# # ----------------------------------------------------------------------------


# def __run__():
#     import time
# 
# #     grid = grid_base.Grid(positionX=10, positionY=400, width=400,
# #                                 height=400, monitorNum="1")
# #     win = grid_base.TransparentWin(grid)
# #     win.draw_grid()
# #     win.update()
# #     win.deiconify()
# #     win.lift()
# #     win.focus_force()
# #     # Reposition
# #     grid = win.get_grid()
# #     grid.recalculate_to_section(5)
# #     grid.calculate_axis()
# #     win.refresh()
# #     pass
# #     win.mainloop()  # Needed to handle internal events.
# 
# # Tip for testing:
# # Open a draw application, like MS Paint, and expand it over multiple screens.
# 
#     time.sleep(3)
# 
# # Open grid on all monitors, select monitor 2.
#     mouse_grid()
#     time.sleep(1)
#     mouse_pos(pos1=1)
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     left_click()
# 
#     time.sleep(3)
# 
# # Open grid on all monitors again, select monitor 2.
#     mouse_grid()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     left_click()
# 
#     time.sleep(3)
# 
# # Quick select monitor grid, monitor 1.
#     mouse_grid(1)
#     time.sleep(1)
#     mouse_pos(pos1=5)
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     left_click()
# 
#     time.sleep(3)
# 
# # Quick select monitor grid, monitor 2.
#     mouse_grid(2)
#     time.sleep(1)
#     mouse_pos(pos1=5)
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     left_click()
# 
# # Mouse mark and mouse drag.
#     mouse_grid()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(1)
#     mouse_pos(pos1=8)
#     time.sleep(1)
#     mouse_mark()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(2)
#     mouse_pos(pos1=7)
#     time.sleep(1)
#     mouse_drag()
#     time.sleep(1)
# 
# # Quick monitor select, mouse mark and mouse drag across 2 monitors.
#     mouse_grid(1)
#     time.sleep(1)
#     mouse_pos(pos1=3)
#     time.sleep(1)
#     mouse_mark()
#     time.sleep(1)
#     mouse_pos(pos1=2)
#     time.sleep(2)
#     mouse_pos(pos1=7)
#     time.sleep(1)
#     mouse_drag()
#     time.sleep(1)
# 
# if __name__ == '__main__':
#     __run__()
