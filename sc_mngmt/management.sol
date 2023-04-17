// SPDX-License-Identifier: MIT
pragma solidity >0.7.17;

contract BlockchainLoadBalancing {

    enum CounterInternalStates {CounterChanged, CounterNotChanged}
    
    struct SmartContract
    {
        string contractName;
        string contractBinary;
        address owner;
    }
    
    struct Shard {
        string httpsAddress;
        uint256 bchNumber;
        address[] contractsArray;
        mapping(address => SmartContract) smartContracts;
    }


    Shard[] blockchain;

    uint256 internal numberOfShard;
    uint256 internal maxDeployedContracts;
    uint256 internal counter;
    CounterInternalStates internal counterState;
    uint256 internal targetShardForDeploy;
    mapping(address => uint256) contractToShard;


    // Initializes Shards and internal variables
    constructor(uint256 shardCount, string[] memory httpsAddress)
    {
        require(shardCount == httpsAddress.length, "shardCount must be the same length as httpsAddress array");
        
        numberOfShard = shardCount;
        counter = 0;
        counterState = CounterInternalStates.CounterNotChanged;

        for (uint256 i = 0; i<shardCount; i++)
        {
            blockchain.push();
            blockchain[i].httpsAddress = httpsAddress[i];
            blockchain[i].bchNumber = i;
        }
     
    }

    /*  Communicates to OffchainManager the index of the shard where the deploy has to be executed.
        
        Ex. If there are four shard, the first deploy will be executed on shard n. 0. Then, 1, 2, 3.
        When the counter is equal to four, it will be resetted to 0.

        If there's no confirmDeploy after the previous execution of whereToDeploy, reverts changes of the counter.*/
    function whereToDeploy() public returns (uint256)
    {
        revertCounterChanges();
        if(counter<numberOfShard)
        {
            targetShardForDeploy = counter;
            counter++;
        }
        else if(counter == numberOfShard)
        {
            counter = 0;
            targetShardForDeploy = counter;
            counter++;
        }
        counterState = CounterInternalStates.CounterChanged;
        return targetShardForDeploy;
    }

    /* Called after the successful deploy by the OffchainManager.
       Writes smart contract data inside the corresponding target shard struct of the OnChainManager. */
    function confirmDeploy(address contractAddress, string calldata contractName, string calldata contractBinary) public
    {

        blockchain[targetShardForDeploy].smartContracts[contractAddress].contractName = contractName;
        blockchain[targetShardForDeploy].smartContracts[contractAddress].contractBinary = contractBinary;
        blockchain[targetShardForDeploy].smartContracts[contractAddress].owner = msg.sender;
        blockchain[targetShardForDeploy].contractsArray.push(contractAddress);
        contractToShard[contractAddress] = targetShardForDeploy;
        counterState = CounterInternalStates.CounterNotChanged;  
    }

    /* Resets counter when whereToDeploy was called but no confirmDeploy were executed. */
    function revertCounterChanges() private 
    {
        if(counterState == CounterInternalStates.CounterChanged)
        {
            counter--;
        }
    }

    function whereIsContractDeployed(address contractAddress) public view returns (string memory, string memory, uint256)
    {
        SmartContract memory smartContract = blockchain[contractToShard[contractAddress]].smartContracts[contractAddress];
        return (smartContract.contractName, smartContract.contractBinary, contractToShard[contractAddress]);
    }

    function printContract(address contractName) public view
    {
        
    }




}