import ServerCommunication.Login as Login
import FrontEnd.gui as GUI

def recieved_message(payload: dict):
    

    msg_type = payload.get("msg_type")

    if msg_type == "login":
        success = payload.get("success")
        
        username = payload.get("username")
        Login.login_confirmation(success, username)

    elif msg_type == "signup":
        success = payload.get("success")

        username = payload.get("username")
        verification_required = payload.get("verification_on")
        Login.sign_up_confirmation(success, username, verification_required)
        
    elif msg_type == "draw":
        drawing_data = payload.get("drawing_data")
        GUI.app.artboard.manual_draw(drawing_data)

    elif msg_type == "verification_attempt":
        success = payload.get("success")
        GUI.app.verification_attempt_response(success)

    elif msg_type == "created_paint_project":
        access_code = payload.get("access_code")
        GUI.app.artboard.created_art_project(access_code)

    elif msg_type == "bulk_draw":
        drawing_data = payload.get("drawing_data")
        GUI.app.artboard.bulk_draw(drawing_data)

    elif msg_type == "join_art_project_response":
        success = payload.get("success")
        reason = payload.get("reason", None)
        GUI.app.artboard.join_art_project_response(success, reason)
