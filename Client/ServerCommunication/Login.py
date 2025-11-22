import ServerCommunication.Client as Client
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

    Client.send_message(payload)




def sign_up(username, password):
    payload = {
        "msg_type": "signup",
        "username": username,
        "password": password
    }
    print("erm?")
    Client.send_message(payload)
    print("SENT!?")


def sign_up_confirmation(success, username=None):
    print("Confirmation recieved")
    if success == False:
         GUI.failed_signup()
         return

    Cache.add("username", username)

    GUI.complete_login()


def login_confirmation(success, username=None):
    print("Confirmation recieved")
    if success == False:
         GUI.failed_login()
         return

    Cache.add("username", username)

    GUI.complete_login()