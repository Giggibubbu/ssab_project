# Progetto del corso di Software Security and Blockchain AA 2022-23 - Gruppo 2

## Descrizione

Il progetto ha come obiettivo quello di costruire un programma che permetta all'utente finale di interfacciarsi con le varie blockchain.
Per fare ciò è stato necessario creare uno Smart Contract di Management di cui viene fatto il deploy alla prima esecuzione del programma e deployato su una blockchain dedicata, detta di Management.
Quest'ultimo viene utilizzato per due scopi:
- Eseguire il bilanciamento dei deploy richiesti dagli utenti sulle varie Shard. Le Shard sono delle blockchain come quella di Management, nelle quali viene però eseguito il deploy degli Smart Contract non di Management;
- Consentire all'Offchain Manager di rintracciare su quale Shard è presente lo Smart Contract su cui è presente il metodo richiamato dall'utente.
Dunque, l'utente potrà eseguire i metodi sugli smart contract attualmente presenti sulle shard o effettuare un deploy di uno smart contract ex novo per poi poter eseguire i suoi metodi.

## Guida all'installazione e all'esecuzione

### Requisiti

* Ganache
* Python 3.11

### Installazione

* Installare Git ed effettuare un git clone del repository altrimenti scaricare lo zip del progetto tramite la sua pagina GitHub.

```
git clone package_name
```

* Dopo aver installato Python 3.11, effettuare installazione tramite pip delle librerie py-solc-x, web3, jsonpickle tramite il seguente comando:

```
pip install package_name
```

* Installare Ganache e configurare un numero a piacimento di blockchain, considerando che una sarà quella dedicata al Management.

* Configurare il file conf.ini sostituendo i link di default dei parametri managementAddress e shardAddresses con gli indirizzi http della propria blockchain di Management e delle proprie Shard.
Di seguito verrà illustrata la posizione dei detti parametri nel file tramite la loro delimitazione tra frecce (-----> <-----).
Mantenere separati i link dal carattere ';' come nel seguente esempio.

```
# Blockchain system configuration #
# Change the parameters value below for the system configuration phase.
# Note that if you change the current file layout or parameters name, system will not recognize it as a configuration file and the program will be terminated.
# This file is fundamental for the program first startup phase. (initial deploy of management smart contract)

# Indicate one management address and at least two shard addresses, separated by ; #
[bchManagement]
-----> managementAddress=http://127.0.0.1:8545  <-----
[shardsSettings]
-----> shardAddresses=http://127.0.0.1:8546;http://127.0.0.1:8547 <-----
```

### Esecuzione

* Eseguire il main.py posizionandosi nella directory di progetto tramite il seguente comando:

```
py main.py
```

* Il programma mostrerà la seguente schermata:

```
Puoi effettuare il deploy di uno smart contract o eseguire una transazione
Di seguito le scelte:
1. Effettua il login
2. Termina l'esecuzione.
```

* Scegliendo la prima opzione, il programma chiederà di inserire la chiave privata nel formato con lo '0x' iniziale.

Successivamente verrà mostrato il menù principale per l'esecuzione delle azioni previste dal programma.

```
Puoi effettuare il deploy di uno smart contract o eseguire una transazione
Di seguito le scelte:
1. Effettua il deploy
2. Effettua una transazione
3. Elimina smart contract
4. Effettua il logout
```

## Autori
- De Stasio Giuseppe
- Lorenzo Olivieri 
- Martina Mammarella
- Simone Murazzo
