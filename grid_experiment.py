import Tkinter as tk
# import re

from Tkconstants import *  # @UnusedWildImport


class TransparentWin(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
#         self.Drag = Drag(self)
        self.focus_force()
        self.overrideredirect(True)  # Removes the title bar.
        self.resizable(False, False)
        self.wm_attributes("-topmost", True)
        self.attributes("-alpha", 0.5)
        self.wm_title("Mouse Grid")
        self.wm_geometry('+' + str(0) + '+' + str(0))
        self.config(bg='#000000')
        # Border quirk, default border is 2. Simply give it -2 to cancel it.
#         canvas = Tk.Canvas(self, bg='#ffffff', bd=-2)
        totalWidth = 1280
        totalHeight = 978
        self.draw_grid(totalWidth, totalHeight)

    def draw_grid(self, totalWidth, totalHeight):
        numSq = 9
        sqX = totalWidth / numSq
        sqY = totalHeight / numSq
        thickevery = 3
        canvas = tk.Canvas(self, width=totalWidth, height=totalHeight,
            bg='white', bd=-2)  # Border quirk, default border is 2.
        canvas.pack()

        x1 = 0
        x2 = totalWidth
        xDiff = totalWidth - (numSq * sqX)
        yDiff = totalHeight - (numSq * sqY)
        count = 1
        # Draw horizontal lines.
        addToY = 0
        for k in range(0, sqY * (numSq + 1), sqY):
            k += addToY
            y1 = y2 = k
            if k == 0 or k == totalWidth:
                continue
            elif count == thickevery:
                fill = "black"
                count = 1
            else:
                fill = "gray"
                count += 1
            if yDiff > 0:
                addToY += 1
                yDiff -= 1
            canvas.create_line(x1, y1, x2, y2, fill=fill)
        # Draw vertical lines.
        y1 = 0
        y2 = numSq * sqY
        count = 1
        addToX = 0
        for k in range(0, sqX * (numSq + 1), sqX):
            k += addToX
            x1 = x2 = k
            if k == 0 or k == totalHeight:
                continue
            elif count == thickevery:
                fill = "black"
                count = 1
            else:
                fill = "gray"
                count += 1
            if xDiff > 0:
                addToX += 1
                xDiff -= 1
            canvas.create_line(x1, y1, x2, y2, fill=fill)
        # Add the numbers.
        position = 1
        for posY in range(1, 4):
            for posX in range(1, 4):
                canvas.create_text(((((posX - 1) * 3) + 1) * sqX) + (sqX / 2),
                                   ((((posY - 1) * 3) + 1) * sqY) + (sqY / 2),
                                   text=str(position))
                position += 1

    def exit(self, event):
        self.destroy()

#     def position(self):
#         _filter = re.compile(r"(\d+)?x?(\d+)?([+-])(\d+)([+-])(\d+)")
#         pos = self.winfo_geometry()
#         filtered = _filter.search(pos)
#         self.X = int(filtered.group(4))
#         self.Y = int(filtered.group(6))
#         return self.X, self.Y

    def callback(self, event):
        print "clicked at", event.x, event.y


def __run__():
    win = TransparentWin()
    win.mainloop()


if __name__ == '__main__':
    __run__()
