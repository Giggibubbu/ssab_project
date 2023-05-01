class User:
    _privateKey =""

    def __init__(self, privateKey):
        self._privateKey = privateKey

    #gestire le eccezioni sulla lunghezza, sintassi della chiave privata
    def _setPrivateKey(self, privateKey):
        isPrivateKeyValid=False
        _privateKey=privateKey    
        return isPrivateKeyValid