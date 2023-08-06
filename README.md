Passo 1:
    Coloque os arquivos a serem enviados para o servidor dentro de 'client/sent';

Passo 2:
    Após isso, execute primeiro o código do servidor;

Passo 3:
    Quando o servidor printar "Server waiting files...", você executa o código do cliente em outra instância do terminal

- Após isso, o cliente enviará os arquivos para o servidor;

- O servidor amazenará na pasta 'server/received' com o nome do arquivo modificado e irá enviá-lo de volta para o cliente, que por sua vez armazenará na pasta 'client/received'

