# Main.py - Sketchi Application Entry Point (With Animated Logo)
import asyncio
import customtkinter as ctk
from tkinter import Canvas, colorchooser
from PIL import Image, ImageTk, ImageDraw
import cv2
from threading import Thread
import os
import math

import Cache.Cache as Cache
import ServerCommunication.message_sender as MessageSender
import ServerCommunication.Login as Login
import ServerCommunication.Client as Client

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



loop = None


# ============================================================================
# ANIMATED LOGO WIDGET
# ============================================================================
class AnimatedLogo(ctk.CTkLabel):
    def __init__(self, parent, video_path, logo_image_path=None, size=100, **kwargs):
        super().__init__(parent, text="", **kwargs)
        
        self.size = size
        self.video_path = video_path
        self.logo_image_path = logo_image_path
        self.is_playing = False
        self.video_frames = []
        self.current_frame = 0
        self.static_logo = None
        self.artboard = None
        
        # Load static logo or create default
        self.load_static_logo()
        
        # Load video frames
        asyncio.create_task(self.load_video_frames())
        
        # Show static logo initially
        self.show_static_logo()
        
        # Bind hover events
        self.bind("<Enter>", self.on_hover_enter)
        self.bind("<Leave>", self.on_hover_leave)
        
        self.configure(cursor="hand2")
        
    def load_static_logo(self):
        """Load static logo image or create a default one"""
        if self.logo_image_path and os.path.exists(self.logo_image_path):
            # Load user-provided logo
            img = Image.open(self.logo_image_path)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Maintain aspect ratio
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height
            new_height = self.size
            new_width = int(new_height * aspect_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            self.static_logo = ImageTk.PhotoImage(img)
            
            # Set transparent background
            self.configure(fg_color="transparent")
        else:
            # Create a default circular logo
            img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))

            draw = ImageDraw.Draw(img)
            draw.ellipse([0, 0, self.size-1, self.size-1], fill='#ff6b35', outline='#ff6b35')
            self.static_logo = ImageTk.PhotoImage(img)
            self.configure(fg_color="transparent")
    
    async def load_video_frames(self):
        """Load all frames from the video"""
        if not os.path.exists(self.video_path):
            print(f"Video not found: {self.video_path}")
            return
            
        cap = cv2.VideoCapture(self.video_path)
        
        # Get video dimensions for aspect ratio
        video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        aspect_ratio = video_width / video_height
        new_height = self.size
        new_width = int(new_height * aspect_ratio)
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            # Convert BGR to RGBA for transparency
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            
            # Resize frame maintaining aspect ratio
            frame = cv2.resize(frame, (new_width, new_height))
            
            # Convert to PIL Image
            img = Image.fromarray(frame)
            
            # Convert to PhotoImage
            photo = ImageTk.PhotoImage(img)
            
            self.video_frames.append(photo)
        
        cap.release()
        print(f"Loaded {len(self.video_frames)} frames from video")
    
    def show_static_logo(self):
        """Display the static logo"""
        self.configure(image=self.static_logo)
        self.image = self.static_logo  # Keep reference
    
    def on_hover_enter(self, event):
        """Start animation on hover"""
        if len(self.video_frames) > 0:
            self.is_playing = True
            self.current_frame = 0
            self.play_animation()
    
    def on_hover_leave(self, event):
        """Stop animation and return to static logo"""
        self.is_playing = False
        self.after(100, self.show_static_logo)  # Small delay before showing static
    
    def play_animation(self):
        """Play the video frames in sequence"""
        if not self.is_playing or len(self.video_frames) == 0:
            return
        
        # Show current frame
        self.configure(image=self.video_frames[self.current_frame])
        self.image = self.video_frames[self.current_frame]  # Keep reference
        
        # Move to next frame
        self.current_frame = (self.current_frame + 1) % len(self.video_frames)
        
        # Schedule next frame (adjust delay for speed - 30ms ≈ 33 fps)
        self.after(30, self.play_animation)

