import asyncio
import uuid
import Main.NewServer as Server

drawings = []


def draw(client_id, data):
    drawings.append(data)
    payload = {
        "msg_type": "draw",
        "drawing_data": data
    }

    asyncio.create_task(Server.send_message_all(payload, [client_id]))

def request_drawings(conn):
    for i in drawings:
        Server.send_message(conn, "draw", i)

    return


    if len(drawings) == 0:
        return

    
    Server.send_message(conn, "bulk_draw", drawings)


class PaintProject:
    def __init__(self, owner_id, password):
        self.drawings = []
        self.active_clients = []
        self.owner_id = owner_id
        self.project_id = uuid.uuid4()
        self.project_password = password

    
    def draw(self, client_id, data):
        if (client_id not in self.active_clients):
            return

        self.drawings.append(data)
        payload = {
            "msg_type": "draw",
            "drawing_data": data
        }

        asyncio.create_task(Server.send_message_all(payload, [client_id]))

    def change_owner(self, new_owner_id):
        self.owner_id = new_owner_id

    def add_client(self, client_id):
        if client_id not in self.active_clients:
            self.active_clients.append(client_id)



    def remove_client(self, client_id):
        if client_id in self.active_clients:
            self.active_clients.remove(client_id)


    async def request_drawings(self, client_id):
        for start in range(0, len(self.drawings), 50):
            data = self.drawings[start:start + 50]

            payload = {
                "msg_type": "bulk_draw",
                "drawing_data": data
            }

            asyncio.create_task(Server.send_message(client_id, payload))

            await asyncio.sleep(0.1) # prevent overload