import ServerCommunication.Formatter as Formatter
import FrontEnd.Main as GUI
import Login.Login as Login


def message_recieved(conn, message):
    print(message)
    msg_type, data = Formatter.decode(message)

    print(msg_type, data)


    if msg_type == "login":
        print("Recieved, login")
        Login.login_confirmation(data)
    elif msg_type == "signup":
        print("Recieved, signup")
        Login.sign_up_confirmation(data)
    elif msg_type == "draw":
        
        result = []
        temp = []

        for item in data:
            # Remove parentheses if present
            clean = item.replace("(", "").replace(")", "")
            
            if "(" in item:  # start of a tuple
                temp = [int(clean)]
            elif ")" in item:  # end of a tuple
                temp.append(int(clean))
                result.append(tuple(temp))
                temp = []
            elif temp:  # inside a tuple
                temp.append(int(clean))
            else:  # standalone number
                result.append(int(clean))


        GUI.manual_draw(result)


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
