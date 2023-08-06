import socket
import os

# Configuração de servidor e buffer size (tamnho dos pacotes)
host = "localhost"
port = 8080

# Criação do socket e bind do servidor -> de acordo com o UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Adiciona a opção SO_REUSEADDR
sock.bind((host, port))

# Recebimento dos arquivos pelo servidor
def receive_file_array():
    buffer_size = 1024

    # Sinais de término de envio de arquivos (SEND_FINISHED) e de envio de um arquivo (FILE_FINISHED)
    SEND_FINISHED = b"<<sendFinished>>"
    FILE_FINISHED = b"<<fileFinished>>"

 
    # Recebimento dos arquivos
    files_being_received = True
    print('Server waiting files...\n')
    while files_being_received:
        file, address = sock.recvfrom(buffer_size)

        # Encerra o recebimento de arquivos
        if file == SEND_FINISHED:
            files_being_received = False
            print("All files received!")
        else:
            file = file.decode()  # Decodifica o nome do arquivo
            file_path = f"server/received/received_{file}"  # Cria o nome do arquivo de recebimento
            filename = file
            file_size, address = sock.recvfrom(buffer_size)
            file_size = int(file_size.decode())  # Decodifica o tamanho do arquivo

            data = b""  # Início da leitura dos dados do arquivo

            # Loop que permite a leitura dos dados do arquivo, subdividindo-o em pacotes de tamanho buffer_size
            file_reading = True
            while file_reading:
                received, address = sock.recvfrom(buffer_size)
                # Encerra a leitura dos dados do arquivo
                if received == FILE_FINISHED:
                    file_reading = False
                # Adiciona o pacote recebido aos dados do arquivo, reconstruindo-o
                else:
                    data += received
            # Escreve os dados recebidos no arquivo (escreve data em received_file_path)
            with open(file_path, "wb") as f:
                f.write(data)

            print(f"- File {filename} received from {address}!")

            # Chama a função para enviar o arquivo de resposta para o cliente
            sent_file_to_client(f'server/received/received_{filename}', address)


def sent_file_to_client(file_path, client_address):
    buffer_size = 1024
    file_name = file_path.split('/')[-1]
    print(f"- Sending file {file_name} to client {client_address}\n")

    FILE_FINISHED = b"<<fileFinished>>"

    # Obtém o tamanho do arquivo
    file_size = os.path.getsize(file_path)

    # Envia o nome do arquivo
    sock.sendto(file_name.encode(), client_address)
    # Envia o tamanho do arquivo
    sock.sendto(str(file_size).encode(), client_address)

    # Abre o arquivo para carregar seus dados
    with open(file_path, "rb") as f:
        data = f.read(buffer_size)  # Lê os dados que vão compor o 1º pacote (buffer_size bytes)
        # Loop que permite o envio de vários pacotes, enquanto houver dados
        while data:
            sock.sendto(data, client_address)
            data = f.read(buffer_size)
    # Sinal de término de envio do arquivo
    sock.sendto(FILE_FINISHED, client_address)

def main():
    os.makedirs('server/received')
    receive_file_array()

if __name__ == "__main__":
    main()
