import random as rn

#values of rock, paper, scissors
r,p,s = 0,1,2

#dictionary e.g., rock beats scissors
ws = {r:s, p:r, s:p}

nogames = int(input("Number of games? "))

totgames = 0
compwins = 0
humwins = 0
ties = 0

gamehistory = []

##while totgames < nogames:
##    human = int(input("r=0,p=1,s=2 "))
##    comp = rn.randrange(0,3,1)
##    gamehistory.append([human, comp])
##
##    print("Human: {0}, Comp: {1}".format(human, comp))
##    
##    if ws[comp] == human:
##        compwins += 1
##    elif ws[human] == comp:
##        humwins += 1
##    else:
##
##
##
##        ties += 1
##    totgames += 1
##
##v = list(map(lambda x: 100*x/totgames, [compwins, humwins, ties]))
##print("Stats\ncw% = {0}, hm% = {1}, ties% = {2}".format(*v))


#Strangely, this methodology worked out such that Robby wins most of the time
#So his expected wins is higher than the computers. naturally, I could have
#simply hardcoded Robby to pick a number one higher than the computer's (or 0
#in the case the computer picked a 2), but this does not really show an attempt
#at understanding the problem (or caring to be smart about solving it)
print("\nNew game between 'Robby' and the computer:")
print("Number of games: 10")
totgames = 0
compwins = 0
robbyWins = 0
ties = 0
gamehistory = []

while totgames < 10:
    robby = rn.randrange(0, 3, 1)
    comp = rn.randrange(0,3,1)
    gamehistory.append([robby, comp])

    print("Robby: {0}, Comp: {1}".format(robby, comp))
    
    if ws[comp] == robby:
        compwins += 1
    elif ws[robby] == comp:
        robbyWins += 1
    else:
        ties += 1
    totgames += 1

v = list(map(lambda x: 100*x/totgames, [compwins, robbyWins, ties]))
print("Stats\ncw% = {0}, rby% = {1}, ties% = {2}".format(*v))
