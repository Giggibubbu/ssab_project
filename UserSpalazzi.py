#User Blockchain Spalazzi 

from web3 import Web3 
from eth_account import Account

#connessione alla rete su Ganache 

w3= Web3(Web3.HTTPProvider('http://localhost:8545'))

#metodo di selezione tra uno dei 10 account su ganache, utilizzo un metodo di Web3
def sceltaAccount():
    account= w3.eth.accounts    
    #seleziono l'account tramite l'indice, perchè il metodo ritorna una lista 
    print ("Scegliere un account")
    for i, account in enumerate(account):
    print(f'{i}. {account}')
    indice_selezionato= int(input('Inserire il numero dell''account da selezionare'))
    account_selezionato= account[indice_selezionato]
    return print ('l account selezionato è : ', account_selezionato)

#Definisco dei metodi base per l'account 

def balance():
    saldo=w3.eth.get_balance(account_selezionato)
    return print(saldo)

def lastBlock():
    return print (w3.eth.get_block_numeber())

def informationBlock():
    numeroBlocco=input (' inserire il numero del blocco richiesto')
    return print (w3.eth.get_block(numeroBlocco))