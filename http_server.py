import threading
from socket import *

# define server, ports and address
proxy_socket_port = 8888
http_socket_port = 8080
server = "localhost"
address_proxy = (server, proxy_socket_port)
address_http = (server, http_socket_port)
FORMAT = 'utf-8'

http_server = socket(AF_INET, SOCK_STREAM)
http_server.bind(address_http)

# main method in this method we listen socket and
# create thread for multithreading
def start():
    http_server.listen(100)
    #print(f"[LISTENING] Server is listening on {server}")
    while True:
        connection, address = http_server.accept()
        thread = threading.Thread(target=multithreading_http, args=(connection, address))
        thread.start()

# in this method we recv request and we return
# necessary response message
def multithreading_http(conn,addr):
    connected = True
    while connected:
        request = conn.recv(1024).decode(FORMAT)
        response = getResponseDoc(getRequest(request))
        conn.sendall((response).encode())

        conn.close()

# this is for take request and find necessary
# response document length
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


# this method for return necessary message
# for taken response length. Also if every
# condition are true response message returns
# #letter A as long as response document.
def getResponseDoc(responseDocLength):
    size = 0
    responseDoc = ""
    if responseDocLength.isdecimal() == False:
        responseDoc = "ERROR CODE : 400 - BAD REQUEST"
    elif int(responseDocLength == -1):
        responseDoc = "ERROR CODE : 501 - NOT IMPLEMENTED"
    elif int(responseDocLength) < 100 or int(responseDocLength) > 20000:
        responseDoc = "ERROR CODE : 400 - BAD REQUEST"
    elif int(responseDocLength) == -1:
        responseDoc = "ERROR CODE : 401 - REQUEST - URI TOO LONG"
    else:
        responseDoc = "I am " + responseDocLength + " bytes long."
        while size < int(responseDocLength):
            responseDoc += "a"
            size += 1
    return responseDoc


print("[STARTING] http server is starting...")
print('Access http://localhost:8080')
start()
