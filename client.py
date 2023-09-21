import socket
import threading
import time
import sys

from values import IP_ADDRESS, SERVER_PORT
from rdt import Client
from queue import Queue
from utils.ResponseTypes import ResponseTypes

# Criação do socket -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

client = Client(sock) # Criação do objeto cliente, com protocolo RDT 3.0 embutido

print("olá! fique à vontade para me enviar comandos")

# configuração de threads para envio e recebimento de mensagens
client_lock = threading.Lock() 
message_queue = Queue()

# função para printar o retorno de dados do servidor, excluindo o caso de não haver mensagens
def print_server_response(server_response):
    if(server_response != str(ResponseTypes.NO_HAVE_MESSAGES.value)):
        print(f'{server_response}\n')

isConected = True

def messageListener():
    global isConected
    try:
        while isConected:

            # envia uma mensagem para o servidor para verificar se há novas mensagens
            with client_lock:
                client.send(str(ResponseTypes.HAVE_NEW_MESSAGES.value), (IP_ADDRESS, SERVER_PORT))
                server_response, _ = client.receive()
                print_server_response(server_response)
            time.sleep(1)  
    except:
        sys.exit()


def sendMessage(comando):
    global isConected
    try:
        # envia uma mensagem para o servidor
        with client_lock:
            client.send(comando, (IP_ADDRESS, SERVER_PORT))
            server_response, address = client.receive()
            print_server_response(server_response)

            # caso o servidor retorne uma mensagem de finalização de conexão, o cliente é desconectado
            if server_response == "conexao finalizada com sucesso":
                isConected = False
                client.sock.close()
                sys.exit()
    except:
        isConected = False
        sys.exit()

# função para receber comandos do usuário e adiciona-los na fila de mensagens
def messageSender():
    global isConected
    while isConected:
        comando = input()
        message_queue.put(comando)

def main():
    global isConected
    threading.Thread(target=messageListener, daemon=True).start() # inicia a thread de recebimento de mensagens
    threading.Thread(target=messageSender, daemon=False).start() # inicia a thread de envio de mensagens

    while isConected:
        # verifica se há mensagens na fila de mensagens e envia para o servidor
        if not message_queue.empty():
            comando = message_queue.get()
            sendMessage(comando)
        time.sleep(1)
    
    sys.exit()


if __name__ == "__main__":
    main()
