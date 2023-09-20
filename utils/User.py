class User:
    def __init__(self, user_name, user_adress) -> None:
        self.user_name = user_name
        self.user_adress = user_adress
    
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
