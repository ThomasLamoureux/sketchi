import socket
import threading
import ServerCommunication.Formatter
import Login.ConnectToServerGUI
import ServerCommunication.Message_Handler as Message_Handler

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

            Message_Handler.message_recieved(client, msg)

        except:
            print("Connection closed by server.")
            client.close()
            break


def send_message(data_type, data):
    if not client:
        return
    message = Formatter.format_message(data_type, data)


    client.send(message.encode(ENCODING))




def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))

    # Start a thread to always listen for server messages
    thread = threading.Thread(target=message_listener, args=(client,))
    thread.daemon = True  # Kills thread when main program exits
    thread.start()



def connect(address):
    address, port = address.split(":")
    port = int(port)

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((address, port))
    except:
        return -1

        # Start a thread to always listen for server messages
    thread = threading.Thread(target=message_listener, args=(client,))
    thread.daemon = True  # Kills thread when main program exits
    thread.start()

    return 1

if __name__ == "__main__":
    connect(HOST + ":" + str(PORT))