import Login.Login as Login
import tkinter as tk

import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Makes it look good


global_methods = {}

def global_method(method):
    global_methods[method]()


def run():
    def center_window(win, width, height):
        # Get screen width and height
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()

        # Calculate position x, y
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        win.geometry(f"{width}x{height}+{x}+{y}")


    def login(username, password):

        if not username or not password:
            lbl_message.config(text="Please fill in all fields.", fg="red")
            return

        result = Login.validate_credentials(username, password)


        if result == 1:
            lbl_message.config(text=f"Welcome back, {username}!", fg="green")

        elif result == 0:
            lbl_message.config(text="Invalid username or password.", fg="red")

        else:
            lbl_message.config(text="An error occured.", fg="red")
            

    def sign_up(username, password):

        if not username or not password:
            lbl_message.config(text="Please fill in all fields.", fg="red")
            return


        result = Login.sign_up(username, password)

        if result == 1:
            lbl_message.config(text="Account created! You can now log in.", fg="green")
            switch_to_login()
        elif result == 0:
            lbl_message.config(text="Username already exists.", fg="red")
        else:
            lbl_message.config(text="An error occured.", fg="red")


    def login_failed():
        print("failed")
        lbl_message.config(text="Invalid username or password.", fg="red")

    
    global_methods["login_failed"] = login_failed



    def switch_to_signup():
        btn_action.config(text="Sign Up", command=lambda: sign_up(entry_username.get().strip(), entry_password.get().strip()), bg="#4CAF50")
        lbl_switch.config(text="Already have an account?")
        btn_switch.config(text="Login", command=switch_to_login)
        lbl_message.config(text="")

    def switch_to_login():
        btn_action.config(text="Login", command=lambda: login(entry_username.get().strip(), entry_password.get().strip()), bg="#2196F3")
        lbl_switch.config(text="Don't have an account?")
        btn_switch.config(text="Sign Up", command=switch_to_signup)



    root = tk.Tk()
    root.title("Sketchi Login")
    center_window(root, 340, 360)
    root.resizable(False, False)
    root.configure(bg="#f0f0f0")


    # Container Frame
    frame = tk.Frame(root, bg="white", bd=2, relief="groove")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=340, height=360)

    # Title
    lbl_title = tk.Label(frame, text="Sketchi", font=("Helvetica", 14, "bold"), bg="white")
    lbl_title.pack(pady=10)

    # Username
    entry_username = tk.Entry(frame, font=("Arial", 10), bd=1, relief="solid")
    entry_username.pack(pady=5, ipady=3, fill="x", padx=20)

    # Password
    entry_password = tk.Entry(frame, show="*", font=("Arial", 10), bd=1, relief="solid")
    entry_password.pack(pady=5, ipady=3, fill="x", padx=20)

    # Message label (for errors/success)
    lbl_message = tk.Label(frame, text="", font=("Arial", 9), bg="white")
    lbl_message.pack(pady=5)

    # Action button
    btn_action = tk.Button(frame, text="Login", command=lambda: login(entry_username.get().strip(), entry_password.get().strip()),
                        bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                        activebackground="#1976D2", activeforeground="white",
                        relief="flat", height=2)
    btn_action.pack(pady=10, fill="x", padx=40)

    # Switch option
    lbl_switch = tk.Label(frame, text="Don't have an account?", bg="white", font=("Arial", 9))
    lbl_switch.pack()

    btn_switch = tk.Button(frame, text="Sign Up", command=switch_to_signup,
                        bg="white", fg="#2196F3", bd=0, font=("Arial", 9, "underline"),
                        activeforeground="#1976D2", cursor="hand2")
    btn_switch.pack()


    root.mainloop()


if __name__ == "__main__":
    run()