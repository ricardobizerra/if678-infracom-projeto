from utils.User import User

class UserList:
    def __init__(self) -> None:
        self.list = {}

    # Converte o endereço do cliente para string
    def clientAddressToString(self, client_address) -> str:
        strClientAddress = str(client_address[0]) + '/' + str(client_address[1])
        return strClientAddress

    # Verifica se o usuário já está registrado
    def userIdIsRegistered(self, address) -> bool:
        address = self.clientAddressToString(address)
        if address in self.list:
            return True
        return False

    # Adiciona um usuário na lista de usuários
    def addUser(self, user: User) -> bool:
        user_address = self.clientAddressToString(user.getUserAddress())
        if not self.userIdIsRegistered(user_address):
            self.list[user_address] = user
            return True
        return False     

    # Remove um usuário da lista de usuários
    def removeUser(self, address) -> bool:
        if self.userIdIsRegistered(address):
            address = self.clientAddressToString(address)
            del self.list[address]
            return True
        return False
    
    # Retorna um possível usuário da lista de usuários que possua o endereço pesquisado
    def getUserByAddress(self, address):
        if self.userIdIsRegistered(address):
            address = self.clientAddressToString(address)
            return self.list[address]
        return None
    
    # Retorna a lista de usuários
    def getList(self):
        return self.list