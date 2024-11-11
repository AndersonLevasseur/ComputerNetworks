from socket import *
from sys import argv
import time


serverName = argv[1]
serverPort = int(argv[2])
path   = "/"
if len(argv) == 4:
    path += argv[3]
clientSocket = socket(AF_INET, SOCK_STREAM)

print(f"Connecting to {serverName} at port {serverPort} requesting object at {path}")
clientSocket.connect((serverName,serverPort))
request = f"GET {path} HTTP/1.1\r\n"
request += f"Host: {serverName}\r\n\r\n"

clientSocket.send(request.encode())
time.sleep(1)
body_char = clientSocket.recv(1024)
response = body_char.decode()

while len(body_char) >= 1023:
    body_char = clientSocket.recv(1024)
    print(len(body_char))
    response += body_char.decode()

print('From Server: ', response)

clientSocket.close()
