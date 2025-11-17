import ServerCommunication.Client as Client
import Cache.Cache as Cache
import FrontEnd.Main as GUI
import tkinter as tk


def validate_credentials(username, password):
    payload = {
        "msg_type": "login",
        "username": username,
        "password": password
    }

    Client.send_message(payload)



def sign_up(username, password):
    payload = {
        "msg_type": "sign_up",
        "username": username,
        "password": password
    }

    Client.send_message(payload)



def sign_up_confirmation(data):
    if data[0] == "-1":
        GUI.failed_signup()
        return

    username = data[1]
    Cache.add("username", username)

    GUI.complete_login()


def login_confirmation(data):
    if data[0] == "-1":
         GUI.failed_login()
         return

    username = data[1]
    Cache.add("username", username)

    GUI.complete_login()