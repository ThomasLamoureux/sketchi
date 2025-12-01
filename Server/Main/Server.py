import asyncio
import json
import struct
import uuid
from typing import Dict

import Main.Message_Handler as message_handler
from Main.user_account import UserAccount


server = None


class Server():

    def __init__(self):
        pass


    async def start(self, host, port):
        self.clients: Dict[str, asyncio.Queue] = {}  # client_id -> send-queue
        self.writers: Dict[str, asyncio.StreamWriter] = {}  # active client writers
        self.accounts: Dict[str, UserAccount] = {}  # client_id -> account info

        self.MSG_HDR = struct.Struct("!I")  # 4-byte big-endian length header

        server = await asyncio.start_server(self.handle_connection, host, port)
        addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
        print(f"Serving on {addrs}")
        import socket

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print("Local IP:", ip)
        async with server:
            await server.serve_forever()



    async def read_message(self, reader: asyncio.StreamReader) -> dict:
        raw = await reader.readexactly(self.MSG_HDR.size)
        (length,) = self.MSG_HDR.unpack(raw)
        payload = await reader.readexactly(length)
        return json.loads(payload.decode('utf-8'))
    
    
    async def write_message(self, writer: asyncio.StreamWriter, obj: dict):
        b = json.dumps(obj, separators=(",", ":")).encode()
        writer.write(self.MSG_HDR.pack(len(b)))
        writer.write(b)
        await writer.drain()


    # message sender task per client
    async def client_sender_task(self, client_id: str, writer: asyncio.StreamWriter, send_queue: asyncio.Queue):
        try:

            # then send queued messages
            while True:
                msg = await send_queue.get()
                await self.write_message(writer, msg)
        except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
            # connection dropped; sender task will exit and the writer removed elsewhere
            pass
        finally:
            # cleanup done by main connection handler
            return

     #application-level handler for each connection
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        peer = writer.get_extra_info('peername')
        print("New connection from", peer)
        client_id = None
        sender_task = None

        try:
            # Expect client to send an initial IDENTIFY message: {"type":"identify","client_id":"..."}
            msg = await self.read_message(reader)
            if msg.get("type") != "identify" or "client_id" not in msg:
                print("Bad identify; closing")
                writer.close()
                await writer.wait_closed()
                return

            client_id = msg["client_id"]
            print(f"Client identified: {client_id} from {peer}")

            # Setup writer queue
            send_queue = self.clients.get(client_id)
            if send_queue == None:
                send_queue = asyncio.Queue()
                self.clients[client_id] = send_queue
                self.accounts[client_id] = None

            self.writers[client_id] = writer

            # start a task to drain send_queue and push to client
            sender_task = asyncio.create_task(self.client_sender_task(client_id, writer, send_queue))

            # main read loop processing client messages
            while True:
                msg = await self.read_message(reader)
                mtype = msg.get("type")

                try:
                    if mtype == "client_msg":
                        payload: dict = msg.get("payload")
                        msgtype = payload.get("msg_type")
                        # create server-side message id (for example for acknowledgment of processing)
                        server_msg_id = str(uuid.uuid4())
                    
                        message_handler.message_recieved(client_id, msgtype, payload)

                        # send a confirmation message back to client via their queue
                        #outmsg = {"type": "server_msg", "msg_id": server_msg_id, "payload": {"status":"ok","orig_id": msg.get("msg_id")}}

                        print(payload)

                        #await send_queue.put(outmsg)
                    else:
                        print("Unknown message type", mtype)
                except Exception as e:
                    print("Message handling exception:", e)
                    
        except asyncio.IncompleteReadError:
            print("Client closed connection", client_id)
        except Exception as e:
            print("Connection handler exception:", e)
        finally:
            # cleanup
            if client_id:
                self.writers.pop(client_id, None)
                self.clients.pop(client_id, None)
                self.accounts.pop(client_id, None)
            if sender_task:
                sender_task.cancel()
            try:
                writer.close()
                await writer.wait_closed()
            except:
                pass
            print("Connection closed for", client_id)
            
    # API to send a message to any connected client (server code or other background tasks)
    async def send_to_client(self, client_id: str, payload: dict):
        # create message id and persist before queuing
        msg_id = str(uuid.uuid4())

        send_queue = self.clients.get(client_id)
        if send_queue:
            await send_queue.put({"type":"server_msg", "msg_id": msg_id, "payload": payload})
        else:
            # client offline: message will remain in DB until they reconnect
            print("Client offline; message queued in outbox for", client_id)

    async def send_many_clients(self, client_ids: list, payload: dict):
        for client_id in client_ids:
            msg_id = str(uuid.uuid4())
            send_queue = self.clients.get(client_id)
            if send_queue:
                await send_queue.put({"type":"server_msg", "msg_id": msg_id, "payload": payload})


    async def send_all_clients(self, payload: dict, exceptions: list):
        for client_id, send_queue in self.clients.items():
            print(client_id)
            if client_id in exceptions:
                continue
            msg_id = str(uuid.uuid4())
            await send_queue.put({"type":"server_msg", "msg_id": msg_id, "payload": payload})

    def set_account(self, client_id: str, username: str):
        self.accounts[client_id] = UserAccount(client_id, username)


# Globally accessible function for sending messages
async def send_message(client_id, payload):
    await server.send_to_client(client_id, payload)

async def send_message_all(payload, exceptions):
    await server.send_all_clients(payload, exceptions)

async def send_message_many(client_ids, payload):
    await server.send_many_clients(client_ids, payload)



def start_server():
    global server
    try:
        server = Server()
        def run(): # I don't know why I have this as a method but its probably important
            asyncio.run(server.start("0.0.0.0", 6700))
            print("Started")
        run()

    except KeyboardInterrupt:
        print("Server stopped")


if __name__ == "__main__":
    start_server()




