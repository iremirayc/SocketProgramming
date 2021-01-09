from socket import *
import threading

HEADER = 1024
PORT = 8080
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket(AF_INET, SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        (clientsocket, address) = server.accept()

        rd = clientsocket.recv(5000).decode()
        pieces = rd.split("\n")
        if (len(pieces) > 0): print(pieces[0])

        data = "HTTP/1.1 200 OK\r\n"
        data += "Content-Type: text/html; charset=utf-8\r\n"
        data += "\r\n"
        data += "<html><body>Hello World</body></html>\r\n\r\n"
        clientsocket.sendall(data.encode())
        clientsocket.shutdown(SHUT_WR)
    conn.close()


def start():
    server.listen(100)
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
print('Access http://localhost:9000')
start()