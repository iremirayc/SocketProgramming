import socket
import threading

HEADER = 64
PORT = 8080 #  ?
#SERVER = "192.168.1.4"
SERVER = socket.gethostbyname(socket.gethostname()) # get IP address automatically
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
#print(SERVER)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create new socket
server.bind(ADDR)

# handle all communication between client and server
def handle_client(connection, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        message_length = connection.recv(HEADER).decode(FORMAT)
        message_length = int(message_length)
        message = connection.recv(message_length).decode(FORMAT)
        if message == DISCONNECT_MESSAGE:
            connected = False

        print(f"[{addr}] {message}")

    connection.close()

def start():
    server.listen(1)
    print (f"[LISTENING] Server is listening on {SERVER}")
    while True:
        connection, addr = server.accept()
        thread = threading.Thread(thread = handle_client, args = (connection, addr))
        thread.start()
        print (f"[ACTIVE CONNECTIONS {threading.activeCount() - 1}")  # ??



print(f"[STARTING] server is starting...")
start()



