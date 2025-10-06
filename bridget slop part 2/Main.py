import customtkinter as ctk
from functionality import SketchiFunctionality
from artboard import SketchiiArtboard 

ctk.set_appearance_mode("dark") #appearence dark mode 
ctk.set_default_color_theme("blue")

class SketchiiApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sketchi") #layout 
        self.geometry("1200x700")
        self.configure(fg_color="#1e1e1e")
        
        self.bg_dark = "#1e1e1e" #colors from tinker 
        self.bg_medium = "#2b2b2b"
        self.bg_light = "#363636"
        self.accent_orange = "#ff6b35"
        self.text_color = "#ffffff"
        
        
        self.sidebar_mode = "servers"
        
        self.functionality = SketchiFunctionality(self)
        self.artboard = SketchiiArtboard(self)
        
        self.create_layout() #main layout
        
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
            text="Main Chat",
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
    
    def add_channel(self, name, is_active=False):
        bg_color = self.bg_light if is_active else self.bg_medium
        
        channel_btn = ctk.CTkButton(
            self.channel_frame,
            text=name,
            font=ctk.CTkFont(size=14),
            fg_color=bg_color,
            hover_color=self.bg_light,
            text_color=self.accent_orange if is_active else "#cccccc",
            corner_radius=8,
            height=35,
            anchor="w"
        )
        channel_btn.pack(fill="x", padx=10, pady=3)

if __name__ == "__main__":
    app = SketchiiApp()
    app.mainloop()