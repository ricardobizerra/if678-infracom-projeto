from utils.ResponseTypes import ResponseTypes
class User:
    def __init__(self, user_name, user_adress) -> None:
        self.user_name = user_name
        self.user_adress = user_adress
        self.messageQueue = []
    
    def getUserName(self) -> str:
        return self.user_name
    
    def getUserAddress(self) -> str:
        return self.user_adress

    def getUserObject(self) -> dict:
        userObject =  {
            "name": self.user_name,
            "address": self.user_adress
        }
        return userObject

    def getNewMessage(self):
        if len(self.messageQueue) > 0:
            newMessage = self.messageQueue[0]
            del self.messageQueue[0]
            return newMessage
        else:
            return str(ResponseTypes.NO_HAVE_MESSAGES.value)
        
    def addMessageToQueue(self, message):
        self.messageQueue.append(message)