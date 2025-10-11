import Main.Server as Server

drawings = []


def draw(conn, data):
    drawings.append(data)

    Server.send_message_all("draw", data, [conn])



def request_drawings(conn):
    for i in drawings:
        Server.send_message(conn, "draw", i)

    return

    print(drawings)
    if len(drawings) == 0:
        return

    
    Server.send_message(conn, "bulk_draw", drawings)