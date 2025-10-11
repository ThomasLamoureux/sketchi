import ServerCommunication.Pipeline as Pipeline


def connect(address):
    print("Connecting")
    connected = Pipeline.connect(address)

    if (connected == 1):
        print("connected")
        return 1
    else:
        return -1