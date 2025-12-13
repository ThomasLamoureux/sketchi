import Main.Login as login
import Main.canvas_project_handler as paint_project_handler
import Main.Main_Server as server


def message_recieved(client_id, msg_type, payload):
    if msg_type == "login":
        username = payload.get("username")
        password = payload.get("password")

        login.login(client_id, username, password)

    elif msg_type == "signup":
        username = payload.get("username")
        email = payload.get("email")
        password = payload.get("password")

        login.sign_up(client_id, username, email, password)

    elif msg_type == "draw":
        paint_project_handler.draw(client_id, payload.get("drawing_data"))

    elif msg_type == "drawings_request":
        paint_project_handler.request_drawings(client_id)

    elif msg_type == "clear_canvas":
        paint_project_handler.clear_canvas(client_id)

    elif msg_type == "email_verification_attempt":
        username = payload.get("username")
        code = payload.get("verification_code")

        login.verify_email_code(client_id, username, code)

    elif msg_type == "join_art_project":
        owner = payload.get("owner")
        code = payload.get("code")

        paint_project_handler.join_art_project(client_id, owner, code)

    elif msg_type == "create_art_project":
        print(server.server.accounts)
        print("write here officer")
        owner_username = server.server.accounts.get(client_id).username
        

        paint_project_handler.new_paint_project(client_id, owner_username)

    elif msg_type == "project_message":
        paint_project_handler.project_message(client_id, payload.get("text"))
