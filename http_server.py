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
        connection.sendall((response).encode())


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
    isGETRequest = request[0:3]
    if (isGETRequest != "GET"):
        responseDocLength = "-1"
    return responseDocLength


def getResponseDoc(responseDocLength):
    size = 0
    responseDoc = ""
    if responseDocLength.isdecimal() == False:
        responseDoc = "ERROR CODE : 400 - BAD REQUEST"
    elif int(responseDocLength == -1):
        responseDoc = "ERROR CODE : 501 - NOT IMPLEMENTED"
    elif int(responseDocLength) < 100 or int(responseDocLength) > 20000:
        responseDoc = "ERROR CODE : 400 - BAD REQUEST"
    else:
        responseDoc = "I am " + responseDocLength + " bytes long."
        while size < int(responseDocLength):
            responseDoc += "a"
            size += 1
    return responseDoc


print("[STARTING] http server is starting...")
print('Access http://localhost:8080')
start()
