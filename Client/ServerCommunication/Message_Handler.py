import FrontEnd.gui as GUI
import Client.ServerCommunication.Login as Login


def message_recieved(msg_type, payload: dict):

    if msg_type == "login":
        print("Recieved, login")

        success = payload.get("success")
        
        username = payload.get("username")
        Login.login_confirmation(success, username)

    elif msg_type == "signup":
        print("Recieved, signup")

        success = payload.get("success")

        username = payload.get("username")
        Login.sign_up_confirmation(success, username)
        
    elif msg_type == "draw":
        drawing_data = payload.get("drawing_data")

        print(drawing_data)
        GUI.manual_draw(drawing_data)


    elif msg_type == "bulk_draw":
        def parse_list(sublist):
            result = []
            temp = []
            for item in sublist:
                clean = item.replace("(", "").replace(")", "")
                if "(" in item:
                    temp = [int(clean)]
                elif ")" in item:
                    temp.append(int(clean))
                    result.append(tuple(temp))
                    temp = []
                elif temp:
                    temp.append(int(clean))
                else:
                    result.append(int(clean))
            return result

        # Apply the parser to each sublist
        final_result = [parse_list(sublist) for sublist in data]


        GUI.bulk_draw(final_result)
