import socket

from values import IP_ADDRESS, SERVER_PORT
from get_time import get_time
from rdt import Server
from utils.ResponseTypes import ResponseTypes
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
    for user in users_list.values():
        user.addMessageToQueue(message)

def get_users_connect():
    users_list = userList.getList()
    table_str = '\nNOME         ||PORTA\n'
    table_str += '=======================================\n'
    for user in users_list.values():
        table_str += f"{user.getUserName().ljust(15)}{user.getUserAddress()[0]}:{user.getUserAddress()[1]}\n"
    return table_str

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
        server.send('Cadastrado com sucesso! Bem vindo', client_address)
    elif command == "list":
        server.send(get_users_connect(), client_address)
    elif command == "bye" and userIsRegistered:
        currentUser = userList.getUserByAddress(client_address)
        
        userList.removeUser(client_address)
        terminal_msg = f"{currentUser.getUserName()} saiu da sala!"
        terminal_msg = f"[server] {terminal_msg} {get_time()}"
        send_message_to_all(terminal_msg)
        server.send('conexao finalizada com sucesso', client_address)

    elif command == str(ResponseTypes.HAVE_NEW_MESSAGES.value):
        if userIsRegistered:
            clientNewMessage = userList.getUserByAddress(client_address).getNewMessage()
            server.send(clientNewMessage, client_address)
        else:
            server.send(str(ResponseTypes.NO_HAVE_MESSAGES.value), client_address)

    elif userIsRegistered:
        currentUser = userList.getUserByAddress(client_address).getUserObject()
        terminal_msg = f"{client_address[0]}:{client_address[1]}/~{currentUser['name']}: {command} {get_time()}"
        server.send(str(ResponseTypes.NO_HAVE_MESSAGES.value), client_address)
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
