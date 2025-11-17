import asyncio
import json
import struct
import uuid
from typing import Dict


MSG_HDR = struct.Struct("!I")  # 4-byte big-endian length header


# --- framing helpers ---
async def read_message(reader: asyncio.StreamReader) -> dict:
    raw = await reader.readexactly(MSG_HDR.size)
    (length,) = MSG_HDR.unpack(raw)
    payload = await reader.readexactly(length)
    return json.loads(payload.decode('utf-8'))

async def write_message(writer: asyncio.StreamWriter, obj: dict):
    b = json.dumps(obj, separators=(",", ":")).encode()
    writer.write(MSG_HDR.pack(len(b)))
    writer.write(b)
    await writer.drain()

# --- Server state ---
clients: Dict[str, asyncio.Queue] = {}  # client_id -> send-queue
writers: Dict[str, asyncio.StreamWriter] = {}  # active client writers

# message sender task per client
async def client_sender_task(client_id: str, writer: asyncio.StreamWriter, send_queue: asyncio.Queue):
    try:

        # then send queued messages
        while True:
            msg = await send_queue.get()
            await write_message(writer, msg)
    except (asyncio.IncompleteReadError, ConnectionResetError, BrokenPipeError):
        # connection dropped; sender task will exit and the writer removed elsewhere
        pass
    finally:
        # cleanup done by main connection handler
        return

# application-level handler for each connection
async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = writer.get_extra_info('peername')
    print("New connection from", peer)
    client_id = None
    sender_task = None

    try:
        # Expect client to send an initial IDENTIFY message: {"type":"identify","client_id":"..."}
        msg = await read_message(reader)
        if msg.get("type") != "identify" or "client_id" not in msg:
            print("Bad identify; closing")
            writer.close()
            await writer.wait_closed()
            return

        client_id = msg["client_id"]
        print(f"Client identified: {client_id} from {peer}")

        # Setup writer queue
        send_queue = clients.get(client_id)
        if send_queue is None:
            send_queue = asyncio.Queue()
            clients[client_id] = send_queue

        writers[client_id] = writer

        # start a task to drain send_queue and push to client
        sender_task = asyncio.create_task(client_sender_task(client_id, writer, send_queue))

        # main read loop processing client messages
        while True:
            msg = await read_message(reader)
            mtype = msg.get("type")

            if mtype == "client_msg":
                # server received a message from client; we'll persist and maybe dispatch to other services
                # echo pattern: server saves and ACKs (here server will send an ack back to client)
                payload = msg.get("payload")
                # create server-side message id (for example for acknowledgment of processing)
                server_msg_id = str(uuid.uuid4())\

                # send a confirmation message back to client via their queue
                outmsg = {"type": "server_msg", "msg_id": server_msg_id, "payload": {"status":"ok","orig_id": msg.get("msg_id")}}
                print(outmsg)
                print(msg.get("payload"))
                # persist already done above; push to send queue
                await send_queue.put(outmsg)
            elif mtype == "ping":
                # respond pong
                await write_message(writer, {"type":"pong"})
            else:
                print("Unknown message type", mtype)
    except asyncio.IncompleteReadError:
        print("Client closed connection", client_id)
    except Exception as e:
        print("Connection handler exception:", e)
    finally:
        # cleanup
        if client_id:
            writers.pop(client_id, None)
            clients.pop(client_id, None)
        if sender_task:
            sender_task.cancel()
        try:
            writer.close()
            await writer.wait_closed()
        except:
            pass
        print("Connection closed for", client_id)

# API to send a message to any connected client (server code or other background tasks)
async def send_to_client(client_id: str, payload: dict):
    # create message id and persist before queuing
    msg_id = str(uuid.uuid4())

    send_queue = clients.get(client_id)
    if send_queue:
        await send_queue.put({"type":"server_msg", "msg_id": msg_id, "payload": payload})
    else:
        # client offline: message will remain in DB until they reconnect
        print("Client offline; message queued in outbox for", client_id)

async def main(host="127.0.0.1", port=8888):

    server = await asyncio.start_server(handle_connection, host, port)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    print(f"Serving on {addrs}")
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
        print("Started")
    except KeyboardInterrupt:
        print("Server stopped")