from utils.User import User

class UserList:
    def __init__(self) -> None:
        self.list = {}

    def clientAddressToString(self, client_address) -> str:
        strClientAddress = str(client_address[0]) + '/' + str(client_address[1])
        return strClientAddress

    def userIdIsRegistered(self, address) -> bool:
        address = self.clientAddressToString(address)
        if address in self.list:
            return True
        return False

    def addUser(self, user: User) -> bool:
        user_address = self.clientAddressToString(user.getUserAddress())
        if not self.userIdIsRegistered(user_address):
            self.list[user_address] = user
            return True
        return False     

    def removeUser(self, address) -> bool:
        address = self.clientAddressToString(address)
        if self.userIdIsRegistered(address):
            del self.list[address]
            return True
        return False
    
    def getUserByAddress(self, address):
        if self.userIdIsRegistered(address):
            address = self.clientAddressToString(address)
            return self.list[address]
        return None
    
    def getList(self):
        return self.list