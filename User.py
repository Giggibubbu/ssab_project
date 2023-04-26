from web3 import Web3
from eth_account import Account
ganache_url= "http://127.0.0.1:7545"
web3=Web3(Web3.HTTPProvider(ganache_url))
class User:
    _privateKey =""
    #gestire le eccezioni sulla lunghezza, sintassi della chiave privata
    def setPrivateKey (privateKey):
        isprivatekeyvalid=False
        _privatekey=privatekey    
        return isprivatekeyvalid

    def getPrivateKey():
        return _privateKey

    def register(self):
     acc = web3.eth.account.create(); 
     return(f'private key={web3.to_hex(acc._private_key)}, account={acc.address}')