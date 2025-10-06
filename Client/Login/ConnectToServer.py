import ServerCommunication.Pipeline as Pipeline


def connect(address):
    connected = Pipeline.connect(address)


    if (connected == 1):
        return 1
    else:
        return -1