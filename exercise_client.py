import socket
import threading

chat_bot_logo = """
    \t     __ _ __ __ _ _
    \t       __ TEXT __
    \t         __ _
    \t         __
    \t
    \t         ||
    \t ________||
    \t| ______ o|
    \t|| xxxxx ||
    \t|| xxxxx ||
    \t||  TX   ||
    \t||  RX   ||
    \t||  U5   ||
    \t||_______||
    \t|'|[---]|'|
    \t| O  O  O |
    \t| O  O  O |
    \t| O  O  O |
    \t| O  O  O |
    \t| O  O  O |
    \t|_________|
    """

host = "127.0.0.1"
port = 9333

def recv_loop(sock):
    while True:
        try:
            data = sock.recv(2048).decode()
            if not data:
                break
            print("\n" + data)
        except Exception as error1:
            print(error1)
            break

client_socket = socket.socket()
client_socket.connect((host, port))

print(chat_bot_logo)
print(f"\nWelcome to ChatBot!\nPlease Verify your login details to join a chat.\n")
name = input("What is your name? ")
user = input(f"Hey {name}! Please enter your *USERNAME* > ")
password = input(f"\t\tPlease enter your *PASSWORD* for: [{user}] > ")

client_socket.send(f"{user}|{password}".encode())

reply = client_socket.recv(1024).decode()

while True:
    if reply != "OK":
        print("Your log-in details are incorrect.\nPlease try again.\n")
        raise SystemExit

    else:
        print(f"\nHey {user}! Welcome to the chat!\nPlease keep on respectful language... conversation has started!\n")
        break

t = threading.Thread(target=recv_loop, args=(client_socket,), daemon=True)
t.start()

while True:
    print("\n")
    msg = input("TYPE HERE > ")
    client_socket.send(msg.encode())
    if msg.lower().strip() == "q":
        break

client_socket.close()