import customtkinter as ctk
from tkinter import Canvas
import tkinter
from FrontEnd.color_picker import ColorPicker
import ServerCommunication.Pipeline as Pipeline

from PIL import Image, ImageDraw, ImageTk


class SketchiiArtboard:
    def __init__(self, app):
        self.app = app
        self.artboard_mode = False
        self.drawing = False
        self.last_x = None
        self.last_y = None

        self.brush_color = self.app.accent_orange
        self.brush_size = 3
        self.brush_opacity = 1.0  # 0.0 .. 1.0

    
        self._img = None
        self._draw = None
        self._img_tk = None
        self._img_id = None

        self.color_picker = ColorPicker(app, self)

   
    def toggle_artboard_mode(self, event=None):
        if not self.artboard_mode:
            self.artboard_mode = True
            self.app.channel_title_label.configure(text="Exit (Notice: Exiting will currently bug artboard and prevent usage when returning)")
            self.switch_to_artboard()

            # Pipeline.send_message("drawings_request", "")
        else:
            self.artboard_mode = False
            self.app.channel_title_label.configure(text="Open Artboard")
            self.switch_to_chat()

    def switch_to_artboard(self):
     
        self.app.chat_area.pack_forget()
        self.app.input_frame.pack_forget()

        
        self.canvas = Canvas(self.app.main_frame, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(20, 10))

      
        self.canvas.bind("<Configure>", self._maybe_init_surface_once)

       
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

       
        self.app.channel_frame.configure(width=200) #minichat
        for w in self.app.channel_frame.winfo_children():
            w.destroy()

        mini_header = ctk.CTkFrame(self.app.channel_frame, height=50,
                                   fg_color=self.app.bg_medium, corner_radius=0)
        mini_header.pack(fill="x")
        ctk.CTkLabel(mini_header, text="Quick Chat",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color=self.app.text_color).pack(pady=15, padx=10)

        self.mini_chat = ctk.CTkScrollableFrame(self.app.channel_frame,
                                                fg_color=self.app.bg_light, corner_radius=0)
        self.mini_chat.pack(fill="both", expand=True, padx=5, pady=5)

        mini_input_frame = ctk.CTkFrame(self.app.channel_frame, height=60,
                                        fg_color=self.app.bg_medium, corner_radius=0)
        mini_input_frame.pack(fill="x", padx=5, pady=5)
        mini_input_frame.pack_propagate(False)

        self.mini_entry = ctk.CTkEntry(mini_input_frame, placeholder_text="Message", height=35,
                                       corner_radius=17, fg_color=self.app.bg_light, border_width=1,
                                       border_color=self.app.accent_orange, text_color=self.app.text_color,
                                       font=ctk.CTkFont(size=12))
        self.mini_entry.pack(fill="x", padx=5, pady=12)
        self.mini_entry.bind("<Return>", lambda e: self.send_mini_message())

       
        self.create_drawing_tools()

    def switch_to_chat(self):
        if hasattr(self, "canvas"):
            self.canvas.destroy()
        if hasattr(self, "tools_frame"):
            self.tools_frame.destroy()

        self.app.chat_area.pack(fill="both", expand=True, padx=20, pady=20)
        self.app.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.app.channel_frame.configure(width=240)

        for w in self.app.channel_frame.winfo_children():
            w.destroy()

        server_header = ctk.CTkFrame(self.app.channel_frame, height=60,
                                     fg_color=self.app.bg_medium, corner_radius=0)
        server_header.pack(fill="x")
        ctk.CTkLabel(server_header, text="Server Name",
                     font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=self.app.text_color).pack(pady=20, padx=15, anchor="w")

        ctk.CTkLabel(self.app.channel_frame, text="Channels",
                     font=ctk.CTkFont(size=14, weight="bold"),
                     text_color="#888888").pack(pady=(10, 5), padx=15, anchor="w")

        self.app.add_channel("#mainchat", True)
        self.app.add_channel("#artchat", False)

    # tools ui
    def create_drawing_tools(self):
        self.tools_frame = ctk.CTkFrame(self.app.main_frame,
                                        fg_color=self.app.bg_medium, corner_radius=10)
        self.tools_frame.pack(fill="x", padx=20, pady=(0, 20))
     

        #Left: color picker
        left = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        left.pack(side="left", fill="y", padx=15, pady=15)
        self.color_picker.create_color_bar(left)

        #Right: actions
        right = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        right.pack(side="right", fill="y", padx=15, pady=15)

        clear_btn = ctk.CTkButton(right, text="Clear", width=80, height=35, corner_radius=17,
                                  fg_color="#cc0000", hover_color="#ff0000",
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  command=self.clear_canvas)
        clear_btn.pack(side="right", padx=(10, 0))

        eraser_btn = ctk.CTkButton(right, text="Eraser", width=80, height=35, corner_radius=17,
                                   fg_color=self.app.bg_light, hover_color=self.app.bg_dark,
                                   font=ctk.CTkFont(size=12, weight="bold"),
                                   command=lambda: self.change_color("#ffffff"))
        eraser_btn.pack(side="right", padx=5)

        #sliders
        center = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        center.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        #opacity slider
        op_label = ctk.CTkLabel(center, text="Opacity:", font=ctk.CTkFont(size=12, weight="bold"),
                                text_color=self.app.text_color)
        op_label.pack(anchor="w", pady=(0, 5))

        op_row = ctk.CTkFrame(center, fg_color="transparent")
        op_row.pack(fill="x", pady=(0, 8))

        self.opacity_slider = ctk.CTkSlider(
            op_row, from_=0, to=100, number_of_steps=100, width=250, height=20,
            button_color=self.app.accent_orange, button_hover_color="#ff8555",
            progress_color=self.app.accent_orange, fg_color=self.app.bg_light,
            command=self.update_brush_opacity
        )
        self.opacity_slider.set(100)
        self.opacity_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.opacity_display = ctk.CTkLabel(op_row, text="100%", width=50,
                                            font=ctk.CTkFont(size=12, weight="bold"),
                                            text_color=self.app.accent_orange)
        self.opacity_display.pack(side="left")

        #brush size slider
        size_label = ctk.CTkLabel(center, text="Brush Size:",
                                  font=ctk.CTkFont(size=12, weight="bold"),
                                  text_color=self.app.text_color)
        size_label.pack(anchor="w", pady=(0, 5))

        size_row = ctk.CTkFrame(center, fg_color="transparent")
        size_row.pack(fill="x")

        self.size_slider = ctk.CTkSlider(
            size_row, from_=1, to=30, number_of_steps=29, width=250, height=20,
            button_color=self.app.accent_orange, button_hover_color="#ff8555",
            progress_color=self.app.accent_orange, fg_color=self.app.bg_light,
            command=self.update_brush_size
        )
        self.size_slider.set(3)
        self.size_slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.size_display = ctk.CTkLabel(size_row, text="3px", width=50,
                                         font=ctk.CTkFont(size=12, weight="bold"),
                                         text_color=self.app.accent_orange)
        self.size_display.pack(side="left")

   
    def _maybe_init_surface_once(self, evt=None):
        """Create the RGBA surface the first time we get a real canvas size."""
        if self._img is not None:
            return
        w = max(self.canvas.winfo_width(), 1)
        h = max(self.canvas.winfo_height(), 1)
       
        self._img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        self._draw = ImageDraw.Draw(self._img, "RGBA")
        self._refresh_canvas_image()

    def _refresh_canvas_image(self):
        """Push the PIL image to the Tk canvas."""
        self._img_tk = ImageTk.PhotoImage(self._img)
        if self._img_id is None:
            self._img_id = self.canvas.create_image(0, 0, image=self._img_tk, anchor="nw")
        else:
            self.canvas.itemconfigure(self._img_id, image=self._img_tk)

    def start_draw(self, event):
        self.drawing = True
        if self._img is None:
            self._maybe_init_surface_once()
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        if not self.drawing or self._img is None:
            return
        if self.last_x is not None and self.last_y is not None:
            r, g, b = self._hex_to_rgb(self.brush_color)
            a = int(255 * max(0.0, min(1.0, self.brush_opacity)))
          
            self._draw.line((self.last_x, self.last_y, event.x, event.y),
                            fill=(r, g, b, a), width=self.brush_size)

            self._refresh_canvas_image()


            Pipeline.send_message("draw", [(self.last_x, self.last_y, event.x, event.y),
                            (r, g, b, a), self.brush_size])


        self.last_x, self.last_y = event.x, event.y

    def manual_draw(self, data):
        if self.artboard_mode == False:
            return

        self._draw.line(data[0], data[1], data[2])
        self._refresh_canvas_image()


    def bulk_draw(self, data):
        for i in data:
            self._draw.line(i[0], i[1], i[2])

        self._refresh_canvas_image()


    def stop_draw(self, event):
        self.drawing = False
        self.last_x = None
        self.last_y = None

   
    def change_color(self, color):
        self.brush_color = color

    def update_brush_size(self, value):
        self.brush_size = int(value)
        self.size_display.configure(text=f"{self.brush_size}px")

    def update_brush_opacity(self, value):
        """Slider gives 0..100; store 0.0..1.0 and show %."""
        pct = int(float(value))
        self.brush_opacity = pct / 100.0
        self.opacity_display.configure(text=f"{pct}%")

   
    def clear_canvas(self):
        if self._img is None:
            return
      
        w, h = self._img.size
        self._img = Image.new("RGBA", (w, h), (255, 255, 255, 255))
        self._draw = ImageDraw.Draw(self._img, "RGBA")
        self._refresh_canvas_image()

    def send_mini_message(self):
        message = self.mini_entry.get()
        if message.strip():
            msg_frame = ctk.CTkFrame(self.mini_chat, fg_color=self.app.bg_medium, corner_radius=8)
            msg_frame.pack(fill="x", pady=3, padx=3)
            ctk.CTkLabel(msg_frame, text=message, font=ctk.CTkFont(size=11),
                         text_color=self.app.text_color, wraplength=170,
                         anchor="w").pack(padx=8, pady=5, anchor="w")
            self.mini_entry.delete(0, "end")

    @staticmethod
    def _hex_to_rgb(hx: str):
        """'#rrggbb' -> (r,g,b)"""
        hx = hx.lstrip("#")
        return tuple(int(hx[i:i+2], 16) for i in (0, 2, 4))
