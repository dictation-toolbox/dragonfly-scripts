import win32api
import win32con
import Tkinter as tk
from Tkconstants import *  # @UnusedWildImport
import time


class Grid:
    def __init__(self, positionX=0, positionY=0, width=1024, height=768,
                 monitorNum=None):
        self.monitorPositionX = positionX
        self.monitorPositionY = positionY
        self.monitorWidth = width
        self.monitorHeight = height
        self.monitorNum = monitorNum
        self.reset()

    def reset(self):
        self.positionX = self.monitorPositionX
        self.positionY = self.monitorPositionY
        self.width = self.monitorWidth
        self.height = self.monitorHeight
        self.calculate_axis()

    def get_geometry_string(self):
        geometry = "%dx%d+%d+%d" % (self.width, self.height, self.positionX,
                                    self.positionY)
        return geometry

    def calculate_axis(self):
        columns = 9
        stepX = self.width / columns
        stepY = self.height / columns
        xDiff = (self.width - 1) - (columns * stepX)
        yDiff = (self.height - 1) - (columns * stepY)
        self.axisX = self._calculate_one_axis(stepX, columns, xDiff)
        self.axisY = self._calculate_one_axis(stepY, columns, yDiff)

    def _calculate_one_axis(self, step, columns, diff):
        axis = []
        addTo = 0
        for value in range(0, step * (columns + 1), step):
            value += addTo
            axis.append(value)
            if diff > 0:
                addTo += 1
                diff -= 1
        return axis

    def get_relative_center_point(self):
        positionX = self.width / 2
        positionY = self.height / 2
        return (positionX, positionY)

    def get_absolute_centerpoint(self):
        x, y = self.get_relative_center_point()
        positionX = self.positionX + x
        positionY = self.positionY + y
        return (positionX, positionY)

    def _get_coordinates(self):
        return {
            1: (self.axisX[0], self.axisY[0], self.axisX[3], self.axisY[3]),
            2: (self.axisX[3], self.axisY[0], self.axisX[6], self.axisY[3]),
            3: (self.axisX[6], self.axisY[0], self.axisX[9], self.axisY[3]),
            4: (self.axisX[0], self.axisY[3], self.axisX[3], self.axisY[6]),
            5: (self.axisX[3], self.axisY[3], self.axisX[6], self.axisY[6]),
            6: (self.axisX[6], self.axisY[3], self.axisX[9], self.axisY[6]),
            7: (self.axisX[0], self.axisY[6], self.axisX[3], self.axisY[9]),
            8: (self.axisX[3], self.axisY[6], self.axisX[6], self.axisY[9]),
            9: (self.axisX[6], self.axisY[6], self.axisX[9], self.axisY[9]),
        }

    def recalculate_to_section(self, section):
        coordinates = self._get_coordinates()
        (x1, y1, x2, y2) = coordinates[section]
        self.positionX = self.positionX + x1
        self.positionY = self.positionY + y1
        self.width = x2 - x1
        self.height = y2 - y1
        self._adjust_edges()

    def _adjust_edges(self):
        if self.positionX > (self.monitorPositionX + 2):
            self.positionX -= 2
            self.width += 2
        if self.positionY > (self.monitorPositionY + 2):
            self.positionY -= 2
            self.height += 2
        if (self.positionX + self.width) < (self.monitorPositionX + \
                                            self.monitorWidth - 2):
            self.width += 2
        if (self.positionY + self.height) < (self.monitorPositionY + \
                                             self.monitorWidth - 2):
            self.height += 2

    def move_to_section(self, section):
        coordinates = self._get_coordinates()
        (x1, y1, x2, y2) = coordinates[section]
        sectionPositionX = (x2 + x1) / 2
        sectionPositionY = (y2 + y1) / 2
        centerX, centerY = self.get_relative_center_point()
        moveX = sectionPositionX - centerX
        moveY = sectionPositionY - centerY
        self.positionX = self.positionX + moveX
        self.positionY = self.positionY + moveY


class TransparentWin(tk.Tk):

    def __init__(self, grid):
        tk.Tk.__init__(self, baseName="")  # baseName replaces argv params.
        self._grid = grid
        self.overrideredirect(True)  # Removes the title bar.
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 0.5)
        self.wm_title("Grid overlay")  # Important for Dragonfly's Context.
        self.wm_geometry(self._grid.get_geometry_string())
        self._canvas = tk.Canvas(master=self, width=self._grid.width,
            height=self._grid.height, bg='white',
            bd=-2)  # Border quirk, default border is 2.
        self._canvas.pack()
        self._monitorNumberItem = None
        self._timestamp = time.time()
#         self.after(1000, self._timer)

