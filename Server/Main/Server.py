import socket
import threading
import Main.Online_Users as Online_Users
import Main.Message_Handler as Message_Handler
import Main.Formatter as Formatter

# Server configuration
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 5005      # Choose a port number > 1024


def user_connected(conn, address):
    Online_Users.add_user(conn, address)
    print("New connection:", address)

    try:
        while True:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break  # Client disconnected

            # Echo message back to all clients
            #for client in clients:
             #   if client != conn:
              #      client.sendall(f"{addr}: {msg}".encode("utf-8"))

            Message_Handler.message_recieved(conn, address, msg)
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {address}")
        Online_Users.remove_user(conn)
        conn.close()


def send_message_all(data_type, data, exceptions):
    msg = Formatter.format_message(data_type, data)

    for i in Online_Users.get_all():
        try:
            conn = i.get_connection()
            if conn in exceptions:
                continue

            i.get_connection().sendall(msg)
        except:
            print("Error sending")


def send_message(conn, data_type, data):
    msg = Formatter.format_message(data_type, data)

    try:
        conn.sendall(msg)
    except:
        print("failed")


def start_server():
    print("[STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")


    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Your computer's local IP address is: {ip_address}, port number is: {PORT}")
    except socket.gaierror:
        print("Could not resolve hostname to an IP address.")


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=user_connected, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")