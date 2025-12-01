import Database.database as account
import Main.server as server
import asyncio

from Main import EmailVerification


def login(client_id, username, password):
    print(f"Login attempt for user: {username}")
    result = account.login(username, password.encode("utf-8"))

    if result == 1:
        payload = {
            "msg_type": "login",
            "username": username,
            "success": True
        }
        
        server.server.set_account(client_id, username)

        asyncio.create_task(server.send_message(client_id, payload))
    else:
        payload = {
            "msg_type": "login",
            "success": False
        }
        asyncio.create_task(server.send_message(client_id, payload))



def sign_up(client_id, username, email, password):
    print("Signing up:", username)
    result = account.signup(username, email, password.encode("utf-8"))
    print("Signup result:", result)
    if result == 1:
        payload = {
            "msg_type": "signup",
            "username": username,
            "success": True,
            "verification_on": EmailVerification.check_verification_enabled()
        }

        server.server.set_account(client_id, username)

        asyncio.create_task(server.send_message(client_id, payload))
    else:
        payload = {
            "msg_type": "signup",
            "success": False
        }
        asyncio.create_task(server.send_message(client_id, payload))


def verify_email_code(client_id, username, code):

    result = EmailVerification.verification_attempt(username, code)

    if result == 1:
        payload = {
            "msg_type": "verification_attempt",
            "success": True
        }

        asyncio.create_task(server.send_message(client_id, payload))
    else:
        payload = {
            "msg_type": "verification_attempt",
            "success": False
        }
        asyncio.create_task(server.send_message(client_id, payload))