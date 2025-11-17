import Main.Formatter as Formatter
import Main.Login as Login
import Main.TempCanvas as TempCanvas


def message_recieved(client_id, msg_type, payload):
    if msg_type == "login":
        print("Login attempt")

        username = payload.get("username")
        password = payload.get("password")

        Login.login(client_id, username, password)

    elif msg_type == "signup":
        print("Signup attempt")

        username = payload.get("username")
        password = payload.get("password")

        Login.sign_up(client_id, username, password)

    elif msg_type == "draw_line":
        print("DRAWING")
        TempCanvas.draw(client_id, payload.get("drawing_data"))

    elif msg_type == "drawings_request":
        TempCanvas.request_drawings(client_id)
