import ServerCommunication.Client as Client


async def connect(address):
    host = address.split(":")[0]
    port = int(address.split(":")[1])
    connected = await Client.init(host, port)

    if (connected == 1):
        print("connected")
        return 1
    else:
        print("failed to connect")
        return -1