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
        string contractName;
        string contractBinary;
        address owner;
    }
    
    struct Shard {
        string httpAddress;
        uint256 bchNumber;
        address[] contractsArray;
        string[] contractsArrayName;
        mapping(address => SmartContract) smartContracts;
    }

    event Deploy(
        address contractAddress,
        uint256 deployedToShard
    );

    event ShardState(
        address sender,
        uint256 whereToDeploy
    );

    // Inizializza la struttura rappresentante le Shards e le variabili interne dello smart contract
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

    /*  
        Comunica all'OffchainManager l'indice della shard sulla quale deve essere eseguito il deploy.

        Es. Se ci sono quattro shard, il primo deploy verrà eseguito sulla shard n.0.
        Successivamente, 1, 2 e 3. Quando il counter è uguale a 4, sarà resettato a 0.

        Se non c'è conferma di avvenuto deploy dopo la precedente esecuzione di whereToDeploy,
        riporta il counter allo stato precedente.

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

    /* 
       Scrive i dati dello smart contract all'interno della struttura della shard su cui era previsto
       che il deploy dovesse avvenire, in seguito alla conferma di operazione avvenuta con
       successo da parte dell'OffchainManager. 
    */
    function confirmDeploy(address contractAddress, string calldata contractName, string calldata contractBinary) public
    {
        blockchain[targetShardForDeploy].smartContracts[contractAddress].contractName = contractName;
        blockchain[targetShardForDeploy].smartContracts[contractAddress].contractBinary = contractBinary;
        blockchain[targetShardForDeploy].smartContracts[contractAddress].owner = msg.sender;
        blockchain[targetShardForDeploy].contractsArray.push(contractAddress);
        blockchain[targetShardForDeploy].contractsArrayName.push(contractName);
        contractToShard[contractAddress] = targetShardForDeploy;
        counterState = CounterInternalStates.CounterNotChanged;
        emit Deploy(contractAddress, targetShardForDeploy);  
    }

    /* Se è stato precedentemente chiamato il metodo whereToDeploy ma il deploy non è stato confermato
       allora la funzione si occupa di resettare lo stato del counter delle Shards */
    function revertCounterChanges() private 
    {
        if(counterState != CounterInternalStates.CounterNotChanged)
        {
            counter--;
        }
    }

    /* Ritorna la shard su cui il contratto avente l'address passatogli come argomento 
       è deployato. Inoltre ritorna anche la struct corrispondente all'indirizzo del
       contratto passato come argomento. */

    function whereIsContractDeployed(address contractAddress) public view returns (uint256, SmartContract memory)
    {
        return (contractToShard[contractAddress], blockchain[contractToShard[contractAddress]].smartContracts[contractAddress]);
    }
    /* Ritorna un array di indirizzi di tutti contratti contenuti nella shard il cui indice è passato alla funzione come argomento. */
    function returnAllContracts(uint256 shardNumber) public view returns (address[] memory)
    {
        return blockchain[shardNumber].contractsArray;
    }
    /* Ritorna un array di stringhe contenente i nomi degli smart contract contenuti nella shard il cui indice è passato alla funzione come argomento.*/
    function returnAllContractsName(uint256 shardNumber) public view returns (string[] memory)
    {
        return blockchain[shardNumber].contractsArrayName;
    }
    function deleteContract(uint256 shardNumber, address contractAddress) public
    {
        delete(blockchain[shardNumber].smartContracts[contractAddress]);
        uint256 length = blockchain[shardNumber].contractsArray.length;
        for(uint256 i=0; i<blockchain[shardNumber].contractsArray.length; i++)
        {
            if(blockchain[shardNumber].contractsArray[i] == contractAddress)
            {
                blockchain[shardNumber].contractsArray[i] = blockchain[shardNumber].contractsArray[length-1];
                blockchain[shardNumber].contractsArrayName[i] = blockchain[shardNumber].contractsArrayName[length-1];
                blockchain[shardNumber].contractsArray.pop();
                blockchain[shardNumber].contractsArrayName.pop();

            }
        }
    }





}