import socket

from values import IP_ADDRESS, SERVER_PORT
from get_time import get_time
from rdt import Server

# Criação do socket e bind do servidor -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

server = Server(sock)
sock.bind((IP_ADDRESS, SERVER_PORT))

def handle_user_input(command, client_address, user_name):

    match(command):

        case "hi, meu nome eh":
            terminal_msg = f"{user_name} entrou na sala!"
            terminal_msg = f"[server] {terminal_msg} {get_time()}"
            server.send(terminal_msg, client_address)
            print(terminal_msg)

        case "bye":
            terminal_msg = f"{user_name} saiu da sala!"
            terminal_msg = f"[server] {terminal_msg} {get_time()}"
            server.send(terminal_msg, client_address)
            print(terminal_msg)
        
        case _:
            terminal_msg = f"{client_address[0]}:{client_address[1]}/~{user_name}: {command} {get_time()}"
            server.send(terminal_msg, client_address)
            print(terminal_msg)

    return True

def main():
    print(f"Server started! {get_time()}")

    while True:
        message, client_address = server.receive()
        
        command, user_name = message.split(" | ")

        if not handle_user_input(
            command=command,
            client_address=client_address,
            user_name=user_name
        ):
            break


if __name__ == "__main__":
    main()