#     def _timer(self):
#         """Timeout after 8 seconds of inactivity."""
#         if self.winfo_viewable():
#             if time.time() - self._timestamp > 8:
#                 self.withdraw()

    def get_grid(self):
        return self._grid

    def refresh(self, monitorSelected=False):
        self._timestamp = time.time()
        self.deiconify()  # Quirk: Secondary window won't refresh without this.
        self._canvas.delete("all")
        self.wm_geometry(self._grid.get_geometry_string())
        self.draw_grid(monitorSelected)
        self.deiconify()
        self.lift()
        time.sleep(0.1)  # Pause to allow focus to take.
        self.focus_force()  # Focus.
        self.focus_set()  # Really focus.
        self.focus()  # Really really focus.

    def draw_grid(self, monitorSelected=False):
        self._draw_lines()
        if not monitorSelected and self._grid.width == self._grid.monitorWidth:
            self.draw_monitor_number()
        elif self._grid.width > 80 and self._grid.height > 80:
            self._draw_section_numbers()

    def _draw_lines(self):
        minimumX = 0
        maximumX = self._grid.width
        axisX = self._grid.axisX
        minimumY = 0
        maximumY = self._grid.height
        axisY = self._grid.axisY
        for index, position in enumerate(axisY):
            fill = "black"
            if index % 3:
                fill = "gray"
            self._canvas.create_line(minimumX, position, maximumX, position,
                                     fill=fill)
        for index, position in enumerate(axisX):
            fill = "black"
            if index % 3:
                fill = "gray"
            self._canvas.create_line(position, minimumY, position, maximumY,
                                     fill=fill)
        self.update()

    def _draw_section_numbers(self):
        axisX = self._grid.axisX
        axisY = self._grid.axisY
        position = 1
        for y in range(3):
            for x in range(3):
                self._canvas.create_text(
                    (axisX[(3 * x) + 1] + axisX[(3 * x) + 2]) / 2,
                    (axisY[(3 * y) + 1] + axisY[(3 * y) + 2]) / 2,
                    text=str(position), font="Arial 10 bold")
                position += 1
        self.update()

    def draw_monitor_number(self):
        positionX, positionY = self._grid.get_relative_center_point()
        self._monitorNumberItem = self._canvas.create_text(positionX,
            positionY, fill="#aaaaaa", text=str(self._grid.monitorNum),
            font="Arial 100 bold")
        self.update()

    def exit(self):
        self.destroy()


def _mouse_event(value, x, y):
    win32api.mouse_event(value, x, y, 0, 0)


def move_mouse(positionX, positionY):
    win32api.SetCursorPos((positionX, positionY))


def left_click_mouse(positionX, positionY):
    _mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, positionX, positionY)
    _mouse_event(win32con.MOUSEEVENTF_LEFTUP, positionX, positionY)


def double_click_mouse(positionX, positionY):
    _mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, positionX, positionY)
    _mouse_event(win32con.MOUSEEVENTF_LEFTUP, positionX, positionY)
    _mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, positionX, positionY)
    _mouse_event(win32con.MOUSEEVENTF_LEFTUP, positionX, positionY)


def right_click_mouse(positionX, positionY):
    _mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, positionX, positionY)
    _mouse_event(win32con.MOUSEEVENTF_RIGHTUP, positionX, positionY)


def control_click(positionX, positionY):
    win32api.keybd_event(win32con.VK_CONTROL, 0, 0, 0)  # @IgnorePep8
    left_click_mouse(positionX, positionY)
    win32api.keybd_event(win32con.VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)


def shift_click(positionX, positionY):
    win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)  # @IgnorePep8
    left_click_mouse(positionX, positionY)
    win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)


def mouse_drag(startX, startY, targetX, targetY):
    win32api.SetCursorPos((startX, startY))
    _mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, startX, startY)
    win32api.SetCursorPos((targetX, targetY))
    time.sleep(0.3)  # Fix for glitching on secondary screen.
    _mouse_event(win32con.MOUSEEVENTF_LEFTUP, targetX, targetY)


def __run__():
#     import win32api
#     print("Get cursor position: %s, %s" % win32api.GetCursorPos())
#     print()
    grid = Grid(positionX=10, positionY=400, width=400, height=400,
        monitorNum="1")
    win = TransparentWin(grid)
    win.draw_grid()
    win.update()
    win.deiconify()
    win.lift()
    win.focus_force()
    # Reposition
    grid = win.get_grid()
    grid.recalculate_to_section(5)
    grid.calculate_axis()
    win.refresh()
    pass
    win.mainloop()  # Needed to handle internal events.


if __name__ == '__main__':
    __run__()
