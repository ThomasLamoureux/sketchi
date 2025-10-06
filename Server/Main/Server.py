import socket
import threading
import Main.Online_Users as Online_Users

# Server configuration
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 12345      # Choose a port number > 1024


def user_connected(conn, address):
    Online_Users.add_user(conn, address)
    print("New connection:", address)

    try:
        while True:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break  # Client disconnected
            print(f"[{address}] {msg}")

            # Echo message back to all clients
            #for client in clients:
             #   if client != conn:
              #      client.sendall(f"{addr}: {msg}".encode("utf-8"))
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {address}")
        clients.remove(conn)
        conn.close()



def start_server():
    print("[STARTING] Server is starting...")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")


    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        print(f"Your computer's local IP address is: {ip_address}")
    except socket.gaierror:
        print("Could not resolve hostname to an IP address.")


    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=user_connected, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")