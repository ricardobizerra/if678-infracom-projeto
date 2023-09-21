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

server = Server(sock) # Criação do objeto servidor, com protocolo RDT 3.0 embutido
sock.bind((IP_ADDRESS, SERVER_PORT))

userList = UserList() # Instanciamento da lista de usuários

# Função para adicionar uma mensagem na fila de mensagens de todos os usuários
def send_message_to_all(message):
    users_list = userList.getList()
    for user in users_list.values():
        user.addMessageToQueue(message)

# Função para retornar uma tabela com os usuários conectados (comando "list")
def get_users_connect():
    users_list = userList.getList()
    table_str = '\nNOME         ||PORTA\n'
    table_str += '=======================================\n'
    for user in users_list.values():
        table_str += f"{user.getUserName().ljust(15)}{user.getUserAddress()[0]}:{user.getUserAddress()[1]}\n"
    return table_str

# Função para tratar os comandos recebidos do usuário e retornar uma resposta adequada
def handle_user_input(command, client_address:str):
    # Verifica se o usuário já está cadastrado
    userIsRegistered = userList.userIdIsRegistered(client_address)

    # comando de registro de usuário
    if command.startswith("hi, meu nome eh") and not userIsRegistered:
        splitted_command = command.split(" ")
        new_user_name = splitted_command[-1]

        newUser = User(new_user_name, client_address)
        userList.addUser(newUser)

        terminal_msg = f"{newUser.getUserName()} entrou na sala!"
        terminal_msg = f"[server] {terminal_msg} {get_time()}"
        send_message_to_all(terminal_msg)
        server.send('Cadastrado com sucesso! Bem vindo', client_address)
    
    # comando de listagem de usuários
    elif command == "list":
        server.send(get_users_connect(), client_address)
    
    # comando de saída do usuário (comando "bye")
    elif command == "bye" and userIsRegistered:
        currentUser = userList.getUserByAddress(client_address)
        
        userList.removeUser(client_address)
        terminal_msg = f"{currentUser.getUserName()} saiu da sala!"
        terminal_msg = f"[server] {terminal_msg} {get_time()}"
        send_message_to_all(terminal_msg)
        server.send('conexao finalizada com sucesso', client_address)

    # tratar o aviso de nova mensagem
    elif command == str(ResponseTypes.HAVE_NEW_MESSAGES.value):

        # envia a nova mensagem para o usuário cadastrado
        if userIsRegistered:
            clientNewMessage = userList.getUserByAddress(client_address).getNewMessage()
            server.send(clientNewMessage, client_address)
        
        # avisa que não há novas mensagens
        else:
            server.send(str(ResponseTypes.NO_HAVE_MESSAGES.value), client_address)

    # não sendo nenhum dos comandos, é uma mensagem para ser enviada para todos os usuários
    elif userIsRegistered:
        currentUser = userList.getUserByAddress(client_address).getUserObject()
        terminal_msg = f"{client_address[0]}:{client_address[1]}/~{currentUser['name']}: {command} {get_time()}"
        server.send(str(ResponseTypes.NO_HAVE_MESSAGES.value), client_address)
        send_message_to_all(terminal_msg)
    
    # caso o usuário não esteja cadastrado, não é possível enviar mensagens
    else:
        server.send('cadastre-se para poder enviar mensagens', client_address)
    
    return True


def main():
    print(f"Server started! {get_time()}") # Mensagem de inicialização do servidor

    while True:
        command, client_address = server.receive()

        # gerenciamento de comandos recebidos do usuário
        if not handle_user_input(
            command=command,
            client_address=client_address,
        ):
            break


if __name__ == "__main__":
    main()
