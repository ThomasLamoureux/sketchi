import ServerCommunication.Main_Client as Main_Client
import Cache.Cache as Cache
import FrontEnd.gui as GUI
import tkinter as tk
import asyncio


def validate_credentials(username, password):
    payload = {
        "msg_type": "login",
        "username": username,
        "password": password
    }

    Main_Client.send_message(payload)




def sign_up(email, username, password):
    payload = {
        "msg_type": "signup",
        "email": email,
        "username": username,
        "password": password
    }
    print("Requesting sign up")
    Main_Client.send_message(payload)


def verify_code(code):
    payload = {
        "msg_type": "email_verification_attempt",
        "username": Cache.get("username"),
        "verification_code": code
    }
    print(f"sending {Cache.get("username")}, {code}")
    Main_Client.send_message(payload)

def sign_up_confirmation(success, username=None, verfication_required=None):
    print("Confirmation recieved")
    if success == False:
         GUI.app.failed_signup()
         return
    
    Cache.add("username", username)

    if verfication_required:
        GUI.app.verification_gui()
    else:
        GUI.app.sign_up_complete(verfication_required)


def login_confirmation(success, username=None):
    print("Confirmation recieved")
    if success == False:
         GUI.app.failed_login()
         return

    Cache.add("username", username)

    GUI.app.complete_login()

