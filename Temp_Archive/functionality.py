import customtkinter as ctk #logic 
import Cache.Cache as Cache

class SketchiFunctionality:
    def __init__(self, app):
        self.app = app
    
    def add_server_icon(self, color, is_active=False):
        """Add a server icon to the sidebar"""
        icon_frame = ctk.CTkFrame(
            self.app.icon_container,
            width=50,
            height=50,
            fg_color=color,
            corner_radius=15
        )
        icon_frame.pack(pady=10, padx=15)
        
        if is_active: #user active 
            indicator = ctk.CTkFrame(
                self.app.server_frame,
                width=4,
                height=30,
                fg_color=self.app.accent_orange,
                corner_radius=2
            )
            indicator.place(x=0, y=icon_frame.winfo_y() + 10)
    
    def add_friend_item(self, name, is_online=True):
        """Add a friend to the friends list"""
        friend_frame = ctk.CTkFrame(
            self.app.icon_container,
            fg_color="transparent"
        )
        friend_frame.pack(pady=5, padx=10, fill="x")
        
       
        status_color = "#00ff00" if is_online else "#888888" #active indicator
        status = ctk.CTkFrame(
            friend_frame,
            width=12,
            height=12,
            fg_color=status_color,
            corner_radius=6
        )
        status.pack(side="left", padx=(5, 8))
        
      
        name_label = ctk.CTkLabel( #userlabeles (will change based on user info)
            friend_frame,
            text=name,
            font=ctk.CTkFont(size=11),
            text_color=self.app.text_color
        )
        name_label.pack(side="left", anchor="w")
    
    def toggle_sidebar_mode(self, event=None):
        """Toggle between servers and friends view"""
        if self.app.sidebar_mode == "servers":
            self.app.sidebar_mode = "friends"
            self.app.servers_label.configure(text="Friends")
            # Expand sidebar for friends view
            self.app.server_frame.configure(width=150)
        else:
            self.app.sidebar_mode = "servers"
            self.app.servers_label.configure(text="Servers")
            # Shrink sidebar for servers view
            self.app.server_frame.configure(width=80)
        
        self.refresh_sidebar_content()
    
    def refresh_sidebar_content(self):
        """Refresh the sidebar content based on current mode"""
        # Clear current content
        for widget in self.app.icon_container.winfo_children():
            widget.destroy()
        
        # Add content based on mode
        if self.app.sidebar_mode == "servers":
            self.add_server_icon("#f4c430", True)
            self.add_server_icon("#f4c430", False)
            self.add_server_icon("#e8a87c", False)
        else:
            self.add_friend_item("Chunky", True)
            self.add_friend_item("Saba.ex", True)
            self.add_friend_item("Kanakara", False)
            self.add_friend_item("WhiteBeard", True)
    
    def send_message(self):
        """Send a message to the chat"""
        message = self.app.search_entry.get()
        if message.strip():
        
            msg_frame = ctk.CTkFrame(
                self.app.chat_area,
                fg_color=self.app.bg_medium,
                corner_radius=10
            )
            msg_frame.pack(fill="x", pady=5, padx=10, anchor="w")
            username = Cache.get("username")
            msg_label = ctk.CTkLabel(
                msg_frame,
                text=f"{username}: {message}",
                font=ctk.CTkFont(size=13),
                text_color=self.app.text_color,
                anchor="w"
            )
            msg_label.pack(padx=15, pady=10, anchor="w")
            

            self.app.search_entry.delete(0, "end")