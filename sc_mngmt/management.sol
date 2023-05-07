// SPDX-License-Identifier: MIT
pragma solidity >0.7.17;

contract BlockchainLoadBalancing {

    uint256 internal numberOfShard;
    uint256 internal maxDeployedContracts;
    uint256 internal counter;
    uint256 internal targetShardForDeploy;
    mapping(address => uint256) contractToShard;

    Shard[] blockchain;
    enum CounterInternalStates {CounterChanged, CounterNotChanged}
    CounterInternalStates internal counterState;
    
    struct SmartContract
    {
        string contractBinary;
        address owner;
    }
    
    struct Shard {
        string httpAddress;
        uint256 bchNumber;
        address[] contractsArray;
        mapping(address => SmartContract) smartContracts;
    }

    event Deploy(
        address contractAddress,
        string message,
        uint256 deployedToShard
    );

    event ShardState(
        address sender,
        uint256 whereToDeploy
    );

    // Initializes Shards and internal variables
    constructor(uint256 shardCount, string[] memory httpAddress)
    {
        require(shardCount == httpAddress.length,
        "shardCount must be the same length as httpsAddress array");
        
        numberOfShard = shardCount;
        counter = 0;
        counterState = CounterInternalStates.CounterNotChanged;

        for (uint256 i = 0; i<shardCount; i++)
        {
            blockchain.push();
            blockchain[i].httpAddress = httpAddress[i];
            blockchain[i].bchNumber = i;
        }
    }

    /*  Communicates to OffchainManager the index of the shard where
        the deploy has to be executed.
        
        Ex. If there are four shard, the first deploy will be executed on shard n. 0.
        Then, 1, 2, 3. When the counter is equal to four, it will be resetted to 0.

        If there's no confirmDeploy after the previous execution of whereToDeploy,
        reverts changes of the counter.
    */
    function whereToDeploy() public
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
        emit ShardState(msg.sender, targetShardForDeploy);
    }

    /* Called after the successful deploy by the OffchainManager.
       Writes smart contract data inside the corresponding target shard struct of
       the OnChainManager.
    */
    function confirmDeploy(address contractAddress, string calldata contractBinary) public
    {

        blockchain[targetShardForDeploy].smartContracts[contractAddress].contractBinary = contractBinary;
        blockchain[targetShardForDeploy].smartContracts[contractAddress].owner = msg.sender;
        blockchain[targetShardForDeploy].contractsArray.push(contractAddress);
        contractToShard[contractAddress] = targetShardForDeploy;
        counterState = CounterInternalStates.CounterNotChanged;
        emit Deploy(contractAddress, "deploy confirmed to shard n. ", targetShardForDeploy);  
    }

    /* Resets counter when whereToDeploy was called but no confirmDeploy were executed. */
    function revertCounterChanges() private 
    {
        if(counterState != CounterInternalStates.CounterNotChanged)
        {
            counter--;
        }
    }

    // Returns  the shard where the contract with address contractAddress is deployed
    function whereIsContractDeployed(address contractAddress) public view returns (uint256)
    {
        return (contractToShard[contractAddress]);
    }

    function returnAllContracts(uint256 s) public view returns (address[] memory)
    {
        return blockchain[s].contractsArray;
    }




}