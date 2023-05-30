from web3 import exceptions
import solcx
from web3 import Account
import jsonpickle
import importlib
import re
class OffchainManager:

    __web3ManagementInstance = None
    __web3ShardsInstances = None


    __contractManagementAddress = None
    __contractManagementAbi = None
    '''
       Il costruttore assegna i parametri in ingresso alla veriabili della classe corrente per la gestione delle istanze di web3.
       Succcessivamente installa il compilatore di solidity ed imposta la sua versione
    '''
    def __init__(self, web3ManagementInstance, web3ShardsInstances):
        self.__web3ManagementInstance = web3ManagementInstance
        self.__web3ShardsInstances = web3ShardsInstances
        solcx.install_solc(version='0.8.9')
        solcx.set_solc_version('0.8.9')

    '''la funzione verifica se lo smart contract di management è stato deployato sulla blockchain di management,
       prende come argomenti la chiave privata dell'utente e l'indirizzo della shard come argomento.
       Se sì, la funzione provvede al recupero dell'indirizzo dello smart contract di management dalla prima transazione su
       l primo blocco e ricompila lo smart contract di management dalla cartella sc_mngmt. Successivamente,
       assegna l'indirizzo del contratto e l'abi a due variabili private; 
       altrimenti viene chiamata la funzione deployScManagement'''

    def isSCManagementDeployed(self, userPrivateKey, addresses):
        try:
            firstBlock = self.__web3ManagementInstance.eth.get_block(1)
            firstTransaction = firstBlock['transactions'][0]
            firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction)
            self.__contractManagementAddress = firstReceipt['contractAddress']
            self.__contractManagementAbi, bytecode = self.__compileScManagement("sc_mngmt/management.sol")
        except (exceptions.BlockNotFound) as e:
            self.__deployScManagement(userPrivateKey, addresses)
    
    '''la funzione effettua la compilazione dello sc in oggetto e ritorna abi e bytecode'''
    def __compileScManagement(self, contractDirAndName):
        try:
            with open(contractDirAndName, 'r') as f:
                source = f.read()
            compiled_sol=solcx.compile_source(source)
            contract_id, contract_interface=compiled_sol.popitem()
            abi = contract_interface['abi']
            bytecode = contract_interface['bin']
            return abi, bytecode
        except IOError as e:
            print("errore nella lettura del file che contiene lo smart contract di management")

    
    '''la funzione effettua il deploy dello sc di management con la chiave privata fornita come argomento,
    assegna l'abi e l'indirizzo dello smart contract di management a due variabili private'''
    def __deployScManagement(self, userPrivateKey, addresses):
        try:
            abi, bytecode = self.__compileScManagement("sc_mngmt/management.sol")
            userAccount=Account.from_key(userPrivateKey)
            self.__web3ManagementInstance.eth.default_account=userAccount.address
            contract = self.__web3ManagementInstance.eth.contract(abi=abi, bytecode=bytecode)
            txHash = contract.constructor(len(self.__web3ShardsInstances), addresses).transact()
            txReceipt = self.__web3ManagementInstance.eth.wait_for_transaction_receipt(txHash)
            self.__contractManagementAbi = abi
            self.__contractManagementAddress = txReceipt['contractAddress']
        except (exceptions.TransactionNotFound) as e:
            print(f"Transazione non trovata\n {e}")

    ''' le funzione richiama la funzione whereToDeploy dello sc di management che restituisce il numero della shard su cui effettuare il deploy
    dello smart contract indicato dall'utente. Viene effettuato il deploy sulla shard identificata. Viene confermato il deploy, memorizzando le relative informazioni 
    nello sc di management
    '''
    def deploy(self, privateKey, contractFileName):
        try:
            scManagement = self.__web3ManagementInstance.eth.contract(address=self.__contractManagementAddress, abi=self.__contractManagementAbi)
            userAccount = Account.from_key(privateKey)
            self.__web3ManagementInstance.eth.default_account=userAccount.address
            shardStateEvent = scManagement.events.ShardState()
            txHash = scManagement.functions.whereToDeploy().transact()
            txReceipt = self.__web3ManagementInstance.eth.wait_for_transaction_receipt(txHash)
            result = shardStateEvent.process_receipt(txReceipt)
            shardStateEventDict = result[0]['args']
            targetShard = shardStateEventDict['whereToDeploy']
            scAbiToDeploy, scBytecodeToDeploy = self.__compileScManagement("user_sc_to_deploy/"+contractFileName)
            userSC=self.__web3ShardsInstances[targetShard].eth.contract(abi=scAbiToDeploy, bytecode=scBytecodeToDeploy)
            self.__web3ShardsInstances[targetShard].eth.default_account = userAccount.address
            txUserSCHash = userSC.constructor().transact()
            txUserSCReceipt = self.__web3ShardsInstances[targetShard].eth.wait_for_transaction_receipt(txUserSCHash)
            txConfirmDeploy = scManagement.functions.confirmDeploy(contractAddress=txUserSCReceipt.contractAddress, contractName=contractFileName.split(".")[0], contractBinary=f"{scAbiToDeploy}").transact()
            txReceiptConfirmDeploy = self.__web3ManagementInstance.eth.wait_for_transaction_receipt(txConfirmDeploy)
        except (exceptions.TransactionNotFound) as e:
            print(f"Transazione non trovata\n {e}")


    '''la funzione, a partire dallo smart contract di management, utilizza le istanze delle 
    diverse shard per richiamare tutti i contratti e i relativi nomi'''
    def retrieveContracts(self):
        try:
            c=0
            j=0
            allContracts=[]
            allContractsName=[]
            scManagement = self.__web3ManagementInstance.eth.contract(address=self.__contractManagementAddress, abi=self.__contractManagementAbi)
            for shard in self.__web3ShardsInstances:
                allContracts.append(scManagement.functions.returnAllContracts(c).call())
                c=c+1
            for shard in self.__web3ShardsInstances:
                allContractsName.append(scManagement.functions.returnAllContractsName(j).call())
                j=j+1
            return allContracts, allContractsName
        except RuntimeError as e:
            print(f"Errore nel richiamo del metodo sullo smart contract\n{e}")

    '''la funzione, a partire dall'indirizzo dello smart contract fornito come argomento,
     restituisce il numero della shard su cui è stato fatto il deploy e l'abi del relativo contratto '''
    def retrieveContract(self, address):
        try:
            scManagement = self.__web3ManagementInstance.eth.contract(address=self.__contractManagementAddress, abi=self.__contractManagementAbi)
            shNumberAndContract = scManagement.functions.whereIsContractDeployed(address).call()
            return shNumberAndContract[0], shNumberAndContract[1]
        except RuntimeError as e:
            print(f"Errore nel richiamo del metodo sullo smart contract\n{e}")
            
    '''la funzione, a partire dal numero della shard, dall'abi (stringa json) e dall'indirizzo del contratto selezionato passati come argomenti,
    effetta la conversione dell'abi in un oggetto python che viene restituito insieme ad una liste contenente  tutte le funzioni del contratto scelto '''
    def retrieveFunctions(self, shardNumber, userChosenContract, chosenContractAddress):
        usc = userChosenContract[1].replace("\'", "\"")
        jp = jsonpickle.unpickler.decode(usc)
        chosenContract = self.__web3ShardsInstances[shardNumber].eth.contract(address=chosenContractAddress, abi=jp)
        contractFunctions = []
        argsFunction = []
        for function in chosenContract.all_functions():
            contractFunctions.append(function.fn_name)
        return contractFunctions, jp
    ''' la funzione prende come argomenti l'abi e il nome della funzione scelta dall'utente, provvede a restituire una lista
    dei tipi degli argomenti richiesti dalla funzione stessa'''
    def retrieveFunctionArgs(self, chosenContractAbi, chosenFunction):
        chosenFunctionArgs = []
        for dictionary in chosenContractAbi:
            if 'name' in dictionary and dictionary['name'] == chosenFunction:
                if len(dictionary['inputs']) != 0:
                   for args in dictionary['inputs']:
                       chosenFunctionArgs.append(args['type'])
        return chosenFunctionArgs   

    '''la funzione verifica che la funzione selezionata dall'utente modifichi o meno lo stato dello smart contract e, sulla base di ciò, esegue 
    rispettivamente una transact o una call '''

    def runChosenFunction(self, userPKey, shardNumber, chosenContractAddress, chosenContractAbi, chosenFunction, chosenFunctionArgs, chosenFunctionTypeArgs):
        try:
            c=0
            if len(chosenFunctionArgs) > 0:
                for argType in chosenFunctionTypeArgs:
                    chosenFunctionArgs[c] = self.convert(chosenFunctionArgs[c], argType)
                    c = c+1
            chosenContract = self.__web3ShardsInstances[shardNumber].eth.contract(address=chosenContractAddress, abi=chosenContractAbi)
            userAccount = Account.from_key(userPKey)
            self.__web3ShardsInstances[shardNumber].eth.default_account=userAccount.address
            for function in chosenContract.all_functions():
                if function.fn_name == chosenFunction:
                    for dictionary in chosenContractAbi:
                        if 'name' in dictionary and dictionary['name'] == chosenFunction:
                            if len(dictionary['inputs']) == 0:
                                if dictionary['stateMutability'] == 'view' or dictionary['stateMutability'] == 'pure':
                                    contract_func = chosenContract.functions[chosenFunction]
                                    return contract_func.__call__().call()
                                else:
                                    contract_func = chosenContract.functions[chosenFunction]
                                    txHash = contract_func.__call__().transact()
                                    txReceipt = self.__web3ShardsInstances[shardNumber].eth.wait_for_transaction_receipt(txHash)
                                    return ""
                            else:
                                if dictionary['stateMutability'] == 'view' or dictionary['stateMutability'] == 'pure':
                                    contract_func = chosenContract.functions[chosenFunction]
                                    return contract_func.__call__(*chosenFunctionArgs).call()
                                else:
                                    contract_func = chosenContract.functions[chosenFunction]
                                    txHash = contract_func.__call__(*chosenFunctionArgs).transact()
                                    txReceipt = self.__web3ShardsInstances[shardNumber].eth.wait_for_transaction_receipt(txHash)
                                    return ""
            print("Transazione effettuata")
        except ValueError as e:
            print(f"inserire argomenti del tipo richiesto\n{e}")
        except RuntimeError as e:
            print(f"Errore nel richiamo del metodo sullo smart contract")
        except (exceptions.TransactionNotFound) as e:
            print(f"Transazione non trovata\n {e}")

    ''' la funzione converte i nomi dei tipi in solidity nei rispettivi nomi di tipi in python, effettua la rispettiva conversione'''                       
    def convert(self, value, type_):
        try:
            if(type_== "string"):
                type_ = "str"
            elif(type_== "address"):
                type_ = "str"
            elif( re.search("^int[0-9]{1,3}$", type_)):
                type_ = "int"
            elif( re.search("^uint[0-9]{1,3}$", type_)):
                type_ = "int"

            module = importlib.import_module('builtins')
            cls = getattr(module, type_)
            return cls(value)
        except Exception as e:
            raise ValueError
       





        


