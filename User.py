import re
class User:
    __privateKey = ""

    def __init__(self, privateKey):
        self.__privateKey = privateKey

    def verifyPrivateKey(self):
        try:
            return re.search("\A([0]{1}[xX]{1})\w{64}", self.__privateKey)
        except Exception as e:
            print(f"errore nella sintassi della chiave privata inserita \n{e}")
    
    def getPrivateKey(self):
        return self.__privateKey

    def setPrivateKey(self, privateKey):
        self.__privateKey = privateKey