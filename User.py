import re
class User:
    __privateKey = ""

    def __init__(self, privateKey):
        self.__privateKey = privateKey

    # gestire le eccezioni sulla lunghezza, sintassi della chiave privata
    def verifyPrivateKey(self):
        return re.search("\A([0]{1}[xX]{1})\w{64}", self.__privateKey)
    
    def getPrivateKey(self):
        return self.__privateKey
    def setPrivateKey(self, privateKey):
        self.__privateKey = privateKey