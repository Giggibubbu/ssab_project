
# Punto di partenza del programma
from web3 import Web3
from User import User
from OffchainManager import OffchainManager
import re

def verifyAddress(address):
   result = re.search("^http://127[.]0[.]0[.]1:[0-9]{1,5}$", address)
   if result:
    number = address.split(":")
    try:
        if 0 <= int(number[2]) <= 65535:
            return True
        else:
            return False
    except Exception:
        return False
   else:
       return False

''' La funzione seguente viene richiamata per la lettura del file di configurazione che contiene gli indirizzi delle blockchain utilizzate, 
nel caso in cui il file non sia presente viene generata '''
def readBchSettingsFromFile():
    try:
        confFile = open("conf.ini", "r")
        confData = {}
        lineList = confFile.readlines()
        for line in lineList:
            if line[0] != '#' and line[0] != '[' and line[0]!='\n':
                line = line.replace('\n', '')
                splittedLine = line.split('=')
                confData[splittedLine[0]] = splittedLine[1]
        confData['shardAddresses'] = confData['shardAddresses'].split(';')
        if not verifyAddress(confData['managementAddress']):
            raise Exception("Management address not valid.")
        if len(confData['shardAddresses']) <2:
            raise Exception("You have to set up at least two shards")
        for ad in confData['shardAddresses']:
            if not verifyAddress(ad):
                raise Exception("Shard address not valid.")
        confFile.close()
        return confData
    except IOError as e:
        print("Errore nella lettura del file conf.ini")
    except Exception as e:
        print("Errore nella lettura del file con.ini")

'''la funzione prende in ingresso listsContracts, che a sua volta contiene altre due liste, crea due liste: 
una contente gli indirizzi e una i nomi delle funzioni'''
def formatList(listsContracts):
    contracts=[]
    contractsName=[]
    for listc in listsContracts[0]:
        for contract in listc:
            contracts.append(contract)
    for listc in listsContracts[1]:
        for contract in listc:
            contractsName.append(contract)
    return contracts, contractsName

#
if __name__ == '__main__':
    try:
    
        try:
            addresses = readBchSettingsFromFile()
            #creazione dell'istanza web3, connessione alla blockchain di management
            web3BchManagement = Web3(Web3.HTTPProvider(addresses['managementAddress']))
            web3InstanceList = []
            #creazione delle istanze web3, connessione alle blockchain su cui fare deploy
            for address in addresses['shardAddresses']:
                web3InstanceList.append(Web3(Web3.HTTPProvider(address)))
            #creazione dell'istanza dell'Offchain Mananger 
            offChainManager = OffchainManager(web3BchManagement, web3InstanceList)
        except Exception as e:
            print(e)

        #creazione dell'istanza dell'utente
        loggedUser = User('')
        x = True
        while True and x:

            print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il login\n2. Effettua la registrazione\n3. Termina l'esecuzione.")
            choiche = input(">>> ")   



            match choiche:
                #login
                case '1':
                    print("Inserisci la tua chiave privata")
                    privateKey = input(">>> ")
                    loggedUser.setPrivateKey(privateKey)
                    loginResult = loggedUser.verifyPrivateKey()
                    while(loginResult):
                        offChainManager.isSCManagementDeployed(privateKey, addresses['shardAddresses'])
                        print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il deploy\n2. Effettua una transazione\n3. Elimina smart contract\n4. Effettua il logout")
                        loggedChoiche = input('>>> ')
                        match loggedChoiche:
                            case '1':
                                print("Inserisci il contratto nella cartella user_sc_to_deploy del programma e fornisci il nome del file contenente lo smart contract da deployare.")
                                contractFileName = input(">>> ")
                                offChainManager.deploy(privateKey, contractFileName)
                                print("Deploy effettuato")
                                
                            case '2':
                                print("Seleziona il contratto al quale sei interessato, scegliendo fra i seguenti")
                                contractsList = formatList(offChainManager.retrieveContracts())
                                j=0
                                for c in contractsList[1]:
                                    print(f"{j}: {c}")
                                    j=j+1
                                chosenContractAddress=input(">>> ") 
                                isNumber = re.match("^[0-9][0-9]*$", chosenContractAddress)
                                
                                if  isNumber and int(chosenContractAddress)<len(contractsList[0]):
                                    shardNumber, userChosenContract = offChainManager.retrieveContract(contractsList[0][int(chosenContractAddress)])
                                    print("Seleziona una funzione relativa al contratto selezionato, scegliendo fra le seguenti:")
                                    contractFunctions, contractAbi=offChainManager.retrieveFunctions(shardNumber, userChosenContract, contractsList[0][int(chosenContractAddress)])
                                    y=0
                                    for c in contractFunctions:
                                        print(f"{y}: {c}")
                                        y=y+1

                                    chosenFunction = input(">>> ")
                                    intChosenFunction = re.match("^[0-9][0-9]*$", chosenFunction)
                                    if intChosenFunction and int(chosenFunction)<len(contractFunctions):
        
                                        chosenFunctionTypeArgs = offChainManager.retrieveFunctionArgs(contractAbi, contractFunctions[int(chosenFunction)])
                                        if (len(chosenFunctionTypeArgs)!=0):
                                            print(f"La funzione scelta prende n.{len(chosenFunctionTypeArgs)} argomenti dei seguenti tipi: {chosenFunctionTypeArgs}\nInserisci il loro valore separato da ; (es. arg1;arg2;...)")
                                            chosenFunctionArgs = input(">>> ")
                                            chosenFunctionArgs = chosenFunctionArgs.split(";")
                                        else:
                                            chosenFunctionArgs=[]
                                        
                                        print(offChainManager.runChosenFunction(privateKey, shardNumber, contractsList[0][int(chosenContractAddress)], contractAbi, contractFunctions[int(chosenFunction)], chosenFunctionArgs, chosenFunctionTypeArgs))
                                     
                                    else:
                                        print("inserisci un numero fra quelli indicati")
                                else:
                                    print("Inserisci un numero tra quelli elencati!")
                            case '3':
                                print("Seleziona il contratto che vuoi eliminare, scegliendo fra i seguenti")
                                contractsList = formatList(offChainManager.retrieveContracts())
                                print(contractsList)
                                j=0
                                for c in contractsList[1]:
                                    print(f"{j}: {c}")
                                    j=j+1
                                chosenContractAddress=input(">>> ") 
                                isNumber = re.match("^[0-9][0-9]*$", chosenContractAddress)
                                if  isNumber and int(chosenContractAddress)<len(contractsList[0]):
                                    shardNumber, userChosenContract = offChainManager.retrieveContract(contractsList[0][int(chosenContractAddress)])
                                    offChainManager.deleteContract(shardNumber, contractsList[0][int(chosenContractAddress)])
                                
                                else:
                                    print("Inserisci un numero tra quelli elencati!")


                            case '4':
                                loggedUser.setPrivateKey(None)
                                print("Logout effettuato")
                                loginResult = False
                            case default:
                                print("Carattere errato")  



                    choiche = '1'

                case '2':
                    print("Generazione della chiave privata...\n...")
                    print("\nUtente registrato!")
                case '3':
                    x = False
                case default:
                    print("Il carattere digitato non corrisponde ad alcuna funzionalità")
    except Exception as e:
        print(f"Errore nel programma principale\n{e}")
    

                


                    