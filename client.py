import socket
import sys

soc = socket.socket()
port = 9999

data = 'GET / HTTP/1.1'.encode("utf-8")
TAM_PACOTE = 2048

try:
    soc.connect((socket.gethostname(), port))
    print("Conectado com server")
except Exception as e:
    print(e)
    sys.exit(1)

soc.send(data)

res = soc.recv(TAM_PACOTE)
res = res.decode("utf-8")
print(res)
soc.close()
sys.exit(1)
