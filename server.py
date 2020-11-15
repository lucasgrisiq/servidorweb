import socket
from WebServer import WebServer
import sys
import signal

def shutdownServer(sig, unused):
    """
    Shutsdown server from a SIGINT recieved signal
    """
    server.shutdown()
    sys.exit(1)

signal.signal(signal.SIGINT, shutdownServer)

server = WebServer(9999)
server.start()
