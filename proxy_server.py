from socket import *
import threading

# define server, ports and address
proxy_socket_port = 8888
http_socket_port = 8080
server = "localhost"
proxy_host = "127.1.1.0"
address_proxy = (proxy_host, proxy_socket_port)
address_http = (server, http_socket_port)

# create proxy server socket
proxy_server = socket(AF_INET, SOCK_STREAM)
proxy_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxy_server.bind((proxy_host, proxy_socket_port))

# this is our main method
# in this we listen socket and
# create thread for all request
def start():
    proxy_server.listen(100)
    while True:
        connection, address = proxy_server.accept()
        thread = threading.Thread(target=multithreading_proxy, args=(connection, address))
        thread.start()

# in this method we controlled necessary conditions
# if every conditions are true we accept request and
# return/send necessary response message
def multithreading_proxy(conn, addr):
    connected = True
    while connected:
        connection, address = proxy_server.accept()
        request = connection.recv(1024).decode()
        if (checkMethod(request) == "GET"  and checkPort(request) == "8080" and checkHostName(request) == "localhost"):
            print("Method Name --> " ,checkMethod(request))
            size = checkURISize(request)
            print("URI Size --> ", size)
            print(request)
            if(size != -1):
                try:
                    http_server_socket = socket(AF_INET, SOCK_STREAM)
                    http_server_socket.connect(address_http)
                    http_server_socket.sendall(request.encode())
                    http_response = http_server_socket.recv(100000).decode()
                    if (checkMethod(request) == "GET"):
                        print(http_response.encode())
                    connection.sendall((formatResponseDoc(http_response)).encode())
                except :
                    print("404 NOT FOUND!")
                connection.close()
                http_server_socket.close()
            else:
                print("ERROR CODE : 401 - REQUEST - URI TOO LONG")

# this method for response documents HTML format
def formatResponseDoc(response):
    title = ""
    if response[0:5] == "ERROR":
        title = response[0:16]
        response = response[19:]
    else:
        title = response[0:getTitle(response)]
        response = response[getTitle(response):]
        response = formatResponse(response)

    data = "HTTP/1.1 200 OK\r\n " \
           "Content-Type: text/html; " \
           "charset=utf-8\r\n\n" \
           "<html><head><title></title>" \
           "<h2>" + title + "</h2>\r\n" \
           "<body>" + response + "</body>" \
           "</head></html>\r\r\n"

    return data

# this method for request message's display type
def formatResponse(response):
    start = 0
    index = 0
    newResponse = ""
    for ch in response:
        if index % 212 == 0:
            newResponse += response[start:index] + "\n"
            start = index
        index += 1
    newResponse += response[start:]
    return newResponse

# this is for response's title
def getTitle(response):
    end = 0
    index = 0
    for ch in response:
        if (ch == "."):
            end = index + 1
            break
        index += 1
    return end

# this method controlled is request has GET method
def checkMethod(request):
    # GET request konrolü
    if request[0:3] == "GET" :
        isGETRequest = "GET"
    else :
        isGETRequest = -1
    return isGETRequest

# this method controlled is request has port number 8080 (true port)
def checkPort(request):
    port = request[21:25]
    if port == "8080":
        port = "8080"
    else:
        port = -1
    return port

# this method for check hostname is localhost
def checkHostName(request):
    hostName = request[11:20]
    if hostName == "localhost":
        hostName = "localhost"
    else:
        hostName = -1
    return hostName

# this method for URI size
def checkURISize(request):
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
    fileSize = request[start:end]

    if int(fileSize) > 9999 :
        fileSize = -1

    else:
        fileSize = fileSize
    return fileSize

print("[STARTING] proxy server is starting...")
#print('Access http://localhost:8888')
start()