import socket

# Recebimento dos arquivos pelo servidor
def receive_file_array():

    # Configuração de servidor e buffer size (tamnho dos pacotes)
    host = "localhost"
    port = 8080
    buffer_size = 1024

    # Sinais de término de envio de arquivos (SEND_FINISHED) e de envio de um arquivo (FILE_FINISHED)
    SEND_FINISHED = b"<<sendFinished>>"
    FILE_FINISHED = b"<<fileFinished>>"

    # Criação do socket e bind do servidor -> de acordo com o UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))

    # Recebimento dos arquivos
    files_being_received = True
    while files_being_received:
        file, address = sock.recvfrom(buffer_size)

        # Encerra o recebimento de arquivos
        if file == SEND_FINISHED:
            files_being_received = False
            print("All files received!")
        
        else:
            file = file.decode() # Decodifica o nome do arquivo
            filename = f"received_{file}" # Cria o nome do arquivo de recebimento
            print(file)

            file_size, address = sock.recvfrom(buffer_size)
            file_size = int(file_size.decode()) # Decodifica o tamanho do arquivo

            data = b"" # Início da leitura dos dados do arquivo

            # Loop que permite a leitura dos dados do arquivo, subdividindo-o em pacotes de tamanho buffer_size
            file_reading = True
            while file_reading:
                received, address = sock.recvfrom(buffer_size)

                # Encerra a leitura dos dados do arquivo
                if received == FILE_FINISHED:
                    file_reading = False
                
                # Adiciona o pacote recebido aos dados do arquivo, reconstruindo-o - lembre da observação 2 da especificação
                else:
                    data += received

            # Escreve os dados recebidos no arquivo (escreve data em received_filename)
            with open(filename, "wb") as f:
                f.write(data)

            print(f"File {filename} received!")

def main():
    receive_file_array()

if __name__ == "__main__":
    main()
