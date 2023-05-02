from web3 import exceptions

class OffchainManager:

    __web3ManagementInstance = ''
    __web3ShardsInstances = ''


    __contractManagementAddress = ''

    def __init__(self, web3ManagementInstance, web3ShardsInstances):
        self.__web3ManagementInstance = web3ManagementInstance
        self.__web3ShardsInstances = web3ShardsInstances

    #verifica se sc di management è stato deployato. se si, si riprende l'address
    def __isSCManagementDeployed(self):
        try:
            firstBlock = self.__web3ManagementInstance.eth.get_block(1)
            print(firstBlock)
            firstTransaction = firstBlock['transactions'][0]
            firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction)
            self.__contractManagementAddress = firstReceipt['contractAddress']

        except (exceptions.BlockNotFound) as e:
            print(e)


        
    
    #def deploy(privateKey):
        


        



