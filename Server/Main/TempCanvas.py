import asyncio
import Main.NewServer as Server

drawings = []


def draw(client_id, data):
    drawings.append(data)
    payload = {
        "msg_type": "draw",
        "drawing_data": data
    }
    print("YEs")
    asyncio.create_task(Server.send_message_all(payload, []))

def request_drawings(conn):
    for i in drawings:
        Server.send_message(conn, "draw", i)

    return


    if len(drawings) == 0:
        return

    
    Server.send_message(conn, "bulk_draw", drawings)