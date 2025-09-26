import socket

HOST = "127.0.0.1"
PORT = 60001


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
    soc.connect((HOST, PORT))


    soc.sendall(b"Hey")

    data = soc.recv(1024)


print(data)