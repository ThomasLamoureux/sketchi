import customtkinter as ctk
import asyncio
import ServerCommunication.Client as Client
from FrontEnd.functionality import SketchiFunctionality
from FrontEnd.artboard import SketchiiArtboard
import ServerCommunication.Login as Login


ctk.set_appearance_mode("dark") #appearence dark mode 
ctk.set_default_color_theme("blue")


loop = None

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
        self.connecting = False
        
        #self.create_layout() #main layout

        self.connect_gui()


    def login_complete(self):
        self.create_layout()


    def failed_login(self):
        print("failed login")
        self.lbl_message.configure(text="Invalid username or password.", text_color="red")


    def failed_signup(self):
        print("failed signup")
        self.lbl_message.configure(text="Username already exists.", text_color="red")


    def failed_connection(self):
        print("failed connection")
        self.lbl_message.configure(text="Failed to connect.", text_color="red")
    

    def success_connection(self):
        print("successful connection")
        self.login_gui()


    def login_gui(self):
        def login(username, password):

            if not username or not password:
                self.lbl_message.configure(text="Please fill in all fields.", text_color="red")
                return



            Login.validate_credentials(username, password)

            

        def sign_up(username, password):

            if not username or not password:
                self.lbl_message.configure(text="Please fill in all fields.", text_color="red")
                return


            Login.sign_up(username, password)


        def switch_to_signup():
            btn_action.configure(text="Sign Up", command=lambda: sign_up(self.entry_username.get().strip(), self.entry_password.get().strip()))
            lbl_switch.configure(text="Already have an account?")
            btn_switch.configure(text="Login", command=switch_to_login)
            self.lbl_message.configure(text="")

        def switch_to_login():
            btn_action.configure(text="Login", command=lambda: login(self.entry_username.get().strip(), self.entry_password.get().strip()))
            lbl_switch.configure(text="Don't have an account?")
            btn_switch.configure(text="Sign Up", command=switch_to_signup)

            
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

        #if success == 1:
        #    self.login_gui()
        #else:
        #    self.lbl_message.configure(text="Failed to connect.", text_color="red")



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

app = None

def run():
    global app
    app = SketchiiApp()
    app.mainloop()


def complete_login():
    app.login_complete()


def manual_draw(data):
    app.artboard.manual_draw(data)


def bulk_draw(data):
    app.artboard.bulk_draw(data)


def failed_login():
    app.failed_login()


def failed_signup():
    app.failed_signup()


def failed_connection():
    app.failed_connection()


def success_connection():
    app.success_connection()