from socket import *

proxy_socket_port = 8888
http_socket_port = 8080
server = "localhost"
address_proxy = (server, proxy_socket_port)
address_http = (server, http_socket_port)
FORMAT = 'utf-8'

http_server = socket(AF_INET, SOCK_STREAM)
http_server.bind(address_http)


def start():
    http_server.listen(1)
    print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = http_server.accept()
        request = connection.recv(1024).decode()
        response = getResponseDoc(getRequest(request))
        connection.sendall((formatResponseDoc(response)).encode())


def getRequest(request):
    start = 0
    end = 0
    index = 0
    space = 0
    for ch in request:
        if (ch == "/"):
            start = index + 1
        if (ch == " "):
            space += 1
        if (space == 2):
            end = index
            break
        index += 1
    responseDocLength = request[start:end]
    return responseDocLength


def getResponseDoc(responseDocLength):
    size = 0
    responseDoc = ""
    if responseDocLength.isdecimal() == False:
        responseDoc = "404 NOT FOUND BAD REQUEST"
        return responseDoc
    if 100 > int(responseDocLength) > 20000:
        responseDoc = "ERROR"
        return responseDoc
    while size < int(responseDocLength):
        responseDoc += "a"
        size += 1
    return responseDoc

def formatResponseDoc(response):
    data = "HTTP/1.1 200 OK\r\n "
    data += "Content-Type: text/html; charset=utf-8\r\n"
    data += "\r\n"
    data += "<html><body>"
    data += response
    data += "</body></html>\r\n\r\n"
    return data

print("[STARTING] http server is starting...")
print('Access http://localhost:8080')
start()
