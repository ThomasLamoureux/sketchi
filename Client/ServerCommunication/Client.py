import asyncio
import json
import struct
import uuid

import ServerCommunication.message_reciever as message_reciever
import FrontEnd.gui as GUI

MSG_HDR = struct.Struct("!I")  # 4-byte big-endian length prefix


Client = None

connection_request = None
host = None
port = None

connecting = False

class Client():
    def __init__(self, host, port):
        self.CLIENT_ID = str(uuid.uuid4())
        self.HOST = host
        self.PORT = port




    async def connect(self, reconnect = True):
        global connecting
        print(f"Connecting to {self.HOST}:{self.PORT} ...")
        while True:
            try:
                print("Trying to connect...")
                self.reader, self.writer = await asyncio.open_connection(self.HOST, self.PORT)
                print("Connected!")
                if reconnect == False:
                    
                    connecting = False
                    GUI.success_connection()

                # identify
                identify_msg = {"type": "identify", "client_id": self.CLIENT_ID}
                await self.write_message(self.writer, identify_msg)

                msg = {"type": "client_msg", "client_id": self.CLIENT_ID, "payload": {"text": "Hello, Server!"}}
                await self.write_message(self.writer, msg)

                asyncio.create_task(self.client_loop())


                break
            except Exception as e:
                if reconnect == False:
                    connecting = False
                    GUI.failed_connection()
                    break
                print("Connection error:", e)
                await asyncio.sleep(3)  # retry delay

    # --- framing helpers (same as server) ---
    async def read_message(self, h: asyncio.StreamReader) -> dict:
        raw = await self.reader.readexactly(MSG_HDR.size)
        (length,) = MSG_HDR.unpack(raw)
        payload = await self.reader.readexactly(length)
        return json.loads(payload.decode('utf-8'))

    async def write_message(self, h: asyncio.StreamWriter, obj: dict):
        b = json.dumps(obj, separators=(",", ":")).encode()
        self.writer.write(MSG_HDR.pack(len(b)))
        self.writer.write(b)
        await self.writer.drain()

    # --- message handlers ---
    async def handle_server_message(self, msg, writer):
        msg_id = msg.get("msg_id")
        payload = msg.get("payload")
        msg_type = payload.get("msg_type")
        print(msg_type)
        print(f"[SERVER MSG] id={msg_id} payload={payload}")


        message_reciever.recieved_message(payload)
        # Here you would process the payload (e.g. display to user, trigger logic)
        # Once processed successfully, send ACK:

        return
        if msg_id:
            ack = {"type": "ack", "msg_id": msg_id}
            await self.write_message(writer, ack)
            print(f"[ACK SENT] for {msg_id}")


    async def client_loop(self):
        while True:
            try:


                # start tasks: one reads incoming, one sends outgoing periodically
                async def read_task():
                    try:
                        while True:
                            msg = await self.read_message(self.reader)
                            print("Message received:", msg)
                            mtype = msg.get("type")
                            if mtype == "server_msg":
                                await self.handle_server_message(msg, self.writer)
                            elif mtype == "pong":
                                print("[PONG] from server")
                            else:
                                print("[INFO] from server:", msg)
                    except asyncio.IncompleteReadError:
                        print("Server closed connection.")
                    except Exception as e:
                        print("Read loop error:", e)


                reader_task = asyncio.create_task(read_task())

                # Keep running until disconnected
                await asyncio.wait([reader_task], return_when=asyncio.FIRST_COMPLETED)

                print("Connection lost, reconnecting soon...")
                #sender_task.cancel()
                self.writer.close()
                await self.writer.wait_closed()
                self.connect()

            except ConnectionRefusedError:
                print("Connection refused, retrying in 3s...")
            except Exception as e:
                print("Connection error:", e)

            await asyncio.sleep(3)  # retry delay


async def init(host, port):
    print("Initializing client...")
    global client
    
    client = Client(host, port)


    await client.connect(False)

send_queue = []

def send_message(payload, message_type="client_msg"):
    msg_id = str(uuid.uuid4())
    msg = {"type": message_type, "msg_id": msg_id, "payload": payload}

    send_queue.append(msg)



# This loop handles all message requests because gui loop will interfere with asyncio.
async def loop():
    global host_request
    global port_request
    global connection_request
    global connecting

    global send_queue

    while True:
        await asyncio.sleep(0.01)
        if connection_request == True:
            connection_request = False
            connecting = True

            host = str(host_request)
            port = int(port_request)

            await init(host, port)
        

        if len(send_queue) > 0:
            while len(send_queue) > 0:
                message = send_queue.pop(0)
                asyncio.create_task(client.write_message(client.writer, message))


# Requests a connection to the server.
def send_connection_request(host, port):
    global connection_request
    global host_request
    global port_request
    host_request = host
    port_request = port
    connection_request = True
