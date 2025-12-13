import asyncio
import secrets

from Main.canvas_project import PaintProject
import Main.Main_Server as server

active_projects: PaintProject = []



def draw(client_id, drawing_data):
    for project in active_projects:
        if client_id in project.active_clients:
            project.draw(client_id, drawing_data)
            return

def clear_canvas(client_id):
    for project in active_projects:
        if client_id in project.active_clients:
            project.clear_canvas(client_id)
            return

def new_paint_project(client_id, owner_username):
    access_code = secrets.token_hex(3).upper()

    project = PaintProject(client_id, owner_username, access_code)
    active_projects.append(project)

    payload = {
        "msg_type": "created_paint_project",
        "access_code": access_code
    }

    project.add_client(client_id)
    asyncio.create_task(server.send_message(client_id, payload))

def project_message(client_id, text):
    for project in active_projects:
        if client_id in project.active_clients:
            project.project_message(client_id, text)
            return


def join_art_project(client_id, owner, code):
    for project in active_projects:
        print(project.owner_username)
        if project.owner_username == owner:
            if project.request_join(code):
                print("Join attempt successful.")
                project.add_client(client_id)
                art_payload = {
                    "msg_type": "join_art_project_response",
                    "success": True
                }
                messages_payload = {
                    "msg_type": "all_project_messages",
                    "messages": project.messages
                }
                asyncio.create_task(server.send_message(client_id, art_payload))
                asyncio.create_task(server.send_message(client_id, messages_payload))
                asyncio.create_task(project.request_drawings(client_id))
                return True
            else:
                print("Join attempt failed: Incorrect access code.")
                payload = {
                    "msg_type": "join_art_project_response",
                    "success": False,
                    "reason": "Incorrect access code."
                }
                asyncio.create_task(server.send_message(client_id, payload))
                return
    else:
        print("Join attempt failed: No active project for that user.")
        payload = {
            "msg_type": "join_art_project_response",
            "success": False,
            "reason": "That user has no active project."
        }
        asyncio.create_task(server.send_message(client_id, payload))
        return