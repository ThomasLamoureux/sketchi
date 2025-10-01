from tkinter import *


from PaintPrototype import test

class Project:


    def __init__(self, id):
        self.id = id


    def init_canvas(self):
        self.canvas = Canvas(width=1000, height=1000, bg="#FFFFFF")


    def paint(self, x_start, y_start, x_end, y_end, fill, width, capstyle, joinstyle):
        self.canvas.create_line(x_start, y_start, x_end, y_end, fill=fill, width=width, capstyle=capstyle, joinstyle=joinstyle)

    def set_bg(self, bg):
        self.canvas.bg = bg



proj = Project(123)

proj.init_canvas()

