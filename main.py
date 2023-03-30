















if __name__ == '__main__':
    print("Ciao")

    x = True


    print("Puoi effettuare il deploy di uno smart contract o eseguire una transazione\nDi seguito le scelte:\n1. Esegui un deploy\n2. Esegui una transazione\n\nLa digitazione di qualunque altro carattere comporterà la terminazione del programma.")
    choiche = input(">>> ")
    while(x):
        match choiche:
            case '1':
                print("Quale smart contract vuoi deployare?")
                choiche = '3'
            case '2':
                print("Quale transazione si vuole effettuare?")
                choiche = '3'
            case default:
                print("Carattere sbagliato")
                x = False



                prova