import socket


HOST = "127.0.0.1"

PORT = 60001


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.bind((HOST, PORT))
    soc.listen()

    connection, address = soc.accept()


    with connection:
        print("Connected through " + str(address))


        while True:
            data = connection.recv(1024)

            if not data:
                break
            connection.sendall(data)
