import asyncio
import uuid
import Main.Main_Server as server


class PaintProject:
    def __init__(self, owner_id, owner_username, access_code = None):
        self.drawings = []
        self.active_clients = []
        self.owner_id = owner_id
        self.owner_username = owner_username
        self.project_id = uuid.uuid4()
        self.project_password = access_code
        self.messages = []

    
    def draw(self, client_id, data):
        print("Drawing data received from client:", client_id)
        if (client_id not in self.active_clients):
            return
        print("Made it")

        self.drawings.append(data)
        payload = {
            "msg_type": "draw",
            "drawing_data": data
        }

        send_clients = self.active_clients.copy()
        send_clients.remove(client_id)  
        asyncio.create_task(server.send_message_many(send_clients, payload))

    def change_owner(self, new_owner_id):
        self.owner_id = new_owner_id

    def add_client(self, client_id):
        if client_id not in self.active_clients:
            self.active_clients.append(client_id)

    def save_project(self):
        pass

    def remove_client(self, client_id):
        if client_id in self.active_clients:
            self.active_clients.remove(client_id)

    def request_join(self, access_code):
        if self.project_password == None:
            return True
        elif self.project_password == access_code:
            return True
        else:
            return False
        
    def clear_canvas(self, client_id):
        if client_id not in self.active_clients:
            return

        self.drawings = []

        payload = {
            "msg_type": "clear_canvas"
        }

        send_clients = self.active_clients.copy()
        send_clients.remove(client_id)

        asyncio.create_task(server.send_message_many(send_clients, payload))

    def project_message(self, client_id, text):
        payload = {
            "msg_type": "project_message",
            "text": text,
        }

        self.messages.append(text)

        send_clients = self.active_clients.copy()
        send_clients.remove(client_id)
        asyncio.create_task(server.send_message_many(send_clients, payload))


    async def request_drawings(self, client_id):
        for start in range(0, len(self.drawings), 50):
            data = self.drawings[start:start + 50]

            payload = {
                "msg_type": "bulk_draw",
                "drawing_data": data
            }

            asyncio.create_task(server.send_message(client_id, payload))

            await asyncio.sleep(0.03) # prevent overload

        payload = {
            "msg_type": "bulk_draw_complete"
        }
        asyncio.create_task(server.send_message(client_id, payload))