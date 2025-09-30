import socket
import threading

# Server configuration
HOST = "0.0.0.0"  # Listen on all available network interfaces
PORT = 12345      # Choose a port number > 1024

# List to keep track of connected clients
clients = []

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    clients.append(conn)

    try:
        while True:
            msg = conn.recv(1024).decode("utf-8")
            if not msg:
                break  # Client disconnected
            print(f"[{addr}] {msg}")

            # Echo message back to all clients
            for client in clients:
                if client != conn:
                    client.sendall(f"{addr}: {msg}".encode("utf-8"))
    except ConnectionResetError:
        pass
    finally:
        print(f"[DISCONNECTED] {addr}")
        clients.remove(conn)
        conn.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()