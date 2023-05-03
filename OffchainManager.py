from web3 import exceptions
import solcx
from web3 import Account

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
            print(firstBlock)
            firstTransaction = firstBlock['transactions'][0]
            firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction)
            self.__contractManagementAddress = firstReceipt['contractAddress']
            self.__contractManagementAbi, bytecode = self.__compileScManagement("management.sol")
        except (exceptions.BlockNotFound) as e:
            self.__deployScManagement(userPrivateKey, addresses)
    
    '''
       Function used for compiling smart contracts (including management smart contract) and returning its abi and
       bytecode.
    '''
    def __compileScManagement(self, contractFileName):
        with open("sc_mngmt/"+contractFileName, 'r') as f:
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
        abi, bytecode = self.__compileScManagement("management.sol")
        userAccount=Account.from_key(userPrivateKey)
        self.__web3ManagementInstance.eth.default_account=userAccount.address
        contract = self.__web3ManagementInstance.eth.contract(abi=abi, bytecode=bytecode)
        txHash = contract.constructor(len(self.__web3ShardsInstances), addresses).transact()
        txReceipt = self.__web3ManagementInstance.eth.wait_for_transaction_receipt(txHash)
        self.__contractManagementAbi = abi
        self.__contractManagementAddress = txReceipt['contractAddress']

    #def deploy(privateKey):
        


        



