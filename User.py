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
from web3 import Web3
from eth_account import Account
ganache_url= "http://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
class User:

    # metodo login(chiave_pubblica, chiave_privata)
    def login (self, public_key, private_key):                                      #eccezioni da gestire sulle lunghezze delle chaivi
     PA=web3.eth.account.from_key(private_key)
     Public_Address=PA.address
     if(Public_Address==public_key):
        return True
     else: 
         return False                                                                     

 

    def register(self):
     acc = web3.eth.account.create(); 
     return(f'private key={web3.to_hex(acc._private_key)}, account={acc.address}')