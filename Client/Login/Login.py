import ServerCommunication.Pipeline as Pipeline
import Cache.Cache as Cache
import Login.LoginGUI as LoginGUI


def validate_credentials(username, password):
    Pipeline.send_message("login; ", [username, password])



def sign_up(username, password):
    Pipeline.send_message("signup; ", [username, password])


def sign_up_confirmation(data):
    if data[0] == "-1":
        return 

    username = data[1]
    Cache.add("username", username)


def login_confirmation(data):
    if data[0] == "-1":
         LoginGUI.global_method("login_failed")

    username = data[1]
    Cache.add("username", username)