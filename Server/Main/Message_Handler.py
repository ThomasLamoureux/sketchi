import Main.Formatter as Formatter
import Main.Login as Login
import Main.TempCanvas as TempCanvas


def message_recieved(conn, address, message):
    msg_type, data = Formatter.decode(message)
    print(msg_type, data)

    if msg_type == "login":
        print("Login attempt")
        Login.login(conn, address, data[0], data[1])
    elif msg_type == "signup":
        print("Signup attempt")
        Login.sign_up(conn, address, data[0], data[1])
    elif msg_type == "draw":
        TempCanvas.draw(conn, data)
    elif msg_type == "drawings_request":
        TempCanvas.request_drawings(conn)
