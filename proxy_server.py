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
            http_response = http_server_socket.recv(100000).decode()
            print(http_response.encode())
            connection.sendall((formatResponseDoc(http_response)).encode())

        except:
            print("ksdfhsjdks")

        connection.close()
        http_server_socket.close()


def formatResponseDoc(response):
    title = ""
    if response[0:5] == "ERROR":
        title = response[0:16]
        response = response[19:]
    else:
        title = response[0:getTitle(response)]
        response = response[getTitle(response):]
        response = formatResponse(response)
    data = "HTTP/1.1 200 OK\r\n Content-Type: text/html; charset=utf-8\r\n\n<html><head><title></title><h2>" + title + "</h2>\r\n<body>" + response + "</body></head></html>\r\r\n"
    return data


def formatResponse(response):
    start = 0
    index = 0
    newResponse = ""
    for ch in response:
        if index % 100 == 0:
            newResponse += response[start:index] + "\n"
            start = index
        index += 1
    newResponse += response[start:]
    return newResponse


def getTitle(response):
    end = 0
    index = 0
    for ch in response:
        if (ch == "."):
            end = index + 1
            break
        index += 1
    return end


print("[STARTING] proxy server is starting...")
print('Access http://localhost:8888')
start()
