import socket
import os

# Envio dos arquivos pelo cliente
def send_files(files):

    # Configuração de servidor e buffer size (tamnho dos pacotes)
    host = "localhost"
    port = 8080
    buffer_size = 1024

    # Sinais de término de envio de arquivos (SEND_FINISHED) e de envio de um arquivo (FILE_FINISHED)
    SEND_FINISHED = b"<<sendFinished>>"
    FILE_FINISHED = b"<<fileFinished>>"

    # Loop que permite o envio de vários arquivos
    for filename in files:
        file_size = os.path.getsize(filename) # Obtém o tamanho do arquivo

        # Criação do socket -> de acordo com o UDP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        sock.sendto(filename.encode(), (host, port)) # Envia o nome do arquivo
        sock.sendto(str(file_size).encode(), (host, port)) # Envia o tamanho do arquivo

        # Abre o arquivo para carregar seus dados
        with open(filename, "rb") as f:
            data = f.read(buffer_size) # Lê os dados que vão compor o 1º pacote (buffer_size bytes)

            # Loop que permite o envio de vários pacotes, enquanto houver dados
            while data:
                sock.sendto(data, (host, port))
                data = f.read(buffer_size)
        
        sock.sendto(FILE_FINISHED, (host, port)) # Sinal de término de envio do arquivo

    print("Files sent!")
    sock.sendto(SEND_FINISHED, (host, port)) # Sinal de término de envio de todos os arquivos

def main():
    # Basta adicionar os arquivos a serem transferidos aqui, apenas lembre-se de que deve estar na mesma pasta do client.py
    files = ["file.txt", "image.jpg"]
    send_files(files)

if __name__ == "__main__":
    main()
