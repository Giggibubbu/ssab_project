
# Punto di partenza del programma
import User

if __name__ == '__main__':
    x = True
    loggedUser = ''

    while(x):

        print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il login\n2. Effettua la registrazione\n3. Termina l'esecuzione\nLa digitazione di qualunque altro carattere comporterà la terminazione del programma.")
        choiche = input(">>> ")   



        match choiche:
            case '1':
                print("Inserisci la chiave pubblica e la chiave privata")
                loggedUser = User()
                #loginResult == 1 allora si deve ritornare a richiestadeploy e richiesta metodo (menu) 
                #loginResult == 0 allora si f
                # a tornare l'utente allo switch esterno
                loginResult = True
                while(loginResult):
                    print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Effettua il deploy\n2. Effettua una transazione\n3. Effettua il logout\n")

                    loggedChoiche = input('>>> ')
                    match loggedChoiche:
                        case '1':
                            # deploy()
                            print("Deploy effettuato")
                            loggedChoiche = '1'
                        case '2':
                            
                            print("Transazione effettuata")
                            loggedChoiche = '2'
                        case '3':
                            # dimentica l'utente
                            print("Logout effettuato")
                            loggedChoiche = '3'
                            loginResult = False
                        case default:
                            print("Carattere errato")  



                choiche = '1'

            case '2':
                print("Generazione della chiave privata e pubblica...\n...")
                print("Utente registrato!")
                choiche = '2'
            case '3':
                print("Termina l'esecuzione")
                choiche = '3'
                x = False
            case default:
                print("Il carattere digitato non corrisponde ad alcuna funzionalità")
                