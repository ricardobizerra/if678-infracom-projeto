import socket

from values import IP_ADDRESS, SERVER_PORT
from get_time import get_time
from rdt import Server

from utils.User import User
from utils.UserList import UserList

# Criação do socket e bind do servidor -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

server = Server(sock)
sock.bind((IP_ADDRESS, SERVER_PORT))

userList = UserList()

def send_message_to_all(message):
    users_list = userList.getList()
    print(message)
    for user in users_list.values():
        server.send(message, user.getUserObject()['address'])



def handle_user_input(command, client_address:str):

    userIsRegistered = userList.userIdIsRegistered(client_address)
    if command.startswith("hi, meu nome eh") and not userIsRegistered:
        splitted_command = command.split(" ")
        new_user_name = splitted_command[-1]

        newUser = User(new_user_name, client_address)
        userList.addUser(newUser)

        terminal_msg = f"{newUser.getUserName()} entrou na sala!"
        terminal_msg = f"[server] {terminal_msg} {get_time()}"
       
        send_message_to_all(terminal_msg)

    elif command == "bye" and userIsRegistered:
        currentUser = userList.getUserByAddress(client_address)
        
        userList.removeUser(client_address)
        terminal_msg = f"{currentUser.getUserName()} saiu da sala!"
        terminal_msg = f"[server] {terminal_msg} {get_time()}"
        send_message_to_all(terminal_msg)

    elif userIsRegistered:
        currentUser = userList.getUserByAddress(client_address).getUserObject()
        terminal_msg = f"{client_address[0]}:{client_address[1]}/~{currentUser['name']}: {command} {get_time()}"
        send_message_to_all(terminal_msg)
    else:
        server.send('cadastre-se para poder enviar mensagens', client_address)

    return True


def main():
    print(f"Server started! {get_time()}")

    while True:
        command, client_address = server.receive()
        if not handle_user_input(
            command=command,
            client_address=client_address,
        ):
            break


if __name__ == "__main__":
    main()



# import socket
# import os

# from values import IP_ADDRESS, SERVER_PORT
# from rdt import Client

# # Criação do socket -> de acordo com o UDP
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

# client = Client(sock)

# print("olá! fique à vontade para me enviar comandos")

# def main():

#     comando=input()
#     registered = False
#     user_name = ''

#     while True:
        
#         if comando.startswith("hi, meu nome eh") and not registered:
#             splitted_command = comando.split(" ")
#             new_user = splitted_command[-1]
#             comando = ' '.join(splitted_command[:-1]) 
            
#             message = f"{comando} | {new_user}"
#             client.send(message, (IP_ADDRESS, SERVER_PORT))
#             data, address = client.receive()
#             print(data)

#             registered = True
#             user_name = new_user
        
#         if registered:

#             if comando == "bye":
#                 message = f"{comando} | {user_name}"
#                 client.send(message, (IP_ADDRESS, SERVER_PORT))
#                 data, address = client.receive()
#                 print(data)

#                 client.sock.close()
            
#             else:
#                 message = f"{comando} | {user_name}"
#                 client.send(message, (IP_ADDRESS, SERVER_PORT))
#                 data, address = client.receive()
#                 print(data)

#         comando = input()

# if __name__ == "__main__":
#     main()
