class User:
    __privateKey = ""

    def __init__(self, privateKey):
        self.__privateKey = privateKey

    # gestire le eccezioni sulla lunghezza, sintassi della chiave privata
    def verifyPrivateKey(self):
        isPrivateKeyValid=False 
        return isPrivateKeyValid
    
    def getPrivateKey(self):
        return self.__privateKey
    def setPrivateKey(self, privateKey):
        self.__privateKey = privateKey