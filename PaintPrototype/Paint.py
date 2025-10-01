from tkinter import *
from tkinter import colorchooser, ttk

import CanvasUtil



class Pen:
    def __init__(self, name, defualt_width, capstyle, smoothing, permanent_color):
        self.name = name
        self.width = defualt_width
        self.capstyle = capstyle
        self.smoothing = smoothing
        self.permanent_color = permanent_color

    def set_width(self, width):
        self.width = width

class Paint_Canvas:
    def __init__(self, window, width, height, bg):
        self.canvas = Canvas(window, width=width, height=height, bg=bg)
        self.canvas.pack(fill=BOTH, expand=True)

pen_selection = {
    "erasor": Pen("default", 15, "round", True, "white"),
    "default": Pen("default", 10, "round", True, None),
}

class Paint_Window:
    def __init__(self, window):
        self.window = window
        self.pen_color = "black"
        self.bg_color = "white"
        self.old_x = None
        self.old_y = None
        self.pen = pen_selection["default"]
        self.draw_window()
        

    def paint(self, event):
        print(f"{event.x} , {event.y}")
        if self.old_x and self.old_y:
            self.paint_canvas.canvas.create_line(self.old_x, self.old_y, event.x, event.y, width = self.pen.width
                                                 , fill = self.pen.permanent_color or self.pen_color, capstyle=self.pen.capstyle, smooth = self.pen.smoothing)
        self.old_x = event.x
        self.old_y = event.y


    def system_paint(self, old_x, old_y, new_x, new_y, fill, width, capstyle, joinstyle):
        self.paint_canvas.canvas.create_line(old_x, old_y, new_x, new_y, fill=fill, width=width, capstyle=capstyle, joinstyle=joinstyle)
    

    def set_pen(self, pen):
        self.pen = pen


    def reset(self, event):
        self.old_x = None
        self.old_y = None
    

    def change_pen(self, pen):
        self.pen = pen_selection[pen]


    def set_pen_width(self, width):
        self.pen.set_width(width)

    def erasor(self):
        self.change_pen("erasor")

    def default_pen(self):
        self.change_pen("default")

    def draw_window(self):
        self.controls = Frame(self.window, padx=5, pady=5)
        textpw = Label(self.controls, text='Pen Width', font='Georgia 16')
        textpw.grid(row=0, column=0)

        color_button = Button(self.window, text = "Select color", command = self.change_color)
        color_button.pack()

        pen_button = Button(self.window, text = "Pen", command = self.default_pen)
        pen_button.pack()

        erasor_button = Button(self.window, text = "Erasor", command = self.erasor)
        erasor_button.pack()

        self.slider = ttk.Scale(self.controls, from_ = 5, to = 100, command = self.set_pen_width, orient = 'vertical')
        self.slider.set(self.pen.width)
        self.slider.grid(row=0, column=1)
        self.controls.pack(side="left")


        menu = Menu(self.window)
        self.window.config(menu=menu)
        optionmenu = Menu(menu)
        menu.add_cascade(label='Menu', menu=optionmenu)
        optionmenu.add_command(label='Brush Color', command=self.change_color)
        optionmenu.add_command(label='Exit', command=self.window.destroy)    
    
        paint_canvas = Paint_Canvas(self.window, 500, 500, self.bg_color)
        paint_canvas.canvas.bind('<B1-Motion>', self.paint)
        paint_canvas.canvas.bind('<ButtonRelease-1>', self.reset)

        self.paint_canvas = paint_canvas



    def change_color(self):
        color_code = colorchooser.askcolor(title ="Choose color")[1]
        self.pen_color = color_code

import threading

wind = [None]

def start(wind):
    win = Tk()
    win.title("Paint App")
    wind[0] = Paint_Window(win)
    win.mainloop()

def system_paint(old_x, old_y, new_x, new_y, fill, width, capstyle, joinstyle):
    print(f"{new_x} , {new_y}")
    wind[0].system_paint(old_x, old_y, new_x, new_y, fill, width, capstyle, joinstyle)

thread = threading.Thread(target=start, args=(wind,))
thread.daemon = True  # Kills thread when main program exits
thread.start()
