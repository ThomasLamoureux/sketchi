import ServerCommunication.Pipeline as Pipeline
import Cache.Cache as Cache
import FrontEnd.Main as GUI
import tkinter as tk


def validate_credentials(username, password):
    Pipeline.send_message("login", [username, password])



def sign_up(username, password):
    Pipeline.send_message("signup", [username, password])


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