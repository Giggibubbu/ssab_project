from web3 import exceptions

class OffchainManager:

    __web3ManagementInstance = ''
    __web3ShardsInstances = ''

    def __init__(self, web3ManagementInstance, web3ShardsInstances):
        self.__web3ManagementInstance = web3ManagementInstance
        self.__web3ShardsInstances = web3ShardsInstances

        
    def isSCManagementDeployed(self):
        try:
            firstBlock = self.__web3ManagementInstance.eth.get_block(1)
            print(firstBlock)
            firstTransaction = firstBlock['transactions'][0]
            firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction)
            print("\n\n", firstReceipt['contractAddress'])

        except exceptions.TransactionNotFound as e:
            print("Nel primo blocco minato non è presen")
        except exceptions.BlockNotFound as e:
            print("Effettuare il deploy di uno smart contract sulla blockchain di management")


        
    
    #def deploy(privateKey):
        


        



