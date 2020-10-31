import socket

soc = socket.socket()
port = 10001

soc.bind(('', port))
soc.listen(0)

while True:
    client, adress = soc.accept()
    print(f'Conexão com {adress} estabelecida!')
    client.send('Hello World'.encode("utf-8"))
    client.close()

