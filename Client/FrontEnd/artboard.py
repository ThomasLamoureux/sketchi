# artboard.py - Artboard drawing functionality
import customtkinter as ctk
from tkinter import Canvas

class SketchiiArtboard:
    def __init__(self, app):
        self.app = app
        self.artboard_mode = False
        self.drawing = False
        self.last_x = None
        self.last_y = None
        self.brush_color = self.app.accent_orange
        self.brush_size = 3
        
    def toggle_artboard_mode(self, event=None):
        """Toggle between chat mode and artboard mode"""
        self.login_gui()
        return
        if not self.artboard_mode:
            # Switch TO artboard mode
            self.artboard_mode = True
            self.app.channel_title_label.configure(text="Artboard")
            self.switch_to_artboard()
        else:
            # Switch BACK to chat mode
            self.artboard_mode = False
            self.app.channel_title_label.configure(text="Main Chat")
            self.switch_to_chat()
    
    def switch_to_artboard(self):
        self.login_gui()
        return
        """Show artboard and hide chat area"""
        # Hide chat area
        self.app.chat_area.pack_forget()
        
        # Hide input frame
        self.app.input_frame.pack_forget()
        
        # Create artboard canvas
        self.canvas = Canvas(
            self.app.main_frame,
            bg="#ffffff",
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True, padx=20, pady=(20, 10))
        
        # Bind drawing events
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Shrink channel sidebar and convert to mini chat
        self.app.channel_frame.configure(width=200)
        
        # Clear channel content
        for widget in self.app.channel_frame.winfo_children():
            widget.destroy()
        
        # Create mini chat header
        mini_header = ctk.CTkFrame(
            self.app.channel_frame,
            height=50,
            fg_color=self.app.bg_medium,
            corner_radius=0
        )
        mini_header.pack(fill="x", padx=0, pady=0)
        
        mini_label = ctk.CTkLabel(
            mini_header,
            text="Quick Chat",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.app.text_color
        )
        mini_label.pack(pady=15, padx=10)
        
        # Create mini chat area
        self.mini_chat = ctk.CTkScrollableFrame(
            self.app.channel_frame,
            fg_color=self.app.bg_light,
            corner_radius=0
        )
        self.mini_chat.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mini chat input
        mini_input_frame = ctk.CTkFrame(
            self.app.channel_frame,
            height=60,
            fg_color=self.app.bg_medium,
            corner_radius=0
        )
        mini_input_frame.pack(fill="x", padx=5, pady=5)
        mini_input_frame.pack_propagate(False)
        
        self.mini_entry = ctk.CTkEntry(
            mini_input_frame,
            placeholder_text="Message",
            height=35,
            corner_radius=17,
            fg_color=self.app.bg_light,
            border_width=1,
            border_color=self.app.accent_orange,
            text_color=self.app.text_color,
            font=ctk.CTkFont(size=12)
        )
        self.mini_entry.pack(fill="x", padx=5, pady=12)
        self.mini_entry.bind("<Return>", lambda e: self.send_mini_message())
        
        # Add drawing tools
        self.create_drawing_tools()


    def login_gui(self):
        def request_art_project(owner, code):
            pass

            
        frame = ctk.CTkFrame(self, width=340, height=360, corner_radius=12)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        lbl_title = ctk.CTkLabel(frame, text="Sketchi", font=ctk.CTkFont(size=18, weight="bold"))
        lbl_title.pack(pady=15)

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
            command=lambda: request_art_project(self.entry_username.get().strip(), self.entry_password.get().strip())
        )

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


    
    
    def switch_to_chat(self):
        """Switch back to regular chat mode"""
        # Destroy artboard canvas
        if hasattr(self, 'canvas'):
            self.canvas.destroy()
        
        # Destroy drawing tools
        if hasattr(self, 'tools_frame'):
            self.tools_frame.destroy()
        
        # Show chat area again
        self.app.chat_area.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Show input frame again
        self.app.input_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        # Restore channel sidebar
        self.app.channel_frame.configure(width=240)
        
        # Clear and restore channel content
        for widget in self.app.channel_frame.winfo_children():
            widget.destroy()
        
        # Recreate server header
        server_header = ctk.CTkFrame(
            self.app.channel_frame,
            height=60,
            fg_color=self.app.bg_medium,
            corner_radius=0
        )
        server_header.pack(fill="x", padx=0, pady=0)
        
        server_label = ctk.CTkLabel(
            server_header,
            text="Server Name",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.app.text_color
        )
        server_label.pack(pady=20, padx=15, anchor="w")
        
        # Channels section
        channels_label = ctk.CTkLabel(
            self.app.channel_frame,
            text="Channels",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#888888"
        )
        channels_label.pack(pady=(10, 5), padx=15, anchor="w")
        
        # Re-add channels
        self.app.add_channel("#mainchat", True)
        self.app.add_channel("#artchat", False)
    
    def create_drawing_tools(self):
        """Create drawing tools palette"""
        self.tools_frame = ctk.CTkFrame(
            self.app.main_frame,
            height=70,
            fg_color=self.app.bg_medium,
            corner_radius=10
        )
        self.tools_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.tools_frame.pack_propagate(False)
        
        # Left side - Colors
        left_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        left_frame.pack(side="left", fill="y", padx=10, pady=10)
        
        tools_label = ctk.CTkLabel(
            left_frame,
            text="Colors:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.text_color
        )
        tools_label.pack(side="left", padx=(0, 10))
        
        colors = [self.app.accent_orange, "#000000", "#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff", "#00ffff", "#ffffff"]
        
        for color in colors:
            color_btn = ctk.CTkButton(
                left_frame,
                text="",
                width=35,
                height=35,
                corner_radius=17,
                fg_color=color,
                hover_color=color,
                border_width=2,
                border_color=self.app.bg_dark if color != "#ffffff" else "#cccccc",
                command=lambda c=color: self.change_color(c)
            )
            color_btn.pack(side="left", padx=3)
        
        # Right side - Tools
        right_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        right_frame.pack(side="right", fill="y", padx=10, pady=10)
        
        # Clear button
        clear_btn = ctk.CTkButton(
            right_frame,
            text="Clear",
            width=80,
            height=35,
            corner_radius=17,
            fg_color="#cc0000",
            hover_color="#ff0000",
            font=ctk.CTkFont(size=12, weight="bold"),
            command=self.clear_canvas
        )
        clear_btn.pack(side="right", padx=(10, 0))
        
        # Eraser button
        eraser_btn = ctk.CTkButton(
            right_frame,
            text="Eraser",
            width=80,
            height=35,
            corner_radius=17,
            fg_color=self.app.bg_light,
            hover_color=self.app.bg_dark,
            font=ctk.CTkFont(size=12, weight="bold"),
            command=lambda: self.change_color("#ffffff")
        )
        eraser_btn.pack(side="right", padx=5)
        
        # Center - Brush size slider
        center_frame = ctk.CTkFrame(self.tools_frame, fg_color="transparent")
        center_frame.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        
        size_label = ctk.CTkLabel(
            center_frame,
            text="Brush Size:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.text_color
        )
        size_label.pack(anchor="w", pady=(0, 5))
        
        # Slider container
        slider_container = ctk.CTkFrame(center_frame, fg_color="transparent")
        slider_container.pack(fill="x")
        
        self.size_slider = ctk.CTkSlider(
            slider_container,
            from_=1,
            to=20,
            number_of_steps=19,
            width=200,
            height=20,
            button_color=self.app.accent_orange,
            button_hover_color="#ff8555",
            progress_color=self.app.accent_orange,
            fg_color=self.app.bg_light,
            command=self.update_brush_size
        )
        self.size_slider.set(3)
        self.size_slider.pack(side="left", padx=(0, 10))
        
        self.size_display = ctk.CTkLabel(
            slider_container,
            text="3px",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.app.accent_orange,
            width=50
        )
        self.size_display.pack(side="left")
    
    def start_draw(self, event):
        """Start drawing"""
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
    
    def draw(self, event):
        """Draw on canvas"""
        if self.drawing:
            if self.last_x and self.last_y:
                self.canvas.create_line(
                    self.last_x, self.last_y, event.x, event.y,
                    fill=self.brush_color,
                    width=self.brush_size,
                    capstyle="round",
                    smooth=True
                )
            self.last_x = event.x
            self.last_y = event.y
    
    def stop_draw(self, event):
        """Stop drawing"""
        self.drawing = False
        self.last_x = None
        self.last_y = None
    
    def change_color(self, color):
        """Change brush color"""
        self.brush_color = color
    
    def change_brush_size(self, size):
        """Change brush size"""
        self.brush_size = size
    
    def update_brush_size(self, value):
        """Update brush size from slider"""
        self.brush_size = int(value)
        self.size_display.configure(text=f"{self.brush_size}px")
    
    def clear_canvas(self):
        """Clear the canvas"""
        self.canvas.delete("all")
    
    def send_mini_message(self):
        """Send a message in mini chat"""
        message = self.mini_entry.get()
        if message.strip(): 
            msg_frame = ctk.CTkFrame(
                self.mini_chat,
                fg_color=self.app.bg_medium,
                corner_radius=8
            )
            msg_frame.pack(fill="x", pady=3, padx=3)
            
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=message,
                font=ctk.CTkFont(size=11),
                text_color=self.app.text_color,
                wraplength=170,
                anchor="w"
            )
            msg_label.pack(padx=8, pady=5, anchor="w")
            
            self.mini_entry.delete(0, "end")