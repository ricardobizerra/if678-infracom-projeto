import socket
import os

from values import IP_ADDRESS, SERVER_PORT
from rdt import Client

# Criação do socket -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

client = Client(sock)

print("olá! fique à vontade para me enviar comandos")

def main():

    comando=input()
    registered = False
    user_name = ''

    while True:
        
        if comando.startswith("hi, meu nome eh") and not registered:
            splitted_command = comando.split(" ")
            new_user = splitted_command[-1]
            comando = ' '.join(splitted_command[:-1]) 
            
            message = f"{comando} | {new_user}"
            client.send(message, (IP_ADDRESS, SERVER_PORT))
            data, address = client.receive()
            print(data)

            registered = True
            user_name = new_user
        
        if registered:

            if comando == "bye":
                message = f"{comando} | {user_name}"
                client.send(message, (IP_ADDRESS, SERVER_PORT))
                data, address = client.receive()
                print(data)

                client.sock.close()
            
            else:
                message = f"{comando} | {user_name}"
                client.send(message, (IP_ADDRESS, SERVER_PORT))
                data, address = client.receive()
                print(data)

        comando = input()

if __name__ == "__main__":
    main()
