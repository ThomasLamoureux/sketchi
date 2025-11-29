import Database.database as account
import Main.server as server
import asyncio


def login(client_id, username, password):
    print(f"Login attempt for user: {username}")
    result = account.login(username, password.encode("utf-8"))

    if result == 1:
        payload = {
            "msg_type": "login",
            "username": username,
            "success": True
        }

        asyncio.create_task(server.send_message(client_id, payload))
    else:
        payload = {
            "msg_type": "login",
            "success": False
        }
        asyncio.create_task(server.send_message(client_id, payload))



def sign_up(client_id, username, password):
    print("Signing up:", username)
    result = account.signup(username, password.encode("utf-8"))
    print("Signup result:", result)
    if result == 1:
        payload = {
            "msg_type": "signup",
            "username": username,
            "success": True
        }

        asyncio.create_task(server.send_message(client_id, payload))
    else:
        payload = {
            "msg_type": "signup",
            "success": False
        }
        asyncio.create_task(server.send_message(client_id, payload))