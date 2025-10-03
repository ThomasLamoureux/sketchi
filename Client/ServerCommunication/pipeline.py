import socket
import threading
import Formatter

HOST = "127.0.0.1"  # Change to server IP if not local
PORT = 12345
ENCODING = "utf-8"

client = None



def message_listener(client):
    #Continuously listen for messages from the server.
    while True:
        try:
            msg = client.recv(1024).decode(ENCODING)
            if not msg:
                break
            print(f"\n{msg}")  # Print server/broadcasted messages
            print(msg)
        except:
            print("Connection closed by server.")
            client.close()
            break


def send_message(data_type, data):
    message = Formatter.format_message(data_type, data)


    client.send(message.encode(ENCODING))




def recieve_message(data):
    pass


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start a thread to always listen for server messages
    thread = threading.Thread(target=message_listener, args=(client,))
    thread.daemon = True  # Kills thread when main program exits
    thread.start()

    print("Connected to server. You can start chatting!")
    while True:
        msg = input(": ")  # Take user input
        if msg.lower() == "/quit":
            client.close()
            break
        client.send(msg.encode(ENCODING))

if __name__ == "__main__":
    main()