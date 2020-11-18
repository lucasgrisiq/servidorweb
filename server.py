import socket
from WebServer import WebServer
import sys
import signal

def shutdownServer(sig, unused):
    #Fecha o server caso receba sinal
    server.shutdown()
    sys.exit(1)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, shutdownServer)

    server = WebServer(9999)
    server.run()