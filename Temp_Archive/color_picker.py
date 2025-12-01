
import customtkinter as ctk #colorpicker wheel, need to fix spacing and color contrast with background 
from tkinter import Canvas
import math
import colorsys
try:
    from PIL import Image, ImageTk
    import numpy as np
    HAS_PIL = True
except ImportError:
    HAS_PIL = False
    print("Warning: PIL/numpy not installed. Using basic color picker.")

class ColorPicker:
    def __init__(self, app, artboard):
        self.app = app
        self.artboard = artboard
        self.picker_window = None
        self.recent_colors = [app.accent_orange, "#000000", "#ffffff"]
        
    
        self.h = 0.0
        self.s = 1.0
        self.v = 1.0
        
    def create_color_bar(self, parent_frame):
        """Create the color selection bar with recent colors and rainbow button"""
     
        self.rainbow_frame = ctk.CTkFrame(
            parent_frame,
            width=35,
            height=35,
            fg_color="transparent"
        )
        self.rainbow_frame.pack(side="left", padx=3)
        
       
        self.rainbow_canvas = Canvas(
            self.rainbow_frame,
            width=35,
            height=35,
            bg=self.app.bg_medium,
            highlightthickness=0
        )
        self.rainbow_canvas.pack()
        
        self.draw_rainbow_circle()
        
        #hover
        self.rainbow_canvas.bind("<Enter>", self.show_picker)
        self.rainbow_canvas.bind("<Leave>", self.schedule_hide)
        
       #recent colors 
        self.recent_btns = []
        for i in range(3):
            color = self.recent_colors[i] if i < len(self.recent_colors) else "#cccccc"
            btn = ctk.CTkButton(
                parent_frame,
                text="",
                width=35,
                height=35,
                corner_radius=17,
                fg_color=color,
                hover_color=color,
                border_width=2,
                border_color=self.app.bg_dark,
                command=lambda c=color, idx=i: self.select_color(c)
            )
            btn.pack(side="left", padx=3)
            self.recent_btns.append(btn)
    
    def draw_rainbow_circle(self):
        """Draw rainbow gradient circle"""
        center = 17.5
        radius = 17.5  #literally still doesnt match other color sizes even if i edit it
        segments = 36
        
        for i in range(segments):
            angle1 = (i * 360 / segments) * math.pi / 180
            angle2 = ((i + 1) * 360 / segments) * math.pi / 180
            
            hue = i / segments
            r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)
            color = f'#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}'
            
            x1 = center + radius * math.cos(angle1)
            y1 = center + radius * math.sin(angle1)
            x2 = center + radius * math.cos(angle2)
            y2 = center + radius * math.sin(angle2)
            
            self.rainbow_canvas.create_polygon(
                center, center, x1, y1, x2, y2,
                fill=color, outline=color
            )
    
    def show_picker(self, event=None):
        """Show color picker popup"""
        if self.picker_window:
            return
        
        if not HAS_PIL:
          
            self.show_basic_picker()
            return
            
        self.picker_window = ctk.CTkToplevel(self.app)
        self.picker_window.title("")
        self.picker_window.configure(fg_color="#55585d")
        self.picker_window.overrideredirect(True)
        
     #appear above raindow picker 
        x = self.rainbow_canvas.winfo_rootx() - 200
        y = self.rainbow_canvas.winfo_rooty() - 520
        self.picker_window.geometry(f"520x500+{x}+{y}")
        
      
        main_frame = ctk.CTkFrame(self.picker_window, fg_color="#55585d")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
     
        self.W, self.H = 400, 400
        self.CX, self.CY = self.W//2, self.H//2
        self.R_OUT = 180
        self.R_IN = 135
        self.DIAMOND_R = 120  
        self.KNOB_R = 8
        
        self.picker_canvas = Canvas(
            main_frame,
            width=self.W,
            height=self.H,
            bg="#3a3a3a",  
            highlightthickness=0
        )
        self.picker_canvas.pack(side="left", padx=5, pady=5)
        
       
        right_panel = ctk.CTkFrame(main_frame, fg_color="#55585d", width=90)
        right_panel.pack(side="left", fill="y", padx=5, pady=5)
        right_panel.pack_propagate(False)
        

        self.color_preview = ctk.CTkLabel(
            right_panel,
            text="",
            width=80,
            height=80,
            fg_color="#ff0000",
            corner_radius=10
        )
        self.color_preview.pack(pady=(10, 15))
        
       #hex
        hex_label = ctk.CTkLabel(
            right_panel,
            text="HEX:",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color="white"
        )
        hex_label.pack(pady=(5, 2))
        
        self.hex_entry = ctk.CTkEntry(
            right_panel,
            width=80,
            height=28,
            fg_color="#4c4f54",
            border_color=self.app.accent_orange,
            border_width=1,
            text_color="white",
            font=ctk.CTkFont(size=10)
        )
        self.hex_entry.pack(pady=2)
        
        apply_btn = ctk.CTkButton(
            right_panel,
            text="Apply",
            width=80,
            height=28,
            fg_color=self.app.accent_orange,
            hover_color="#ff8555",
            font=ctk.CTkFont(size=11, weight="bold"),
            command=self.apply_hex_color
        )
        apply_btn.pack(pady=5)
        
    
        self.build_hsv_picker()
    
        self.picker_canvas.bind("<Button-1>", self.on_picker_click)
        self.picker_canvas.bind("<B1-Motion>", self.on_picker_drag)
        self.picker_window.bind("<Enter>", self.cancel_hide)
        self.picker_window.bind("<Leave>", self.schedule_hide)
        

        self.update_picker_preview()
    
    def build_hsv_picker(self):
        """Build the HSV color picker with hue ring and SV diamond"""
       #hue
        hue_img = self.make_hue_ring()
        self.hue_tk = ImageTk.PhotoImage(hue_img)
        self.picker_canvas.create_image(self.CX, self.CY, image=self.hue_tk)
        
    
        self.render_sv_diamond() #diamond shape
        
        self.h_knob = self.picker_canvas.create_oval(0,0,0,0, width=3, outline="#e6e6e6", fill="#3a3a3a")
        self.sv_knob = self.picker_canvas.create_oval(0,0,0,0, width=3, outline="#e6e6e6", fill="#3a3a3a")
        
        self.place_hue_knob()
        self.place_sv_knob()
    
    def make_hue_ring(self):
        """Create hue ring image"""
        size = (self.W, self.H)
        y, x = np.ogrid[:self.H, :self.W]
        dx = x - self.CX
        dy = y - self.CY
        r = np.sqrt(dx*dx + dy*dy)
        ang = (np.degrees(np.arctan2(dy, dx)) + 360.0) % 360.0
        
        ring_mask = (r <= self.R_OUT) & (r >= self.R_IN)
        
        h = ang / 360.0
        s = np.ones_like(h)
        v = np.ones_like(h)
        
        rgb = np.vectorize(lambda hh, ss, vv: colorsys.hsv_to_rgb(hh, ss, vv))(h, s, v)
        r_ch, g_ch, b_ch = (np.uint8(np.clip(np.array(c)*255, 0, 255)) for c in rgb)
        
        img = np.zeros((self.H, self.W, 4), dtype=np.uint8)
        img[...,0] = r_ch
        img[...,1] = g_ch
        img[...,2] = b_ch
        img[...,3] = (ring_mask * 255).astype(np.uint8)
        
        return Image.fromarray(img, mode="RGBA")
    
    def render_sv_diamond(self):
        """Render SV diamond for current hue"""
        side = int(self.DIAMOND_R * math.sqrt(2))
        sv = np.zeros((side, side, 4), dtype=np.uint8)
        
        xs = np.linspace(0.0, 1.0, side)
        ys = np.linspace(1.0, 0.0, side)  
        S, V = np.meshgrid(xs, ys)
        Hh = np.full_like(S, self.h)
        
        hsv_to_rgb = np.vectorize(lambda hh, ss, vv: colorsys.hsv_to_rgb(hh, ss, vv))
        rr, gg, bb = hsv_to_rgb(Hh, S, V)
        
        sv[...,0] = np.uint8(rr*255)
        sv[...,1] = np.uint8(gg*255)
        sv[...,2] = np.uint8(bb*255)
        sv[...,3] = 255
        
        # Lighten the dark areas (change 0.2 to adjust how much lighter)
        # Uncomment these lines to make blacks less black
      #  min_brightness = 0.2  # 0.0 = pure black, 1.0 = no change
           #     for i in range(3):
           # sv[...,i] = np.uint8(np.clip(sv[...,i] + (255 * min_brightness * (1 - V)), 0, 255))
        
        img = Image.fromarray(sv, mode="RGBA").rotate(45, resample=Image.BICUBIC, expand=True)
        
       
        w, h = img.size
        # Create background with your any color u want(change this!)
        bg_color = (76, 79, 84)  
        mask = Image.new("L", (w, h), 0)
        bg = Image.new("RGBA", (w, h), bg_color + (255,))
        
        mpx = mask.load()
        cx, cy = w//2, h//2
        for yy in range(h):
            for xx in range(w):
                dx, dy = xx - cx, yy - cy
                d = math.hypot(dx, dy)
                a = 255 if d <= self.DIAMOND_R else max(0, int(255 - (d-self.DIAMOND_R)*24))
                mpx[xx, yy] = a
        
        img.putalpha(mask)
        bg.paste(img, (0, 0), img)
        img = bg
        
        self.sv_tk = ImageTk.PhotoImage(img)
        self.sv_img_id = self.picker_canvas.create_image(self.CX, self.CY, image=self.sv_tk)
    
    def place_hue_knob(self):
        """Place hue knob on ring"""
        ang = self.h * 2*math.pi
        r = (self.R_OUT + self.R_IN)/2
        x = self.CX + r*math.cos(ang)
        y = self.CY + r*math.sin(ang)
        self.move_knob(self.h_knob, x, y)
    
    def place_sv_knob(self):
        """Place SV knob on diamond"""
        side = self.DIAMOND_R * math.sqrt(2)
        x_sq = (self.s - 0.5) * side * 2
        y_sq = (0.5 - self.v) * side * 2
        
        cos_a = math.cos(math.pi/4)
        sin_a = math.sin(math.pi/4)
        xr = x_sq*cos_a - y_sq*sin_a
        yr = x_sq*sin_a + y_sq*cos_a
        x = self.CX + xr
        y = self.CY + yr
        self.move_knob(self.sv_knob, x, y)
    
    def move_knob(self, knob, x, y):
        """Move a knob to position"""
        self.picker_canvas.coords(knob, x-self.KNOB_R, y-self.KNOB_R, x+self.KNOB_R, y+self.KNOB_R)
    
    def on_picker_click(self, e):
        """Handle click on picker"""
        self.handle_picker_point(e.x, e.y)
    
    def on_picker_drag(self, e):
        """Handle drag on picker"""
        self.handle_picker_point(e.x, e.y)
    
    def handle_picker_point(self, x, y):
        """Handle interaction with picker"""
        dx, dy = x - self.CX, y - self.CY
        r = math.hypot(dx, dy)
        
        # Hue ring
        if self.R_IN - 14 <= r <= self.R_OUT + 14:
            ang = (math.degrees(math.atan2(dy, dx)) + 360) % 360
            self.h = ang / 360.0
            self.place_hue_knob()
            self.render_sv_diamond()
            self.place_sv_knob()
            self.update_picker_preview()
            return
        
        # SV diamond
        if r <= self.DIAMOND_R * 1.25:
            cos_a = math.cos(math.pi/4)
            sin_a = math.sin(math.pi/4)
            xr = (dx*cos_a + dy*sin_a)
            yr = (-dx*sin_a + dy*cos_a)
            
            side = self.DIAMOND_R * math.sqrt(2)
            if abs(xr) <= side and abs(yr) <= side:
                self.s = 0.5 + xr/(2*side)
                self.v = 0.5 - yr/(2*side)
                self.s = max(0.0, min(1.0, self.s))
                self.v = max(0.0, min(1.0, self.v))
                self.place_sv_knob()
                self.update_picker_preview()
    
    def update_picker_preview(self):
        """Update color preview and hex display"""
        r, g, b = colorsys.hsv_to_rgb(self.h, self.s, self.v)
        rgb = (int(r*255), int(g*255), int(b*255))
        hexv = "#{:02x}{:02x}{:02x}".format(*rgb)
        
        self.color_preview.configure(fg_color=hexv)
        self.hex_entry.delete(0, "end")
        self.hex_entry.insert(0, hexv)
    
    def show_basic_picker(self):
        """Fallback basic picker if PIL not available"""
        pass
    
    def select_color(self, color):
        """Select a color and update recent colors"""
        self.artboard.change_color(color)
        
       
        if color in self.recent_colors:
            self.recent_colors.remove(color)
        self.recent_colors.insert(0, color)
        self.recent_colors = self.recent_colors[:3]
        
        for i in range(len(self.recent_btns)):
            if i < len(self.recent_colors):
                new_color = self.recent_colors[i]
                self.recent_btns[i].configure(fg_color=new_color, hover_color=new_color)
                self.recent_btns[i].configure(command=lambda c=new_color: self.select_color(c))
    
    def apply_hex_color(self):
        """Apply hex color from text input"""
        hex_color = self.hex_entry.get().strip()
        
        if not hex_color.startswith('#'):
            hex_color = '#' + hex_color
        
        if len(hex_color) == 7:
            try:
                int(hex_color[1:], 16)
                self.select_color(hex_color)
                self.hide_picker()
            except ValueError:
                pass
    
    def schedule_hide(self, event=None):
        """Schedule hiding picker"""
        if hasattr(self, '_hide_job'):
            self.app.after_cancel(self._hide_job)
        self._hide_job = self.app.after(300, self.hide_picker)
    
    def cancel_hide(self, event=None):
        """Cancel scheduled hide"""
        if hasattr(self, '_hide_job'):
            self.app.after_cancel(self._hide_job)
    
    def hide_picker(self):
        """Hide the picker window"""
        if self.picker_window:
            self.picker_window.destroy()
            self.picker_window = None