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

    Client.send_message(payload)



def sign_up_confirmation(success, username=None, verfication_required=None):
    print("Confirmation recieved")
    if success == False:
         GUI.app.failed_signup()
         return

    Cache.add("username", username)

    GUI.app.sign_up_complete(verfication_required)


def login_confirmation(success, username=None):
    print("Confirmation recieved")
    if success == False:
         GUI.app.failed_login()
         return

    Cache.add("username", username)

    GUI.app.complete_login()