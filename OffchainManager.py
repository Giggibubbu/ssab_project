

class OffchainManager:

    __web3ManagementInstance = ''
    __web3ShardsInstances = ''

    def __init__(self, web3ManagementInstance, web3ShardsInstances):
        self.__web3ManagementInstance = web3ManagementInstance
        self.__web3ShardsInstances = web3ShardsInstances

        
    def isSCManagementDeployed(self):
        firstBlock = self.__web3ManagementInstance.eth.get_block(1, True)
        firstTransaction = firstBlock['transactions'][0]
        firstReceipt = self.__web3ManagementInstance.eth.get_transaction_receipt(firstTransaction['hash'])
        print(firstReceipt)
    
    #def deploy(privateKey):
        


        



