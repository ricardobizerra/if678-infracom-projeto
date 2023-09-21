from utils.ResponseTypes import ResponseTypes
class User:
    def __init__(self, user_name, user_adress) -> None:
        self.user_name = user_name
        self.user_adress = user_adress
        self.messageQueue = []
    
    # Retorna o nome do usuário
    def getUserName(self) -> str:
        return self.user_name
    
    # Retorna o endereço (ip, porta) do usuário
    def getUserAddress(self) -> str:
        return self.user_adress

    # Retorna um dicionário com o nome e endereço do usuário
    def getUserObject(self) -> dict:
        userObject =  {
            "name": self.user_name,
            "address": self.user_adress
        }
        return userObject

    # Retorna nova mensagem da fila de mensagens, caso não haja retorna um código de erro (enums do ResponseTypes.py)
    def getNewMessage(self):
        if len(self.messageQueue) > 0:
            newMessage = self.messageQueue[0]
            del self.messageQueue[0]
            return newMessage
        else:
            return str(ResponseTypes.NO_HAVE_MESSAGES.value)
    
    # Adiciona uma mensagem na fila de mensagens
    def addMessageToQueue(self, message):
        self.messageQueue.append(message)