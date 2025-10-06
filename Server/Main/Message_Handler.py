import Main.Formatter as Formatter
import Main.Login as Login


def message_recieved(conn, address, message):
    msg_type, data = Formatter.decode(message)


    if msg_type == "login":
        Login.login(conn, address, data[0], data[1])
    elif msg_type == "signup":
        Login.sign_up(conn, address, data[0], data[1])