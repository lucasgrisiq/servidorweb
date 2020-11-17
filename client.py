import socket
import sys

if __name__ == "__main__":
    soc = socket.socket() #cria socket
    port = 9999 #escolhe a porta

    data = 'GET / HTTP/1.1'.encode("utf-8")
    TAM_PACOTE = 2048

    try: #tenta se conectar com o server
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
