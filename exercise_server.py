import socket
import threading
from datetime import datetime

HOST = "0.0.0.0"
PORT = 9333
max_clients = 5

USERS_DB = {
    "OR360": "11111",
    "TOMER1207": "54321",
    "dan": "12345",
    "abagugu": "00000",
}

clients = {}
lock = threading.Lock()

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def broadcast(message: str, exclude_socket=None):
    data = message.encode()
    with lock:
        dead = []
        for u, s in clients.items():
            if exclude_socket is not None and s is exclude_socket:
                continue
            try:
                s.send(data)
            except Exception as error2:
                print(error2)
                dead.append(u)
        for u in dead:
            try:
                clients[u].close()
            except Exception as error3:
                print(error3)
                pass
            clients.pop(u, None)

def handle_client(client_socket: socket.socket, client_address):
    username = None
    try:
        login_data = client_socket.recv(1024).decode().strip()
        if "|" not in login_data:
            client_socket.send("FAIL".encode())
            client_socket.close()
            return

        username, password = login_data.split("|", 1)

        if USERS_DB.get(username) != password:
            client_socket.send("FAIL".encode())
            client_socket.close()
            return

        with lock:
            if username in clients:
                client_socket.send("FAIL".encode())
                client_socket.close()
                return
            clients[username] = client_socket
            current = len(clients)

        client_socket.send("OK".encode())
        broadcast(f"[{now_str()}] <{username}> joined the chat.")
        broadcast(f"\t☎ Online Users: {current}/{max_clients}")

        while True:
            msg = client_socket.recv(2048).decode()
            if not msg:
                break
            if msg.lower().strip() == "q":
                break
            broadcast(f"<{username}> {msg}")

    except Exception as error4:
        print(error4)
        pass

    finally:
        online_msg = None
        left_msg = None
        with lock:
            if username in clients:
                clients.pop(username, None)
                current = len(clients)
                left_msg = f"[{now_str()}] <{username}> left the chat."
                online_msg = f"\t☎ Online Users: {current}/{max_clients}"

        if left_msg:
            broadcast(left_msg)
            print(f"User Left: <{username}>")

        elif online_msg:
            broadcast(online_msg)
            print(f"User Joined: <{username}>")

        try:
            client_socket.close()
        except Exception as error10:
            print(error10)


server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen(5)

print(f"Server is listening on {HOST}:{PORT}\n")

while True:
    client_socket, client_address = server.accept()
    t = threading.Thread(target=handle_client, args=(client_socket, client_address), daemon=True)
    t.start()
