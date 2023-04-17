from eth_account import Account
class User:
    #chiavepubblica
    publicAddress = ''
    #chiaveprivata
    _privateKey = ''

    web3Instance = ''

    isPrivateKeyValid = False

    def __init__(self, privateKey):
        self.login(privateKey)
        ##bilancio wallet


    
    # metodo login
    def login(privateKey):
        assert privateKey is not None, "Devi inserire una chiave privata valida."
        assert privateKey.startswith("0x"), "Le chiavi private devono cominciare con il prefisso esadecimale 0x"
        isPrivateKeyValid = True
        _privateKey = privateKey


    
    #metodo register