# ============================================================================
# COLOR PICKER WINDOW (CIRCULAR GRADIENT)
# ============================================================================
class ColorPickerWindow(ctk.CTkToplevel):
    def __init__(self, parent, initial_color, callback):
        super().__init__(parent)
        
        self.callback = callback
        self.selected_color = initial_color
        
        self.title("Color Picker")
        self.geometry("600x500")
        self.configure(fg_color="#363636")
        
        self.transient(parent)
        self.grab_set()
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 300
        y = (self.winfo_screenheight() // 2) - 250
        self.geometry(f"600x500+{x}+{y}")
        
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Color wheel
        left_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self.picker_canvas = Canvas(
            left_frame,
            width=400,
            height=400,
            bg="#363636",
            highlightthickness=0
        )
        self.picker_canvas.pack()
        
        # Draw circular gradient
        self.draw_color_gradient()
        self.picker_canvas.bind("<Button-1>", self.on_color_click)
        self.picker_canvas.bind("<B1-Motion>", self.on_color_click)
        
        # Right side - Controls
        right_frame = ctk.CTkFrame(main_frame, fg_color="#2b2b2b", corner_radius=15)
        right_frame.pack(side="right", fill="y")
        
        # Color preview
        self.color_preview = ctk.CTkFrame(
            right_frame,
            width=120,
            height=120,
            corner_radius=15,
            fg_color=self.selected_color
        )
        self.color_preview.pack(padx=20, pady=20)
        
        # HEX label
        hex_label = ctk.CTkLabel(
            right_frame,
            text="HEX:",
            font=("Segoe UI", 14, "bold")
        )
        hex_label.pack(pady=(10, 5))
        
        # HEX entry
        self.hex_entry = ctk.CTkEntry(
            right_frame,
            width=140,
            height=40,
            font=("Segoe UI", 12),
            fg_color="#363636",
            border_color="#ff6b35",
            border_width=2
        )
        self.hex_entry.pack(padx=20)
        self.hex_entry.insert(0, self.selected_color)
        self.hex_entry.bind("<Return>", lambda e: self.apply_hex_color())
        
        # Apply button
        apply_btn = ctk.CTkButton(
            right_frame,
            text="Apply",
            width=140,
            height=40,
            font=("Segoe UI", 14, "bold"),
            fg_color="#ff6b35",
            hover_color="#ff8555",
            corner_radius=10,
            command=self.apply_color
        )
        apply_btn.pack(pady=20)
    
    def draw_color_gradient(self):
        """Draw CLEAN color picker - proper HSV color space"""
        size = 400
        center = size // 2
        radius = center - 5
        
        img = Image.new('RGB', (size, size), '#505050')
        draw = ImageDraw.Draw(img)
        
        # Draw EVERY pixel with proper HSV color space
        for y in range(size):
            for x in range(size):
                dx = x - center
                dy = y - center
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Only draw inside the circle
                if distance <= radius:
                    # Calculate HUE from angle (0-360 around the circle)
                    angle = math.atan2(dy, dx)
                    hue = int((angle + math.pi) / (2 * math.pi) * 360)
                    
                    # Calculate SATURATION from distance from center
                    # Center = 0% saturation (white)
                    # Edge = 100% saturation (full color)
                    saturation = int((distance / radius) * 100)
                    
                    # Calculate VALUE (brightness) from vertical position
                    # Top = 100% (bright)
                    # Bottom = 0% (dark/black)
                    y_from_top = y - (center - radius)
                    value = int(100 - (y_from_top / (radius * 2)) * 100)
                    value = max(0, min(100, value))
                    
                    # Convert HSV to RGB
                    color = self.hsv_to_rgb(hue, saturation, value)
                    draw.point((x, y), fill=color)
        
        self.gradient_photo = ImageTk.PhotoImage(img)
        self.picker_canvas.create_image(0, 0, anchor="nw", image=self.gradient_photo)
    
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        
        if s == 0:
            r = g = b = int(v * 255)
            return (r, g, b)
        
        i = int(h * 6)
        f = (h * 6) - i
        p = v * (1 - s)
        q = v * (1 - f * s)
        t = v * (1 - (1 - f) * s)
        i = i % 6
        
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def on_color_click(self, event):
        """Handle color selection from gradient"""
        x, y = event.x, event.y
        center = 200
        dx = x - center
        dy = y - center
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance <= center:
            angle = math.atan2(dy, dx)
            hue = int((angle + math.pi) / (2 * math.pi) * 360)
            saturation = int((distance / center) * 100)
            value = 100
            
            r, g, b = self.hsv_to_rgb(hue, saturation, value)
            hex_color = f"#{r:02x}{g:02x}{b:02x}"
            
            self.selected_color = hex_color
            self.color_preview.configure(fg_color=hex_color)
            self.hex_entry.delete(0, "end")
            self.hex_entry.insert(0, hex_color)
    
    def apply_hex_color(self):
        """Apply color from HEX entry"""
        hex_value = self.hex_entry.get().strip()
        if hex_value.startswith('#') and len(hex_value) == 7:
            try:
                int(hex_value[1:], 16)
                self.selected_color = hex_value
                self.color_preview.configure(fg_color=hex_value)
            except ValueError:
                pass
        
    def apply_color(self):
        self.callback(self.selected_color)
        self.destroy()

# ============================================================================
# ARTBOARD
# ============================================================================
class SketchiArtboard(ctk.CTkFrame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.app = app
        
        self.current_color = "#ff6b35"
        self.brush_size = 3
        self.opacity = 100
        self.recent_colors = ["#ff6b35", "#000000", "#ffffff"]
        self.is_drawing = False
        self.last_x = None
        self.last_y = None
        
        #self.setup_ui()
        self.project_join_gui()


    def created_art_project(self, access_code):
        Cache.add("art_project_access_code", access_code)
        self.app.channels_frame.access_code.configure(text=f"Access Code:\n{access_code}")
        self.setup_ui()

    def join_art_project_response(self, success, reason=None):
        if success:
            self.setup_ui()
        else:
            self.lbl_message.configure(text=f"Join Failed: {reason}")


    def project_join_gui(self):
        def request_art_project(owner, code):
            Client.send_message(
                payload={
                    "msg_type": "join_art_project",
                    "owner": owner,
                    "code": code
                }
            )
        def create_art_project():
            payload = {
                "msg_type": "create_art_project",
            }

            Client.send_message(payload)

            
        frame = ctk.CTkFrame(self, width=340, height=360, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        lbl_title = ctk.CTkLabel(frame, text="Join Art Project", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=15)

        # Username Entry
        self.entry_username = ctk.CTkEntry(frame, placeholder_text="Owner Username")
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Password Entry
        self.entry_password = ctk.CTkEntry(frame, placeholder_text="Invite Code")
        self.entry_password.pack(pady=10, padx=20, fill="x")

        # Message Label
        self.lbl_message = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_message.pack(pady=5)

        # Login Button
        btn_action = ctk.CTkButton(
            frame,
            text="Join",
            command=lambda: request_art_project(self.entry_username.get().strip(), self.entry_password.get().strip())
        )
        btn_action.pack(pady=10, padx=10, fill="x")


        btn_switch = ctk.CTkButton(
            frame,
            text="Create New Project",
            command=create_art_project,
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#E3F2FD",
            font=ctk.CTkFont(size=12, underline=True)
        )
        btn_switch.pack(pady=5)
        
    def setup_ui(self):
        canvas_container = ctk.CTkFrame(self, fg_color="white", corner_radius=10)
        canvas_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas = Canvas(
            canvas_container,
            bg="white",
            highlightthickness=0,
            cursor="crosshair"
        )
        self.canvas.pack(fill="both", expand=True)
        
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
        self.create_tools()
        
    def create_tools(self):
        tools_frame = ctk.CTkFrame(
            self,
            height=120,
            fg_color=self.app.bg_medium,
            corner_radius=10
        )
        tools_frame.pack(fill="x", padx=20, pady=(0, 20))
        tools_frame.pack_propagate(False)
        
        color_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
        color_frame.pack(side="left", padx=15)
        
        self.color_wheel = ctk.CTkButton(
            color_frame,
            text="◆",
            width=40,
            height=40,
            corner_radius=8,
            fg_color=self.current_color,
            hover_color=self.current_color,
            font=("Segoe UI", 24),
            text_color="#ffffff",
            command=self.open_color_picker
        )
        self.color_wheel.pack(side="left", padx=4)
        
        self.color_buttons = []
        for i, color in enumerate(self.recent_colors):
            btn = ctk.CTkButton(
                color_frame,
                text="",
                width=35,
                height=35,
                corner_radius=17,
                fg_color=color,
                hover_color=color,
                border_width=2 if color == self.current_color else 0,
                border_color=self.app.accent_orange,
                command=lambda c=color: self.select_color(c)
            )
            btn.pack(side="left", padx=4)
            self.color_buttons.append(btn)
            
        sliders_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
        sliders_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        """opacity_container = ctk.CTkFrame(sliders_frame, fg_color="transparent")
        opacity_container.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            opacity_container,
            text="Opacity:",
            font=("Segoe UI", 12, "bold"),
            width=80,
            anchor="w"
        ).pack(side="left")
        
        self.opacity_slider = ctk.CTkSlider(
            opacity_container,
            from_=0,
            to=100,
            number_of_steps=100,
            command=self.update_opacity
        )
        self.opacity_slider.set(100)
        self.opacity_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        self.opacity_label = ctk.CTkLabel(
            opacity_container,
            text="100%",
            font=("Segoe UI", 12, "bold"),
            text_color=self.app.accent_orange,
            width=50,
            anchor="e"
        )
        self.opacity_label.pack(side="left")
        """
        brush_container = ctk.CTkFrame(sliders_frame, fg_color="transparent")
        brush_container.pack(fill="x", pady=5)
        
        ctk.CTkLabel(
            brush_container,
            text="Brush Size:",
            font=("Segoe UI", 12, "bold"),
            width=80,
            anchor="w"
        ).pack(side="left")
        
        self.brush_slider = ctk.CTkSlider(
            brush_container,
            from_=1,
            to=100,
            number_of_steps=99,
            command=self.update_brush_size
        )
        self.brush_slider.set(3)
        self.brush_slider.pack(side="left", fill="x", expand=True, padx=10)
        
        self.brush_label = ctk.CTkLabel(
            brush_container,
            text="3px",
            font=("Segoe UI", 12, "bold"),
            text_color=self.app.accent_orange,
            width=50,
            anchor="e"
        )
        self.brush_label.pack(side="left")
        
        buttons_frame = ctk.CTkFrame(tools_frame, fg_color="transparent")
        buttons_frame.pack(side="left", padx=15)
        
        clear_btn = ctk.CTkButton(
            buttons_frame,
            text="Clear",
            width=80,
            height=32,
            corner_radius=16,
            fg_color="#cc0000",
            hover_color="#ff0000",
            font=("Segoe UI", 12, "bold"),
            command=self.clear_canvas
        )
        clear_btn.pack(pady=2)
        
        eraser_btn = ctk.CTkButton(
            buttons_frame,
            text="Eraser",
            width=80,
            height=32,
            corner_radius=16,
            fg_color=self.app.bg_light,
            hover_color=self.app.bg_dark,
            font=("Segoe UI", 12, "bold"),
            command=self.set_eraser
        )
        eraser_btn.pack(pady=2)
        
    def start_drawing(self, event):
        self.is_drawing = True
        self.last_x = event.x
        self.last_y = event.y
        
    def draw(self, event):
        if self.is_drawing and self.last_x and self.last_y:
            drawing_data = {
                "line": (self.last_x, self.last_y, event.x, event.y),
                "fill": self.current_color,
                "brush_size": self.brush_size
            }
            self.canvas.create_line(
                (self.last_x, self.last_y, event.x, event.y),
                fill=self.current_color,
                width=self.brush_size,
                capstyle="round",
                smooth=True
            )
            
            self.last_x = event.x
            self.last_y = event.y

            payload = {
                "msg_type": "draw",
                "drawing_data": drawing_data
            }
            Client.send_message(payload)
            
    def stop_drawing(self, event):
        self.is_drawing = False
        self.last_x = None
        self.last_y = None

    def manual_draw(self, drawing_data):
        line = drawing_data["line"]
        fill = drawing_data["fill"]
        brush_size = drawing_data["brush_size"]
        
        self.canvas.create_line(
            line,
            fill=fill,
            width=brush_size,
            capstyle="round",
            smooth=True
        )

    def bulk_draw(self, drawings):
        for drawing_data in drawings:
            self.manual_draw(drawing_data)
        
    def select_color(self, color):
        self.current_color = color
        self.update_color_buttons()
        
    def update_color_buttons(self):
        for btn in self.color_buttons:
            color = btn.cget("fg_color")
            if color == self.current_color:
                btn.configure(border_width=2, border_color=self.app.accent_orange)
            else:
                btn.configure(border_width=0)
                
    def update_opacity(self, value):
        self.opacity = int(value)
        self.opacity_label.configure(text=f"{self.opacity}%")
        
    def update_brush_size(self, value):
        self.brush_size = int(value)
        self.brush_label.configure(text=f"{self.brush_size}px")
        
    def clear_canvas(self):
        self.canvas.delete("all")
        
    def set_eraser(self):
        self.select_color("#ffffff")
        
    def open_color_picker(self):
        picker = ColorPickerWindow(self, self.current_color, self.on_color_selected)
        
    def on_color_selected(self, color):
        self.current_color = color
        
        # Update diamond button color
        self.color_wheel.configure(fg_color=color, hover_color=color)
        
        if color not in self.recent_colors:
            self.recent_colors = [color] + self.recent_colors[:2]
            
            for i, btn in enumerate(self.color_buttons):
                btn.configure(fg_color=self.recent_colors[i])
                btn.configure(command=lambda c=self.recent_colors[i]: self.select_color(c))
                
        self.update_color_buttons()

# ============================================================================
# CHANNELS FRAME
# ============================================================================
class ChannelsFrame(ctk.CTkFrame):
    def __init__(self, parent, app, **kwargs):
        super().__init__(parent, width=240, **kwargs)
        self.app = app
        self.pack_propagate(False)
        
        self.channels = ["#mainchat", "#artchat", "#artsharing", "#artcontest"]
        self.mini_messages = []
        
        self.current_mode = "channels"
        self.show_channels()
        
    def show_channels(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        header = ctk.CTkFrame(self, height=140, fg_color=self.app.bg_medium)
        header.pack(fill="x", pady=(0, 1))
        header.pack_propagate(False)
        
        server_name = ctk.CTkLabel(
            header,
            text="Server Name",
            font=("Segoe UI", 18, "bold")
        )
        server_name.pack(padx=20, pady=20, anchor="w")
        
        channels_container = ctk.CTkFrame(self, fg_color="transparent")
        channels_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        channels_label = ctk.CTkLabel(
            channels_container,
            text="Channels",
            font=("Segoe UI", 12, "bold"),
            text_color="#888888"
        )
        channels_label.pack(anchor="w", pady=(0, 10))
        
        for channel in self.channels:
            is_active = channel == self.app.active_channel
            
            channel_btn = ctk.CTkButton(
                channels_container,
                text=channel,
                fg_color=self.app.bg_light if is_active else "transparent",
                text_color=self.app.accent_orange if is_active else "#cccccc",
                hover_color=self.app.bg_light,
                corner_radius=8,
                anchor="w",
                command=lambda ch=channel: self.select_channel(ch)
            )
            channel_btn.pack(fill="x", pady=2)
            
    def select_channel(self, channel):
        self.app.load_channel(channel)
        self.show_channels()
        
    def show_mini_chat(self):
        for widget in self.winfo_children():
            widget.destroy()
            
        self.configure(width=200)
        
        details_frame = ctk.CTkFrame(self, fg_color="transparent", height=100)
        details_frame.pack(side="top", expand=True)


        self.access_code = ctk.CTkLabel(
            details_frame,
            text=f"Access Code:\n{Cache.get('art_project_access_code')}",
            font=("Segoe UI", 14, "bold"),
            justify="center"
        )
        self.access_code.pack(pady=10)

        self.active_artists_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.active_artists_frame.pack(fill="both", expand=True, padx=10, pady=10)

        header = ctk.CTkFrame(self, height=50, fg_color=self.app.bg_medium)
        header.pack(fill="x", pady=(0, 1))
        header.pack_propagate(False)


        

        title = ctk.CTkLabel(
            header,
            text="Quick Chat",
            font=("Segoe UI", 14, "bold")
        )
        title.pack(padx=15, pady=15)
        


        self.mini_messages_frame = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.mini_messages_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for msg in self.mini_messages:
            msg_frame = ctk.CTkFrame(
                self.mini_messages_frame,
                fg_color=self.app.bg_light,
                corner_radius=8
            )
            msg_frame.pack(fill="x", pady=2)
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=msg,
                font=("Segoe UI", 11),
                wraplength=160
            )
            msg_label.pack(padx=8, pady=8)
            
        input_frame = ctk.CTkFrame(self, height=55, fg_color=self.app.bg_medium)
        input_frame.pack(fill="x", pady=(1, 0))
        input_frame.pack_propagate(False)
        
        self.mini_entry = ctk.CTkEntry(
            input_frame,
            height=35,
            corner_radius=17,
            border_width=1,
            border_color=self.app.accent_orange,
            fg_color=self.app.bg_light,
            placeholder_text="Message"
        )
        self.mini_entry.pack(padx=10, pady=10, fill="x")
        self.mini_entry.bind("<Return>", self.send_mini_message)
        
    def send_mini_message(self, event=None):
        text = self.mini_entry.get().strip()
        if text:
            self.write_mini_message(text)
            payload = {
                "msg_type": "project_message",
                "text": text
            }
            Client.send_message(payload)
    
    def write_mini_message(self, text):
        if (self.current_mode != "mini_chat"):
            return
        self.mini_messages.append(text)
        
        msg_frame = ctk.CTkFrame(
            self.mini_messages_frame,
            fg_color=self.app.bg_light,
            corner_radius=8
        )
        msg_frame.pack(fill="x", pady=2)
        
        msg_label = ctk.CTkLabel(
            msg_frame,
            text=text,
            font=("Segoe UI", 11),
            wraplength=160
        )
        msg_label.pack(padx=8, pady=8)
        
        self.mini_entry.delete(0, "end")
            
    def switch_to_mini_chat(self):
        self.current_mode = "mini_chat"
        self.show_mini_chat()
        
    def switch_to_channels(self):
        self.current_mode = "channels"
        self.configure(width=240)
        self.show_channels()

# ============================================================================
# MAIN APP
# ============================================================================
class SketchiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sketchi")
        self.geometry("1200x700")
        self.configure(fg_color="#1e1e1e")
        
        self.bg_dark = "#1e1e1e"
        self.bg_medium = "#2b2b2b"
        self.bg_light = "#363636"
        self.accent_orange = "#ff6b35"
        
        self.current_view = "chat"
        self.sidebar_mode = "servers"
        self.active_channel = "#mainchat"
        
        # Paths for logo and animation (same folder as Main.py)
        self.logo_image_path = "Resources/sketchi_logo.png"
        self.animation_video_path = "Resources/loading_screen.mp4"
        
        self.friends = [
            {"name": "Thomas", "status": "online"},
            {"name": "Luke", "status": "online"},
            {"name": "Bridget", "status": "away"},
            {"name": "Eddie", "status": "offline"},
            {"name": "Tim", "status": "online"}
        ]
        
        self.messages = []
        
        self.connect_gui()


    def clear_gui(self):
        for widget in self.winfo_children():
            widget.destroy()
        


    def complete_login(self):
        self.setup_ui()


    def failed_login(self):
        print("failed login")
        self.lbl_message.configure(text="Invalid username or password.", text_color="red")

    def sign_up_complete(self, verification_required):
        if verification_required:
            print("verification required")
            self.verification_gui()
        else:
            print("signup complete")
            self.complete_login()


    def failed_signup(self):
        print("failed signup")
        self.lbl_message.configure(text="Username already exists.", text_color="red")


    def failed_connection(self):
        print("failed connection")
        self.lbl_message.configure(text="Failed to connect.", text_color="red")
    

    def success_connection(self):
        print("successful connection")
        self.login_gui()

    
    def incorrect_verification(self):
        print("incorrect verification")
        self.lbl_message.configure(text="Incorrect verification code.", text_color="red")

    def successful_verification(self):
        print("successful verification")
        self.complete_login()


    def verification_gui(self):
        self.delete_this_frame.pack_forget()
        def verify_code(code):
            print(code)
            if not code:
                self.lbl_message.configure(text="Please enter the verification code.", text_color="red")
                return

            Login.verify_code(code)
        
        frame = ctk.CTkFrame(self, width=340, height=240, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")



        # Title
        lbl_title = ctk.CTkLabel(frame, text="Email Verification", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=15)
        # Info Label
        lbl_info = ctk.CTkLabel(frame, text="A verification code has been sent to your email. Please enter it below to activate your account.", 
                                wraplength=200, font=ctk.CTkFont(size=12))
        lbl_info.pack(pady=(10, 0), padx=20)
        # Code Entry
        self.entry_code = ctk.CTkEntry(frame, placeholder_text="XXXXXX") 
        self.entry_code.pack(pady=10, padx=20, fill="x")
        # Message Label
        self.lbl_message = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_message.pack(pady=5)
        # Verify Button
        btn_verify = ctk.CTkButton(frame, text="Verify", command=lambda: verify_code(self.entry_code.get().strip()))
        btn_verify.pack(pady=10, padx=40, fill="x")




    def login_gui(self):
        def login(username, password):
            if not username or not password:
                self.lbl_message.configure(text="Please fill in all fields.", text_color="red")
                return



            Login.validate_credentials(username, password)

            

        def sign_up(email, username, password):

            if not email or not username or not password:
                self.lbl_message.configure(text="Please fill in all fields.", text_color="red")
                return


            Login.sign_up(email, username, password)


        def switch_to_signup():
            btn_action.configure(text="Sign Up", command=lambda: sign_up(self.entry_email.get().strip(), self.entry_username.get().strip(), self.entry_password.get().strip()))
            lbl_switch.configure(text="Already have an account?")
            btn_switch.configure(text="Login", command=switch_to_login)
            self.lbl_message.configure(text="")
            self.entry_email.pack(fill="x")
            btn_action.configure(fg_color="#ff6b35", hover_color="#d04918")

        def switch_to_login():
            btn_action.configure(text="Login", command=lambda: login(self.entry_username.get().strip(), self.entry_password.get().strip()))
            lbl_switch.configure(text="Don't have an account?")
            btn_switch.configure(text="Sign Up", command=switch_to_signup)
            self.entry_email.pack_forget()
            btn_action.configure(fg_color="#2196F3", hover_color="#0A599A")


            
        frame = ctk.CTkFrame(self, width=340, height=360, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")
        self.delete_this_frame = frame
        # Title
        lbl_title = ctk.CTkLabel(frame, text="Sketchi", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=15)

        # Email Entry
        slot = ctk.CTkFrame(frame, fg_color="transparent")
        self.entry_email = ctk.CTkEntry(slot, placeholder_text="Email")
        self.entry_email.pack(fill="x")
        self.entry_email.pack_forget()
        slot.pack(pady=10, padx=20, fill="x")

        # Username Entry
        self.entry_username = ctk.CTkEntry(frame, placeholder_text="Username")
        self.entry_username.pack(pady=10, padx=20, fill="x")

        # Password Entry
        self.entry_password = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=10, padx=20, fill="x")

        # Message Label
        self.lbl_message = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_message.pack(pady=5)

        # Login Button
        btn_action = ctk.CTkButton(
            frame,
            text="Login",
            command=lambda: login(self.entry_username.get().strip(), self.entry_password.get().strip())
        )
        btn_action.pack(pady=10, padx=40, fill="x")

        # Switch to Sign Up
        lbl_switch = ctk.CTkLabel(frame, text="Don't have an account?", font=ctk.CTkFont(size=12))
        lbl_switch.pack(pady=(10, 0))


        btn_switch = ctk.CTkButton(
            frame,
            text="Sign Up",
            command=switch_to_signup,
            fg_color="transparent",
            text_color="#2196F3",
            hover_color="#E3F2FD",
            font=ctk.CTkFont(size=12, underline=True)
        )
        btn_switch.pack(pady=5)
        
    
    def connect(self, entry):
        try:
            global loop
            host = entry.split(":")[0]
            port = int(entry.split(":")[1])


            Client.send_connection_request(host, port)
        except Exception as err:
            print(err)
            self.lbl_message.configure(text="Please enter a valid address.", text_color="red")
            return




    def connect_gui(self):

        frame = ctk.CTkFrame(self, corner_radius=10, width=300, height=250)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        lbl_title = ctk.CTkLabel(frame, text="Enter server IP and port", font=ctk.CTkFont(size=14, weight="bold"))
        lbl_title.pack(pady=(15, 10))

        # IP Entry
        self.entry_ip = ctk.CTkEntry(frame, placeholder_text="Server IP (e.g., 192.168.0.10:5000)")
        self.entry_ip.pack(pady=10, padx=20, fill="x")

        # Message Label
        self.lbl_message = ctk.CTkLabel(frame, text="", text_color="red")
        self.lbl_message.pack(pady=5)

        # Action Button
        btn_action = ctk.CTkButton(
            frame,
            text="Connect",
            command=lambda: self.connect(self.entry_ip.get().strip())
        )
        btn_action.pack(pady=10, padx=40, fill="x")
    
        
    def create_layout(self):
        self.server_frame = ctk.CTkFrame( #server reizing 
            self, 
            width=80, 
            fg_color=self.bg_dark,
            corner_radius=0
        )
        self.server_frame.pack(side="left", fill="y", padx=0, pady=0)
        
        self.servers_label = ctk.CTkLabel( #clicking (implement hover) 
            self.server_frame,
            text="Servers",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.text_color,
            cursor="hand2"
        )
        self.servers_label.pack(pady=(15, 10), padx=10)
        self.servers_label.bind("<Button-1>", self.functionality.toggle_sidebar_mode)
        
        self.icon_container = ctk.CTkFrame(
            self.server_frame,
            fg_color=self.bg_dark
        )
        self.icon_container.pack(fill="both", expand=True)
        
    
        self.functionality.refresh_sidebar_content()
        

        self.channel_frame = ctk.CTkFrame( #sidebar (channels)
            self,
            width=240,
            fg_color=self.bg_medium,
            corner_radius=0
        )
        self.channel_frame.pack(side="left", fill="y", padx=0, pady=0)
        self.channel_frame.pack_propagate(False)
        
        server_header = ctk.CTkFrame( #server header
            self.channel_frame,
            height=60,
            fg_color=self.bg_medium,
            corner_radius=0
        )
        server_header.pack(fill="x", padx=0, pady=0)
        
        server_label = ctk.CTkLabel(
            server_header,
            text="Server Name",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.text_color
        )
        server_label.pack(pady=20, padx=15, anchor="w")
        
        channels_label = ctk.CTkLabel(
            self.channel_frame,
            text="Channels",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        channels_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        self.add_channel("#mainchat", True)
        self.add_channel("#artchat", False) #adding channels
        
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color=self.bg_light,
            corner_radius=0
        )
        self.main_frame.pack(side="left", fill="both", expand=True)
        
        chat_header = ctk.CTkFrame( #chat header 
            self.main_frame,
            height=60,
            fg_color=self.bg_medium,
            corner_radius=0
        )
        chat_header.pack(fill="x", padx=0, pady=0)
        
        self.channel_title_label = ctk.CTkLabel( #clickable chanels to change 
            chat_header,
            text="Open Artboard",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.text_color,
            cursor="hand2"
        )
        self.channel_title_label.pack(pady=20, padx=20, anchor="w")
        self.channel_title_label.bind("<Button-1>", self.artboard.toggle_artboard_mode)
        
      
        self.chat_area = ctk.CTkScrollableFrame( #quick chat area 
            self.main_frame,
            fg_color=self.bg_light,
            corner_radius=0
        )
        self.chat_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.input_frame = ctk.CTkFrame( #message send 
            self.main_frame,
            height=80,
            fg_color=self.bg_light,
            corner_radius=0
        )
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.input_frame.pack_propagate(False)
        
        input_container = ctk.CTkFrame(
            self.input_frame,
            fg_color="transparent"
        )
        input_container.pack(fill="x", padx=10, pady=15)
        
        self.search_entry = ctk.CTkEntry( #message input area 
            input_container,
            placeholder_text="Message Chat",
            height=50,
            corner_radius=25,
            fg_color=self.bg_medium,
            border_width=2,
            border_color=self.accent_orange,
            text_color=self.text_color,
            font=ctk.CTkFont(size=14)
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
    
        send_btn = ctk.CTkButton( #send button (fix emoji)
            input_container,
            text="→",
            width=50,
            height=50,
            corner_radius=25,
            fg_color=self.accent_orange,
            hover_color="#ff8555",
            font=ctk.CTkFont(size=24, weight="bold"),
            command=self.functionality.send_message
        )
        send_btn.pack(side="right")
        
    def setup_ui(self):
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        self.create_sidebar()
        
        self.channels_frame = ChannelsFrame(
            self.main_container, 
            self,
            fg_color=self.bg_medium
        )
        self.channels_frame.pack(side="left", fill="y")
        
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color=self.bg_light)
        self.content_frame.pack(side="left", fill="both", expand=True)
        
        self.create_header()
        self.create_chat_view()
        
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self.main_container, 
            width=80, 
            fg_color=self.bg_dark
        )
        self.sidebar.pack(side="left", fill="y", padx=(0, 1))
        self.sidebar.pack_propagate(False)
        
        self.sidebar_label = ctk.CTkLabel(
            self.sidebar,
            text="Servers",
            font=("Segoe UI", 12, "bold"),
            cursor="hand2"
        )
        self.sidebar_label.pack(pady=(15, 15))
        self.sidebar_label.bind("<Button-1>", self.toggle_sidebar_mode)
        
        self.servers_container = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.servers_container.pack(fill="both", expand=True)
        
        self.show_servers()
        
    def show_servers(self):
        for widget in self.servers_container.winfo_children():
            widget.destroy()
            
        colors = ["#1e3a8a", "#15803d", "#f4c430"]
        for i, color in enumerate(colors):
            server_frame = ctk.CTkFrame(
                self.servers_container,
                width=50,
                height=50,
                corner_radius=15,
                fg_color=color,
                border_width=2,
                border_color=self.accent_orange
            )
            server_frame.pack(pady=10, padx=15)
            
            if i == 0:
                indicator = ctk.CTkFrame(
                    server_frame,
                    width=4,
                    height=30,
                    fg_color=self.accent_orange,
                    corner_radius=2
                )
                indicator.place(x=-10, y=10)
                
    def show_friends(self):
        for widget in self.servers_container.winfo_children():
            widget.destroy()
            
        for friend in self.friends:
            friend_frame = ctk.CTkFrame(
                self.servers_container,
                fg_color="transparent",
                height=30
            )
            friend_frame.pack(fill="x", padx=10, pady=2)
            
            status_colors = {
                "online": "#00ff00",
                "away": "#ffff00",
                "offline": "#666666"
            }
            
            status_dot = ctk.CTkFrame(
                friend_frame,
                width=10,
                height=10,
                corner_radius=5,
                fg_color=status_colors[friend["status"]]
            )
            status_dot.pack(side="left", padx=(0, 8))
            
            name_label = ctk.CTkLabel(
                friend_frame,
                text=friend["name"],
                font=("Segoe UI", 11)
            )
            name_label.pack(side="left")
            
    def toggle_sidebar_mode(self, event=None):
        if self.sidebar_mode == "servers":
            self.sidebar_mode = "friends"
            self.sidebar_label.configure(text="Friends")
            self.sidebar.configure(width=150)
            self.show_friends()
        else:
            self.sidebar_mode = "servers"
            self.sidebar_label.configure(text="Servers")
            self.sidebar.configure(width=80)
            self.show_servers()
            
    def create_header(self):
        self.header = ctk.CTkFrame(
            self.content_frame,
            height=100,
            fg_color=self.bg_medium
        )
        self.header.pack(fill="x", pady=(0, 1))
        self.header.pack_propagate(False)
        
        # Container for title and logo
        header_content = ctk.CTkFrame(self.header, fg_color="transparent")
        header_content.pack(side="left", padx=20, pady=17)
        
        # Title
        self.header_title = ctk.CTkLabel(
            header_content,
            text="Main Chat",
            font=("Segoe UI", 16, "bold"),
            cursor="hand2"
        )
        self.header_title.pack(side="left", padx=(0, 15))
        self.header_title.bind("<Button-1>", self.toggle_view)
        
        # Animated Logo (positioned after title)
        self.animated_logo = AnimatedLogo(
            header_content,
            video_path=self.animation_video_path,
            logo_image_path=self.logo_image_path,
            size=80
        )
        self.animated_logo.pack(side="left")
        
        # Make header clickable too
        self.header.bind("<Button-1>", self.toggle_view)
        
    def toggle_view(self, event=None):
        if self.current_view == "chat":
            self.switch_to_artboard()
        else:
            self.switch_to_chat()
            
    def switch_to_artboard(self):
        self.current_view = "artboard"
        self.header_title.configure(text="Artboard")
        
        if hasattr(self, 'chat_container'):
            self.chat_container.destroy()
            
        self.channels_frame.switch_to_mini_chat()
        
        self.artboard = SketchiArtboard(self.content_frame, self)
        self.artboard.pack(fill="both", expand=True)
        
    def switch_to_chat(self):
        self.current_view = "chat"
        self.header_title.configure(text="Main Chat")
        
        if hasattr(self, 'artboard'):
            self.artboard.destroy()
            
        self.channels_frame.switch_to_channels()
        
        self.create_chat_view()
        
    def create_chat_view(self):
        self.chat_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.chat_container.pack(fill="both", expand=True)
        
        self.messages_area = ctk.CTkScrollableFrame(
            self.chat_container,
            fg_color="transparent"
        )
        self.messages_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        for msg in self.messages:
            msg_frame = ctk.CTkFrame(
                self.messages_area,
                fg_color=self.bg_medium,
                corner_radius=10
            )
            msg_frame.pack(fill="x", pady=5, anchor="w")
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=f"{msg['sender']}: {msg['text']}",
                font=("Segoe UI", 12),
                anchor="w"
            )
            msg_label.pack(padx=15, pady=12, fill="x")
            
        self.input_frame = ctk.CTkFrame(
            self.chat_container,
            height=90,
            fg_color="transparent"
        )
        self.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.input_frame.pack_propagate(False)
        
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            height=50,
            corner_radius=25,
            border_width=2,
            border_color=self.accent_orange,
            fg_color=self.bg_medium,
            placeholder_text="Message Chat"
        )
        self.message_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message)
        
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="→",
            width=50,
            height=50,
            corner_radius=25,
            fg_color=self.accent_orange,
            hover_color="#ff8555",
            font=("Segoe UI", 24),
            command=self.send_message
        )
        self.send_button.pack(side="left")

    def write_message_to_chat(self, text, username):
        text = text.strip()
        if text:
            self.messages.append({"sender": username, "text": text})
            
            msg_frame = ctk.CTkFrame(
                self.messages_area,
                fg_color=self.bg_medium,
                corner_radius=10
            )
            msg_frame.pack(fill="x", pady=5, anchor="w")
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=f"{username}: {text}",
                font=("Segoe UI", 12),
                anchor="w"
            )
            msg_label.pack(padx=15, pady=12, fill="x")
            
            self.message_entry.delete(0, "end")
            
            self.messages_area._parent_canvas.yview_moveto(1.0) # Moves area down when there are more messages than screenspace

    def clear_messages(self):
        for widget in self.messages_area.winfo_children():
            widget.destroy()
        self.messages = []
        
    def send_message(self, event=None):
        text = self.message_entry.get().strip()
        username = Cache.get("username")

        self.write_message_to_chat(text, username)


    def load_channel(self, channel_name):
        self.clear_messages()

        channel_messages = Cache.get(f"channel_{channel_name}_messages")
        if channel_messages:
            for msg in channel_messages:
                self.write_message_to_chat(msg['text'], msg['sender'])
        else:
            MessageSender.send_message({
                "msg_type": "channel_messages_request",
                "channel": channel_name
            })

        self.active_channel = channel_name
        



app = None

def run():
    global app

    app = SketchiApp()
    app.mainloop()

