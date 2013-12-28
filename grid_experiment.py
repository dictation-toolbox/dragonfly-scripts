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
        self.attributes("-alpha", 0.6)
        self.wm_geometry('+' + str(10) + '+' + str(10))
        self.config(bg='#000000')
        # Border quirk, default border is 2. Simply give it -2 to cancel it.
#         canvas = Tk.Canvas(self, bg='#ffffff', bd=-2)
        totalWidth = 1000
        totalHeight = 800
        self.draw_grid(totalWidth, totalHeight)

    def draw_grid(self, totalWidth, totalHeight):
        numSq = 9
        sqX = totalWidth / numSq
        sqY = totalHeight / numSq
        thickevery = 3
        canvas = tk.Canvas(self, width=numSq * sqX, height=numSq * sqY,
            bg='white', bd=-2)
        canvas.pack()
        # Draw horizontal lines.
        x1 = 0
        x2 = numSq * sqX
        count = 1
        for k in range(0, sqY * (numSq + 1), sqY):
            y1 = k
            y2 = k
            if k == 0 or k == totalWidth:
                continue
            elif count == thickevery:
                fill = "black"
                count = 1
            else:
                fill = "gray"
                count += 1
            canvas.create_line(x1, y1, x2, y2, fill=fill)
        # Draw vertical lines.
        y1 = 0
        y2 = numSq * sqY
        for k in range(0, sqX * (numSq + 1), sqX):
            x1 = k
            x2 = k
            if k == 0 or k == totalHeight:
                continue
            elif count == thickevery:
                fill = "black"
                count = 1
            else:
                fill = "gray"
                count += 1
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


# class Drag:
#
#     def __init__(self, par, dissable=None, releasecmd=None):
#         self.Par = par
#         self.Dissable = dissable
#         self.ReleaseCMD = releasecmd
#         self.Par.bind('<Button-1>', self.relative_position)
#         self.Par.bind('<ButtonRelease-1>', self.drag_unbind)
#
#     def relative_position(self, event):
#         cx, cy = self.Par.winfo_pointerxy()
#         x, y = self.Par.position()
#         self.OriX = x
#         self.OriY = y
#         self.RelX = cx - x
#         self.RelY = cy - y
#         self.Par.bind('<Motion>', self.drag_wid)
#
#     def drag_wid(self, event):
#         cx, cy = self.Par.winfo_pointerxy()
#         d = self.Dissable
#         if d == 'x':
#             x = self.OriX
#             y = cy - self.RelY
#         elif d == 'y':
#             x = cx - self.RelX
#             y = self.OriY
#         else:
#             x = cx - self.RelX
#             y = cy - self.RelY
#         if x < 0:
#             x = 0
#         if y < 0:
#             y = 0
#         self.Par.wm_geometry('+' + str(x) + '+' + str(y))
#
#     def drag_unbind(self, event):
#         self.Par.unbind('<Motion>')
#         if self.ReleaseCMD != None:
#             self.ReleaseCMD()
#
#     def dissable(self):
#         self.Par.unbind('<Button-1>')
#         self.Par.unbind('<ButtonRelease-1>')
#         self.Par.unbind('<Motion>')


def __run__():
    win = TransparentWin()
    win.mainloop()


if __name__ == '__main__':
    __run__()
