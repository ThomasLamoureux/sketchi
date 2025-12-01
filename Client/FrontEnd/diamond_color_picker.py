# color_picker.py (diamond and gradient color acutally works

import math
import colorsys

import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk


class DiamondColorPicker(ctk.CTkToplevel):
 

    def __init__(self, parent, current_color="#ff00ff", callback=None):
        super().__init__(parent)

        self.callback = callback
        self.current_color = current_color

        #hsv
        self.hue = 300.0    # 0..360
        self.sat = 1.0      # 0..1
        self.val = 1.0      # 0..1
        self._hex_to_hsv(current_color)

        self.title("Color Picker")
        self.geometry("800x520")
        self.configure(fg_color="#2b2b2b")

        self.transient(parent) #middle
        self.grab_set()

        #center on screen
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 400
        y = (self.winfo_screenheight() // 2) - 260
        self.geometry(f"800x520+{x}+{y}")

        #geometry
        self.canvas_size = 420
        self.center = self.canvas_size // 2
        self.hue_outer_radius = self.center - 6
        self.hue_inner_radius = int(self.hue_outer_radius * 0.70)
        self.diamond_half = int(self.hue_inner_radius * 0.95)
        self._sqrt2 = math.sqrt(2)

        # canvas items
        self.picker_image_id = None
        self.hue_handle_id = None
        self.sv_handle_id = None

        self._build_ui()
        self._draw_composite_image()
        self._update_handles_from_hsv()
        self._update_preview_from_hsv()


    def _build_ui(self): #ui implementation 
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        #color picker 
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))

        self.picker_canvas = Canvas(
            left_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#2b2b2b",
            highlightthickness=0
        )
        self.picker_canvas.pack()

        self.picker_canvas.bind("<Button-1>", self._on_canvas_event)
        self.picker_canvas.bind("<B1-Motion>", self._on_canvas_event)

        #controls 
        right_frame = ctk.CTkFrame(main_frame, fg_color="#3c3c3c", corner_radius=18)
        right_frame.pack(side="right", fill="y")

        self.color_preview = ctk.CTkFrame(
            right_frame,
            width=140,
            height=140,
            corner_radius=18,
            fg_color=self.current_color
        )
        self.color_preview.pack(padx=20, pady=24)

        hex_label = ctk.CTkLabel(
            right_frame,
            text="HEX:",
            font=("Segoe UI", 14, "bold")
        )
        hex_label.pack(pady=(10, 4))

        self.hex_entry = ctk.CTkEntry(
            right_frame,
            width=160,
            height=40,
            font=("Segoe UI", 12),
            fg_color="#222222",
            border_color="#ff6b35",
            border_width=2
        )
        self.hex_entry.pack(padx=20)
        self.hex_entry.insert(0, self.current_color)
        self.hex_entry.bind("<Return>", lambda e: self._apply_hex_from_entry())

        apply_btn = ctk.CTkButton(
            right_frame,
            text="Apply",
            width=160,
            height=42,
            font=("Segoe UI", 14, "bold"),
            fg_color="#ff6b35",
            hover_color="#ff854f",
            corner_radius=10,
            command=self._apply_color_and_close
        )
        apply_btn.pack(pady=26)



    def _draw_composite_image(self): #drawing componment 
        
        size = self.canvas_size
        c = self.center
        outer = self.hue_outer_radius
        inner = self.hue_inner_radius
        half = self.diamond_half
        sqrt2 = self._sqrt2

        img = Image.new("RGB", (size, size), "#3b3b3b")
        px = img.load()

        for y in range(size): #huge ring, help me 
            dy = y - c 
            for x in range(size):
                dx = x - c
                dist = math.hypot(dx, dy)

                if inner <= dist <= outer:
                    angle = math.atan2(dy, dx)
                    hue = (angle + math.pi) / (2 * math.pi)  # 0..1
                    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    px[x, y] = (int(r * 255), int(g * 255), int(b * 255))

    
        h = self.hue / 360.0 #saturation 

        for y in range(size):
            y0 = y - c
            for x in range(size):
                x0 = x - c

                xr = (x0 + y0) / sqrt2
                yr = (y0 - x0) / sqrt2 #ui diamond roation 

                if -half <= xr <= half and -half <= yr <= half:
                   
                    s = (xr + half) / (2 * half)        
                    v = 1.0 - (yr + half) / (2 * half)   
                    s = max(0.0, min(1.0, s))
                    v = max(0.0, min(1.0, v))

                    r, g, b = colorsys.hsv_to_rgb(h, s, v)
                    px[x, y] = (int(r * 255), int(g * 255), int(b * 255))

        self.composite_image = ImageTk.PhotoImage(img)

        if self.picker_image_id is None:
            self.picker_image_id = self.picker_canvas.create_image(
                0, 0, anchor="nw", image=self.composite_image
            )
        else:
            self.picker_canvas.itemconfig(self.picker_image_id, image=self.composite_image)


    def _update_handles_from_hsv(self):
        """Place hue-circle handle and SV diamond handle based on hsv values."""
        # hue handle on ring
        angle = (self.hue / 360.0) * (2 * math.pi) - math.pi
        r = (self.hue_inner_radius + self.hue_outer_radius) / 2
        hx = self.center + r * math.cos(angle)
        hy = self.center + r * math.sin(angle)
        self._draw_hue_handle(hx, hy)

        half = self.diamond_half
        sqrt2 = self._sqrt2

        xr = self.sat * 2 * half - half
        yr = (1.0 - self.val) * 2 * half - half

        x0 = (xr - yr) / sqrt2
        y0 = (xr + yr) / sqrt2

        sx = self.center + x0
        sy = self.center + y0
        self._draw_sv_handle(sx, sy)

    def _draw_hue_handle(self, x, y):
        r = 9
        if self.hue_handle_id is None:
            self.hue_handle_id = self.picker_canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline="#ffffff", width=2
            )
        else:
            self.picker_canvas.coords(
                self.hue_handle_id, x - r, y - r, x + r, y + r
            )

    def _draw_sv_handle(self, x, y):
        r = 9
        if self.sv_handle_id is None:
            self.sv_handle_id = self.picker_canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline="#ffffff", width=2
            )
        else:
            self.picker_canvas.coords(
                self.sv_handle_id, x - r, y - r, x + r, y + r
            )

    def _on_canvas_event(self, event):
        x, y = event.x, event.y
        dx = x - self.center
        dy = y - self.center
        dist = math.hypot(dx, dy)

        #huge ring
        if self.hue_inner_radius <= dist <= self.hue_outer_radius:
            angle = math.atan2(dy, dx)
            self.hue = ((angle + math.pi) / (2 * math.pi)) * 360.0
            self._draw_hue_handle(x, y)
        
            self._draw_composite_image()
            self._update_handles_from_hsv()
            self._update_color_from_hsv()
            return

        #diamond
        if self._point_in_diamond(x, y):
            self._update_sv_from_point(x, y)
            self._draw_sv_handle(x, y)
            self._update_color_from_hsv()

    def _point_in_diamond(self, x, y):
        """Check whether (x,y) lies inside the diamond region."""
        x0 = x - self.center
        y0 = y - self.center

        xr = (x0 + y0) / self._sqrt2
        yr = (y0 - x0) / self._sqrt2
        half = self.diamond_half

        return -half <= xr <= half and -half <= yr <= half

    def _update_sv_from_point(self, x, y):
        """Convert a canvas point inside the diamond into S and V values."""
        x0 = x - self.center
        y0 = y - self.center

        xr = (x0 + y0) / self._sqrt2
        yr = (y0 - x0) / self._sqrt2
        half = self.diamond_half

        s = (xr + half) / (2 * half)
        v = 1.0 - (yr + half) / (2 * half)

        self.sat = max(0.0, min(1.0, s))
        self.val = max(0.0, min(1.0, v))


    def _update_color_from_hsv(self): #color hex
        h = self.hue / 360.0
        r, g, b = colorsys.hsv_to_rgb(h, self.sat, self.val)
        self.current_color = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
        self._update_preview_from_hsv()

    def _update_preview_from_hsv(self):
        self.color_preview.configure(fg_color=self.current_color)
        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, self.current_color)

    def _hex_to_hsv(self, hex_color: str):
        """Initialize hue, sat, val from a #rrggbb string."""
        try:
            hex_color = hex_color.lstrip("#")
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            h, s, v = colorsys.rgb_to_hsv(r, g, b)
            self.hue = h * 360.0
            self.sat = s
            self.val = v
        except Exception:
            self.hue, self.sat, self.val = 300.0, 1.0, 1.0

    def _apply_hex_from_entry(self):
        value = self.hex_entry.get().strip()
        if not (value.startswith("#") and len(value) == 7):
            return
        try:
            int(value[1:], 16)
        except ValueError:
            return

        self.current_color = value
        self._hex_to_hsv(value)
        self._draw_composite_image()
        self._update_handles_from_hsv()
        self._update_preview_from_hsv()



    def _apply_color_and_close(self):
        if self.callback:
            self.callback(self.current_color)
        self.destroy()


# quick demo
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    root = ctk.CTk()
    root.geometry("300x200")

    def open_picker():
        def on_color(c):
            print("Chosen:", c)
        DiamondColorPicker(root, "#ff00ff", on_color)

    btn = ctk.CTkButton(root, text="Open Color Picker", command=open_picker)
    btn.pack(pady=60)
    root.mainloop()





