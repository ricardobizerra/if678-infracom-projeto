import socket
import os

#from values import BUFFER_SIZE, IP_ADDRESS, SERVER_PORT, CLIENT_BASE_PORT
from rdt import Client

# Criação do socket -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR

client = Client(sock)

print("olá! fique à vontade para me enviar comandos")

def main():
    # Basta adicionar os arquivos a serem transferidos aqui, apenas lembre-se de que deve estar na mesma pasta do client.py
    #os.makedirs('client/received')
    #files = ["client/sent/file.txt", "client/sent/image.jpg"]
    #send_files(files)
    #receive_files()

    comando=input()
    number_users = 0

    while True:
        if comando.startswith("hi, meu nome eh"):
            new_user = comando.split("hi, meu nome eh ")[1]

            print(f"Ola, {new_user}!")
            number_users += 1
            port_number = 8081 + number_users
            print(f"connected to port {port_number}")
            sock.bind(("localhost", 8081 + number_users))

            comando = input()




# Envio dos arquivos pelo cliente
# def send_files(files):
#     # Configuração de servidor e buffer size (tamnho dos pacotes)
#     host = "localhost"
#     port = 8080
#     buffer_size = 1024

#     # Sinais de término de envio de arquivos (SEND_FINISHED) e de envio de um arquivo (FILE_FINISHED)
#     SEND_FINISHED = b"<<sendFinished>>"
#     FILE_FINISHED = b"<<fileFinished>>"

#     # Loop que permite o envio de vários arquivos
#     for file_path in files:
#         file_size = os.path.getsize(file_path) # Obtém o tamanho do arquivo
#         filename = file_path.split('/')[-1]

#         sock.sendto(filename.encode(), (host, port)) # Envia o nome do arquivo
#         sock.sendto(str(file_size).encode(), (host, port)) # Envia o tamanho do arquivo

#         # Abre o arquivo para carregar seus dados
#         with open(file_path, "rb") as f:
#             data = f.read(buffer_size) # Lê os dados que vão compor o 1º pacote (buffer_size bytes)

#             # Loop que permite o envio de vários pacotes, enquanto houver dados
#             while data:
#                 sock.sendto(data, (host, port))
#                 data = f.read(buffer_size)
        
#         sock.sendto(FILE_FINISHED, (host, port)) # Sinal de término de envio do arquivo

#     print("Files sent!\n")
#     sock.sendto(SEND_FINISHED, (host, port)) # Sinal de término de envio de todos os arquivos

# def receive_files():
#     print("Client waiting files...\n\n")
#     buffer_size = 1024

#     FILE_FINISHED = b"<<fileFinished>>"
#     SEND_FINISHED = b"<<sendFinished>>"

#     receiving_files = True
#     while receiving_files:
#         file, address = sock.recvfrom(buffer_size)

#         # Encerra o recebimento de arquivos
#         if file == SEND_FINISHED:
#             receiving_files = False
#             print("All files received!")
#         else:
#             file = file.decode()  # Decodifica o nome do arquivo
#             file_path = f"client/received/server_response_{file}"  # Cria o nome do arquivo de recebimento
#             filename = file_path.split('/')[-1]
#             file_size, address = sock.recvfrom(buffer_size)
#             file_size = int(file_size.decode())  # Decodifica o tamanho do arquivo

#             data = b""  # Início da leitura dos dados do arquivo

#             # Loop que permite a leitura dos dados do arquivo, subdividindo-o em pacotes de tamanho buffer_size
#             file_reading = True
#             while file_reading:
#                 received, address = sock.recvfrom(buffer_size)
#                 # Encerra a leitura dos dados do arquivo
#                 if received == FILE_FINISHED:
#                     file_reading = False
#                 # Adiciona o pacote recebido aos dados do arquivo, reconstruindo-o
#                 else:
#                     data += received

#             # Escreve os dados recebidos no arquivo (escreve data em received_file_path)
#             with open(file_path, "wb") as f:
#                 f.write(data)
#             print(f'- Client received file "{filename}" as a response\n')

if __name__ == "__main__":
    main()
