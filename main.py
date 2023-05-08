
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

# Lancia eccezioni, quindi inserirlo dentro al try. ## da gestire eccezioni nel caso non sia presente il conf.ini ##
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
    except Exception as e:
        print(e)
    
def formatList(listsContracts):
    contracts=[]
    for listc in listsContracts:
        for contract in listc:
            contracts.append(contract)
    return contracts







        




if __name__ == '__main__':
    
    
    try:
        addresses = readBchSettingsFromFile()
        web3BchManagement = Web3(Web3.HTTPProvider(addresses['managementAddress']))
        web3InstanceList = []
        for address in addresses['shardAddresses']:
            web3InstanceList.append(Web3(Web3.HTTPProvider(address)))

        offChainManager = OffchainManager(web3BchManagement, web3InstanceList)
    except Exception as e:
        print(e)


    loggedUser = User('')
    x = True
    while True and x:

        print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il login\n2. Effettua la registrazione\n3. Termina l'esecuzione.")
        choiche = input(">>> ")   



        match choiche:
            case '1':
                print("Inserisci la tua chiave privata")
                privateKey = input(">>> ")
                loggedUser.setPrivateKey(privateKey)
                loginResult = loggedUser.verifyPrivateKey()
                while(loginResult):
                    offChainManager.isSCManagementDeployed(privateKey, addresses['shardAddresses'])
                    print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il deploy\n2. Effettua una transazione\n3. Effettua il logout\n")
                    


                    loggedChoiche = input('>>> ')
                    match loggedChoiche:
                        case '1':
                            print("Inserisci il contratto nella cartella user_sc_to_deploy del programma e fornisci il nome del file contenente lo smart contract da deployare.")
                            contractFileName = input(">>> ")
                            offChainManager.deploy(privateKey, contractFileName)
                            print("Deploy effettuato")
                            
                        case '2':
                            print("Seleziona il contratto, scegliendo fra i seguenti")
                            contractsList = formatList(offChainManager.retrieveContracts())
                            ##print contracts
                            print(contractsList)
                            chosenContractAddress=input(">>> ") #tryexcept
                            isNumber = re.match("^[0-9][0-9]*$", chosenContractAddress)
                            if  isNumber and int(chosenContractAddress)<len(contractsList):
                                shardNumber, userChosenContract = offChainManager.retrieveContract(contractsList[int(chosenContractAddress)])
                                print("seleziona ua funzione relativa al contratto selezionato, scegliendo fra le seguenti:")
                                contractFunctions=offChainManager.retrieveFunctions(shardNumber, userChosenContract, contractsList[int(chosenContractAddress)])
                                print(contractFunctions)
                                chosenFunction = input(">>> ")

                                print(contractFunctions)
                                print("Transazione effettuata")
                            else:
                                print("Inserisci un numero tra quelli elencati!")
                            
                        case '3':
                            # dimentica l'utente
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

            


                