from socket import *

proxy_socket_port = 8888
http_socket_port = 8080
server = "localhost"
address_proxy = (server, proxy_socket_port)
address_http = (server, http_socket_port)

proxy_server = socket(AF_INET, SOCK_STREAM)
proxy_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxy_server.bind((server, proxy_socket_port))


def start():
    proxy_server.listen(10)
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = proxy_server.accept()
        request = connection.recv(1024).decode()
        try:
            http_server_socket = socket(AF_INET, SOCK_STREAM)
            http_server_socket.connect(address_http)
            http_server_socket.sendall(request.encode())
            http_response = http_server_socket.recv(1024).decode()
            print(http_response.encode())
            connection.sendall((formatResponseDoc(http_response)).encode())

        except:
            print("ksdfhsjdks")

        connection.close()
        http_server_socket.close()



def formatResponseDoc(response):
    data = "HTTP/1.1 200 OK\r\n\n "
    data += "Content-Type: text/html; charset=utf-8\r\n\n"
    data += "\r\n\n"
    data += "<html><body>"
    data += response
    data += "</body></html>\r\n\r\n"
    return data


print("[STARTING] proxy server is starting...")
print('Access http://localhost:8888')
start()
