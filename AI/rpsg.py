import random as rn

#values of rock, paper, scissors
r,p,s = 0,1,2

#dictionary e.g., rock beats scissors
ws = {r:s, p:r, s:p}


humchips = 100
comchips = 100
totgames = 1
compwins = 0
humwins = 0
gamehistory = []

while humchips != 0 and comchips != 0:

    print("Your current chip count is: " + str(humchips) + ". And the computer's is: " + str(comchips))
    humwager = int(input("What is your wager? "))
    if humwager < 5:
        humwager = 5
    human = int(input("r=0,p=1,s=2 "))

    
    compWager = int(30 * compwins/totgames)
    if compWager < 5:
        compWager = 5
    print("The computer's wager: " + str(compWager))
    grandwager = min(humwager, compWager)
    print("The bet is for " + str(grandwager) + " chips.")
    comp = rn.randrange(0,3,1)
    gamehistory.append([human, comp])

    print("Human: {0}, Comp: {1}".format(human, comp))
        
    if ws[comp] == human:
        compwins += 1
        humchips -= grandwager
        comchips += grandwager
        print("Victory to the ocmputer\n")
    elif ws[human] == comp:
        humwins += 1
        humchips += grandwager
        comchips -= grandwager
        print("Victory to the human\n")
    else:
        print("Tie, no chips lost.\n")
        continue
    totgames += 1

if humchips != 0:
    print("You won!")
else:
    print("The computer won :(")



