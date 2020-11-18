import socket 
import sys
import time
import threading
import os
from datetime import datetime
import zlib

class WebServer(object):

    def __init__(self, port=8080, serverSize = 10):
        self.host = socket.gethostname() #salva o nome do host
        self.port = port #salva a porta atual
        self.dir_arquivos = 'public' #diretorio do arquivo
        self.serverSize = serverSize #numero maximo de clientes que podem esperar

    def run(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try: #tenta ligar um socket ao server
            self.soc.bind((self.host, self.port))
            print("Server na porta {porta}.".format(porta=self.port))
        except: #se nao conseguir ele desliga o server
            print("Erro: nao foi possivel conectar-se a porta {porta}".format(porta=self.port))
            self.shutdown()
            sys.exit(1)
        
        self.listen()

    
    def listen(self): #espera por clientes
        self.soc.listen(self.serverSize)
        while True:
            (cliente, addr) = self.soc.accept()
            print("Cliente conectado com endereco", addr)
            #dedica uma thread para atender um cliente
            threading.Thread(target=self.attend_cliente, args=(cliente, addr)).start()

    def shutdown(self):
        try:
            print("Fechando servidor")
            self.soc.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(e)
            pass

    def get_header(self, codigo_http, content_length, path = ''):
        header = 'HTTP/1.1 '
        #indica se ocorreu erro ou nao
        if codigo_http == 200:
            header += '200 OK\r\n'
        elif codigo_http == 404:
            header += '404 Not Found\r\n'
        elif codigo_http == 505:
            header += 'HTTP Version Not Supported\r\n'
        elif codigo_http == 400:
            header += 'Bad Request\r\n'
        #completa o header
        header += 'Server: Servidor da galera\r\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {data} GMT-3\r\n'.format(data=time_now)
        header += 'Content-Type: text/html\r\n'
        header += 'Content-Length {tam}\r\n'.format(tam=content_length)
        if path:
        	header += 'Last-Modified: ' + datetime.fromtimestamp(os.path.getmtime(self.dir_arquivos + path)).strftime("%a, %B %d, %Y %I:%M:%S") + ' GMT-3\r\n'

        header += 'Connection: close\r\n'
        header += '\r\n'
        return header


    def attend_cliente(self, cliente, addr): # recebe os dados do cliente e retorna o que foi pedido
        TAM_PACOTE = 2048

        while True:
            dados = cliente.recv(TAM_PACOTE).decode()

            if not dados: 
                res_header = self.get_header(400, 0)
                res = res_header.encode()
                cliente.send(res)
                cliente.close()
                break

            metodo_req = dados.split(' ')[0]
            print("Metodo:", metodo_req)
            print("Corpo:", dados)

            if metodo_req == "GET" or metodo_req == "HEAD":
                # checa versao solicitada 
                versao = dados.split(' ')[2]
                
                arq_solicitado = dados.split(' ')[1]

                # ignora parametro, caso haja
                arq_solicitado = arq_solicitado.split('?')[0]
                
                # index.html como arquivo default
                if arq_solicitado == "/":
                    arq_solicitado = "/index.html"
                
                path_arquivo = self.dir_arquivos + arq_solicitado

                # tenta abrir arquivos
                try:
                    f = open(path_arquivo, 'rb')
                    if metodo_req == "GET":
                        res_data = f.read().decode()
                    f.close()
                    tam = sys.getsizeof(res_data)
                    res_header = self.get_header(200, tam)
                
                # caso não haja o arquivo requisitado, responde com 404
                except Exception as e:
                    res_header = self.get_header(404, 0)
                    res_data = ''

                res = res_header
                if metodo_req == "GET":
                    res += res_data
                
                cliente.send(res.encode())
                cliente.close()
                break
            
            else:
                print("Metodo HTTP '{metodo}' nao existente.".format(metodo=metodo_req))
            







