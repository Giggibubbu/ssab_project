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
       Constructor.
       It assigns the value passed to it to the class variables for managing web3 instances.
       Then install the solidity compiler and set its version.
    '''
    def __init__(self, web3ManagementInstance, web3ShardsInstances):
        self.__web3ManagementInstance = web3ManagementInstance
        self.__web3ShardsInstances = web3ShardsInstances
        solcx.install_solc(version='0.8.9')
        solcx.set_solc_version('0.8.9')

    '''Function used for checking if a management sc is ever deployed to the management blockchain instance.
       It takes the user private key and http addresses of shards as arguments.
       If yes, the function recovers sc management address from the first transaction in the first block of the
       management bch instance and re-compiles the sc from sc_mngmt folder.
       Then, it assigns the contract address and abi to private class variable (__contractManagementAddress
       and __contractManagementAbi).
       If not, the function calls the private deployScManagement function (passing its argument).
    '''
    def isSCManagementDeployed(self, userPrivateKey, addresses):
        try:
            firstBlock = self.__web3ManagementInstance.eth.get_block(1)
            firstTransaction = firstBlock['transactions'][0]
            firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction)
            self.__contractManagementAddress = firstReceipt['contractAddress']
            self.__contractManagementAbi, bytecode = self.__compileScManagement("sc_mngmt/management.sol")
        except (exceptions.BlockNotFound) as e:
            self.__deployScManagement(userPrivateKey, addresses)
    
    '''
       Function used for compiling smart contracts (including management smart contract) and returning its abi and
       bytecode.
    '''
    def __compileScManagement(self, contractDirAndName):
        with open(contractDirAndName, 'r') as f:
            source = f.read()
        compiled_sol=solcx.compile_source(source)
        contract_id, contract_interface=compiled_sol.popitem()
        abi = contract_interface['abi']
        bytecode = contract_interface['bin']
        return abi, bytecode

    '''
       Deploys the sc management with the provided private key (first argument).
       Then, it assigns abi and sc management contract address to class private variables.
       (__contractManagementAbi and __contractManagementAddress)
    '''    
    def __deployScManagement(self, userPrivateKey, addresses):
        abi, bytecode = self.__compileScManagement("sc_mngmt/management.sol")
        userAccount=Account.from_key(userPrivateKey)
        self.__web3ManagementInstance.eth.default_account=userAccount.address
        contract = self.__web3ManagementInstance.eth.contract(abi=abi, bytecode=bytecode)
        txHash = contract.constructor(len(self.__web3ShardsInstances), addresses).transact()
        txReceipt = self.__web3ManagementInstance.eth.wait_for_transaction_receipt(txHash)
        self.__contractManagementAbi = abi
        self.__contractManagementAddress = txReceipt['contractAddress']

    def deploy(self, privateKey, contractFileName):
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

    
    def retrieveContracts(self):
        c=0
        allContracts=[]
        scManagement = self.__web3ManagementInstance.eth.contract(address=self.__contractManagementAddress, abi=self.__contractManagementAbi)
        for shard in self.__web3ShardsInstances:
            allContracts.append(scManagement.functions.returnAllContracts(c).call())
            c=c+1
        return allContracts

    def retrieveContract(self, address):
        scManagement = self.__web3ManagementInstance.eth.contract(address=self.__contractManagementAddress, abi=self.__contractManagementAbi)
        shNumberAndContract = scManagement.functions.whereIsContractDeployed(address).call()
        return shNumberAndContract[0], shNumberAndContract[1]

    def retrieveFunctions(self, shardNumber, userChosenContract, chosenContractAddress):
        usc = userChosenContract[1].replace("\'", "\"")
        jp = jsonpickle.unpickler.decode(usc)
        print(jp)
        chosenContract = self.__web3ShardsInstances[shardNumber].eth.contract(address=chosenContractAddress, abi=jp)
        contractFunctions = []
        argsFunction = []
        for function in chosenContract.all_functions():
            contractFunctions.append(function.fn_name)
        return contractFunctions, jp
    
    def retrieveFunctionArgs(self, chosenContractAbi, chosenFunction):
        chosenFunctionArgs = []
        for dictionary in chosenContractAbi:
            if 'name' in dictionary and dictionary['name'] == chosenFunction:
                if len(dictionary['inputs']) != 0:
                   for args in dictionary['inputs']:
                       chosenFunctionArgs.append(args['type'])
        return chosenFunctionArgs   



    def runChosenFunction(self, userPKey, shardNumber, chosenContractAddress, chosenContractAbi, chosenFunction, chosenFunctionArgs, chosenFunctionTypeArgs):
        # controllo tipi e argomenti inseriti dall'utente
        c=0
        if len(chosenFunctionArgs) > 0:
            for argType in chosenFunctionTypeArgs:
                chosenFunctionArgs[c] = self.convert(chosenFunctionArgs[c], argType)
                c = c+1

                

        
        chosenContract = self.__web3ShardsInstances[shardNumber].eth.contract(address=chosenContractAddress, abi=chosenContractAbi)
        userAccount = Account.from_key(userPKey)
        self.__web3ShardsInstances[shardNumber].eth.default_account=userAccount.address
        # questo for è inutile
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
                                return txHash
                        else:
                            if dictionary['stateMutability'] == 'view' or dictionary['stateMutability'] == 'pure':
                                contract_func = chosenContract.functions[chosenFunction]
                                return contract_func.__call__().call(*chosenFunctionArgs)
                            else:
                                contract_func = chosenContract.functions[chosenFunction]
                                txHash = contract_func.__call__().transact(*chosenFunctionArgs)
                                txReceipt = self.__web3ShardsInstances[shardNumber].eth.wait_for_transaction_receipt(txHash)
                                return txHash
                            
    def convert(self, value, type_):
        # Check if it's a builtin type
        
        match type_:
            case "string":
                type_ = "str"
            case "address":
                type_ = "str"
            case re.search("^int[0-9]{1,3}$", type_):
                type_ = "int"
            case re.search("^uint[0-9]{1,3}$", type_):
                type_ = "int"

        module = importlib.import_module('builtins')
        if not re.search("\[\]$", type_):
            cls = getattr(module, type_)
            return cls(value)
        else:
            array = []
            match type_:
                case re.search("^string\[\]$"):
                    for element in value:
                        array.append(str(element))
                case re.search("^address\[\]$"):
                    for element in value:
                        array.append(str(element))
                case re.search("^uint[0-9]{1,3}\[\]$"):
                    for element in value:
                        array.append(int(element))
                case re.search("^int[0-9]{1,3}\[\]$"):
                    for element in value:
                        array.append(int(element))
                case re.search("^bool\[\]$"):
                    for element in value:
                        array.append(bool(element))
            return array





        


