import Login.ConnectToServer as ConnectToServer
import Login.LoginGUI as LoginGUI
import tkinter as tk

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Makes it look good



def connect(address):

    if not address:
        lbl_message.config(text="Please enter server address", fg="red")

    else:
        lbl_message.config(text="Connecting...", fg="black")

        connected = ConnectToServer.connect(address)


        if connected == 1:
            success()
        else:
            failed()



def success():
    root.destroy()
    LoginGUI.run()



def failed():
    lbl_message.config(text="Failed to connect...", fg="red")



def center_window(win, width, height):
    # Get screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate position x, y
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    win.geometry(f"{width}x{height}+{x}+{y}")
        



root = tk.Tk()
root.title("Connect")
center_window(root, 300, 250)
root.resizable(False, False)
root.configure(bg="#f0f0f0")
root.tk.call('tk', 'scaling', 1.5)  # Try 1.25, 1.5, 2.0 depending on your screen



# Container Frame
frame = tk.Frame(root, bg="white", bd=2, relief="groove")
frame.place(relx=0.5, rely=0.5, anchor="center", width=300, height=250)

# Title
lbl_title = tk.Label(frame, text="Enter server IP and port", font=("Helvetica", 12, "bold"), bg="white")
lbl_title.pack(pady=10)

# IP
entry_ip = tk.Entry(frame, font=("Arial", 10), bd=1, relief="solid")
entry_ip.pack(pady=5, ipady=3, fill="x", padx=20)

# Message label (for errors/success)
lbl_message = tk.Label(frame, text="", font=("Arial", 9), bg="white")
lbl_message.pack(pady=5)

# Action button
btn_action = tk.Button(frame, text="Connect", command=lambda: connect(entry_ip.get().strip()),
                    bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                    activebackground="#1976D2", activeforeground="white",
                    relief="flat", height=2)
btn_action.pack(pady=10, fill="x", padx=40)




root.mainloop()