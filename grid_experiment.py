import Tkinter as tk
from Tkconstants import *  # @UnusedWildImport


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

    def new_position(self, positionX, positionY, width, height):
        self.positionX = positionX
        self.positionY = positionY
        self.width = width
        self.height = height
        self.calculate_axis()

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

    def get_center_point(self):
        positionX = self.width / 2
        positionY = self.height / 2
        return (positionX, positionY)


class TransparentWin(tk.Tk):
    def __init__(self, grid):
        tk.Tk.__init__(self, baseName="")  # baseName replaces argv params.
        self._grid = grid
        self.overrideredirect(True)  # Removes the title bar.
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 0.5)
        self.wm_title("Grid overlay")  # Important for Dragonfly context.
        self.wm_geometry(self._grid.get_geometry_string())
        self._canvas = tk.Canvas(master=self, width=self._grid.width,
            height=self._grid.height, bg='white',
            bd=-2)  # Border quirk, default border is 2.
        self._canvas.pack()
        self._monitorNumberItem = None

    def draw_grid(self):
        self._draw_lines(minimumX=0, maximumX=self._grid.width,
                         axisX=self._grid.axisX, minimumY=0,
                         maximumY=self._grid.height, axisY=self._grid.axisY)

    def _draw_lines(self, minimumX, maximumX, axisX, minimumY, maximumY,
                    axisY):
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
        # Add eventual monitor number.
        if self._grid.monitorNum:
            self.draw_monitor_number()
        # Add section the numbers.
        position = 1
        for y in range(3):
            for x in range(3):
                self._canvas.create_text(
                    (axisX[(3 * x) + 1] + axisX[(3 * x) + 2]) / 2,
                    (axisY[(3 * y) + 1] + axisY[(3 * y) + 2]) / 2,
                    text=str(position))
                position += 1

    def draw_monitor_number(self):
        positionX, positionY = self._grid.get_center_point()
        self._monitorNumberItem = self._canvas.create_text(positionX,
            positionY, fill="#555555", text=str(self._grid.monitorNum),
            font="Arial 100 bold")

    def remove_monitor_number(self):
        self._canvas.delete(self._monitorNumText)
        self.update_idletasks()
        self.deiconify()

    def exit(self):
        self.destroy()

    def callback(self, event):
        print "clicked at", event.x, event.y


def __run__():
    from dragonfly import Rectangle
    r = Rectangle(x1=10, y1=400, dx=400, dy=400)
    grid = Grid(positionX=int(r.x),
        positionY=int(r.y), width=int(r.dx), height=int(r.dy),
        monitorNum=None)
    win = TransparentWin(grid)
    win.draw_grid()
    win.update()
    win.deiconify()
    win.lift()
    win.focus_force()
    pass
    #win.mainloop()  # Needed to handle internal events.


if __name__ == '__main__':
    __run__()
