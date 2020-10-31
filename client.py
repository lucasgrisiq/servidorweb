import socket

soc = socket.socket()
port = 10001

soc.connect((socket.gethostname(), port))

print (soc.recv(1024).decode("utf-8"))
soc.close()