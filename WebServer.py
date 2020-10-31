import socket 
import sys
import time
import threading

class WebServer(object):

    def __init__(self, port=8080):
        self.host = socket.gethostname()    
        self.port = port
        self.dir_arquivos = 'public'

    def start(self):
        self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.soc.bind((self.host, self.port))
            print("Server na porta {porta}.".format(porta=self.port))
        except Exception as e:
            print("Erro: nao foi possivel conectar-se a porta {porta}".format(porta=self.port))
            self.shutdown()
            sys.exit(1)
        
        self._listen()

    
    def _listen(self):
        self.soc.listen(5)
        while True:
            (cliente, addr) = self.soc.accept()
            print("Cliente conectado com endereco", addr)
            threading.Thread(target=self._recebe_cliente, args=(cliente, addr)).start()

    def shutdown(self):
        try:
            print("Fechando servidor")
            self.soc.shutdown(socket.SHUT_RDWR)
        except Exception as e:
            print(e)
            pass

    def _gera_headers(self, codigo_http, content_length):
        header = 'HTTP/1.1 '

        if codigo_http == 200:
            header += '200 OK\r\n'
        elif codigo_http == 404:
            header += '404 Not Found\r\n'
        elif codigo_http == 505:
            header += 'HTTP Version Not Supported\r\n'
        elif codigo_http == 400:
            header += 'Bad Request\r\n'
        
        header += 'Server: Servidor da galera\r\n'
        time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
        header += 'Date: {data}\r\n'.format(data=time_now)
        header += 'Content-Type: text/html\r\n'
        header += 'Content-Length {tam}\r\n'.format(tam=content_length)
        header += 'Connection: close\r\n'
        header += '\r\n'
        return header


    def _recebe_cliente(self, cliente, addr):
        TAM_PACOTE = 2048

        while True:
            dados = cliente.recv(TAM_PACOTE).decode() 

            if not dados: 
                res_header = self._gera_headers(400, 0)
                res = res_header.encode("utf-8")
                cliente.send(res)
                cliente.close()
                break
            
            metodo_req = dados.split(' ')[0]
            print("Metodo:", metodo_req)
            print("Corpo:", dados)

            if metodo_req == "GET" or metodo_req == "HEAD":
                # checa versao solicitada 
                versao = dados.split(' ')[2]
                if versao != "HTTP/1.1":
                    res_header = self._gera_headers(505, 0)
                    res_data = ''
                
                else:
                    arq_solicitado = dados.split(' ')[1]

                    # ignora parametro, caso haja
                    arq_solicitado = arq_solicitado.split('?')[0]
                    
                    # index.html como arquivo default
                    if arq_solicitado == "/":
                        arq_solicitado = "/index.html"
                    
                    path_arquivo = self.dir_arquivos + arq_solicitado

                    # tenta abrir arquivos
                    try:
                        f = open(path_arquivo, 'r')
                        if metodo_req == "GET":
                            res_data = f.read()
                        f.close()
                        tam = sys.getsizeof(res_data)
                        res_header = self._gera_headers(200, tam)
                    
                    # caso não haja o arquivo requisitado, responde com 404
                    except Exception as e:
                        if metodo_req == "GET":
                            f = open(self.dir_arquivos+"404.html", 'rb')
                            res_data = f.read()
                            f.close()
                        
                        tam = sys.getsizeof(res_data)
                        res_header = self._gera_headers(404, tam)

                res = res_header.encode("utf-8")
                if metodo_req == "GET":
                    res += res_data.encode("utf-8")
                
                cliente.send(res)
                cliente.close()
                break
            
            else:
                print("Metodo HTTP '{metodo}' nao existente.".format(metodo=metodo_req))
            







