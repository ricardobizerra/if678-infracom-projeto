import socket
import os
import threading
import time
from values import IP_ADDRESS, SERVER_PORT
from rdt import Client
from queue import Queue
from utils.ResponseTypes import ResponseTypes
import sys

# Criação do socket -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

client = Client(sock)

print("olá! fique à vontade para me enviar comandos")

client_lock = threading.Lock()

message_queue = Queue()

pause_event = threading.Event()

def print_server_response(server_response):
    if(server_response != str(ResponseTypes.NO_HAVE_MESSAGES.value)):
        print(f'{server_response}\n')

isConected = True

def messageListener():
    global isConected
    try:
        while isConected:
            while pause_event.is_set():
                time.sleep(1)

            with client_lock:
                client.send(str(ResponseTypes.HAVE_NEW_MESSAGES.value), (IP_ADDRESS, SERVER_PORT))
                server_response, address = client.receive()
                print_server_response(server_response)
            time.sleep(1)  
    except:
        sys.exit()


def sendMessage(comando):
    global isConected
    try:
        with client_lock:
            client.send(comando, (IP_ADDRESS, SERVER_PORT))
            server_response, address = client.receive()
            print_server_response(server_response)
            if server_response == "conexao finalizada com sucesso":
                isConected = False
                client.sock.close()
                sys.exit()
    except:
        isConected = False
        sys.exit()

def messageSender():
    global isConected
    while isConected:
        comando = input()
        message_queue.put(comando)

def main():
    global isConected
    threading.Thread(target=messageListener, daemon=True).start()
    threading.Thread(target=messageSender, daemon=False).start()

    while isConected:
        if not message_queue.empty():
            comando = message_queue.get()
            sendMessage(comando)
        time.sleep(1)
    
    sys.exit()


if __name__ == "__main__":
    main()
