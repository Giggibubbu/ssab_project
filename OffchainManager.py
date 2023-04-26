from web3 import Web3
from eth_account import Account
ganache_url= "http://127.0.0.1:7545"       #presodalfilediconfig
web3=Web3(Web3.HTTPProvider(ganache_url))

class OffchainManager:
    #costruttore con inizializzazione su blockchain di management
    def isSCManagementDeployed():
        #test delle transazione
