import ServerCommunication.Formatter as Formatter
import Login.Login as Login


def message_recieved(conn, message):
    msg_type, data = Formatter.decode(message)


    if msg_type == "login":
        Login.login_confirmation(data)
    elif msg_type == "signup":
        Login.sign_up_confirmation(data)