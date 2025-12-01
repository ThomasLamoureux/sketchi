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

        print(drawing_data)
        GUI.manual_draw(drawing_data)


