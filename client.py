import socket
import threading

from values import IP_ADDRESS, SERVER_PORT
from rdt import Client

# Criação do socket -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

client = Client(sock)

print("olá! fique à vontade para me enviar comandos")

def receive_messages():
    while True:
        server_response, address = client.receive()
        print(server_response)

# Iniciar uma thread para receber mensagens do servidor em segundo plano
message_thread = threading.Thread(target=receive_messages)
message_thread.daemon = True  # Tornar a thread um daemon para que ela seja encerrada quando o programa principal terminar
message_thread.start()

def main():
    while True:
        comando = input("Digite um comando: ")
        client.send(comando, (IP_ADDRESS, SERVER_PORT))

if __name__ == "__main__":
    main()
