import Main.login as login
import Main.paint_project_handler as paint_project_handler


def message_recieved(client_id, msg_type, payload):
    if msg_type == "login":
        username = payload.get("username")
        password = payload.get("password")

        login.login(client_id, username, password)

    elif msg_type == "signup":
        username = payload.get("username")
        password = payload.get("password")

        login.sign_up(client_id, username, password)

    elif msg_type == "draw_line":
        paint_project_handler.draw(client_id, payload.get("drawing_data"))

    elif msg_type == "drawings_request":

        paint_project_handler.request_drawings(client_id)
