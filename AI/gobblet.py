#This is as far as I could get with this assignment. I feel as though we
#did not have near enough time to fulfill these requirements at the level
#required of us. Maybe this would have been easier if we were given starter
#code instead of having to develop the whole thing by ourselves. Designing
#game alone is challenging in the attention to detail expected of us, much less
#the actual design of a robot that not only performs logically, but also has
#different difficulty levels and time restraints.

import time

board = {"0,0":[['e']], "0,1":[['e']], "0,2":[['e']], "0,3":[['e']], "1,0":[['e']], "1,1":[['e']], "1,2":[['e']], "1,3":[['e']], "2,0":[['e']], "2,1":[['e']], "2,2":[['e']], "2,3":[['e']], "3,0":[['e']], "3,1":[['e']], "3,2":[['e']], "3,3":[['e']]}
p1Pieces = ["b4", "b3", "b2", "b1", "b4", "b3", "b2", "b1", "b4", "b3", "b2", "b1"]
p2Pieces = ["r4", "r3", "r2", "r1", "r4", "r3", "r2", "r1", "r4", "r3", "r2", "r1"]
seq = []
       
def gobby(players, difficulty, timeLimit):
    if players not in ['h2', 'hr', 'rh', 'r2']:
        return "Invalid player selection, terminating."
    if difficulty not in range(0, 3):
        return "Invalid difficulty selection, terminating."
    for key in board.keys():
        board[key] = [['e']]
    p1Pieces = ["b4", "b3", "b2", "b1", "b4", "b3", "b2", "b1", "b4", "b3", "b2", "b1"]
    p2Pieces = ["r4", "r3", "r2", "r1", "r4", "r3", "r2", "r1", "r4", "r3", "r2", "r1"]
    seq = []
    if players == "h2":
        while exitCondition(seq) == False:
            ls = human('b', p1Pieces, seq)
            p1Pieces = ls[0]
            seq = ls[1]
            if exitCondition(seq) != False:
                break
            ls = human('r', p2Pieces, seq)
            p2Pieces = ls[0]
            seq = ls[1]       
    elif players == 'hr':
        while exitCondition(seq) == False:
            ls = human('b', p1Pieces, seq)
            p1Pieces = ls[0]
            seq = ls[1]
            if exitCondition(seq) != False:
                break
            ls = robot('r', p2Pieces, seq, difficulty, timeLimit)
            p2Pieces = ls[0]
            seq = ls[1]
    elif players == 'rh':
        while exitCondition(seq) == False:
            ls = robot('b', p1Pieces, seq, difficulty, timeLimit)
            p1Pieces = ls[0]
            seq = ls[1]
            if exitCondition(seq) != False:
                break
            ls = human('r', p2Pieces, seq)
            p2Pieces = ls[0]
            seq = ls[1]
    else:
        while exitCondition(seq) == False:
            ls = robot('b', p1Pieces, seq, difficulty, timeLimit)
            p1Pieces = ls[0]
            seq = ls[1]
            if exitCondition(seq) != False:
                break
            ls = robot('r', p2Pieces, seq, difficulty, timeLimit)
            p2Pieces = ls[0]
            seq = ls[1]
    if exitCondition(seq) == 'draq':
        return ['Draw: '] + seq
    return [exitCondition(seq) + ' wins: '] + seq

def human(team, pieces, seq):
    printBoard()
    while True:
        if team == 'b':
            p = input("Blue player: Either move a piece (m) or place a new piece (p): ")            
        else:
            p = input("Red player: Either move a piece (m) or place a new piece (p): ")            
        if p != "m" and p != "p":
            print("Invalid Selection, try again")
            continue
        elif p == "m":
            print("Available moves: ")
            moveable = moving(team)
            print(moveable)
            pMove = input("Select one of the above options to move (ex: '2,1') or 'r' to return to selections: ")
            if pMove == "r":
                continue
            elif pMove not in moveable:
                print("Invalid selection, returning to choices")
                continue
            else:
                loc = input("Select where to move this piece (ex: '1,0'): ")
                if loc not in board.keys() or (getTopElement(loc) != "e" and getPieceValue(loc) >= getPieceValue(pMove)):
                    print("Invalid selection, returning to choices")
                    continue
                piece = board[pMove][0]
                seq = seq + ["Move " + str(piece) + " from " + pMove + " to " + loc]
                board[loc] = [piece] + board[loc]
                board[pMove] = board[pMove][1:]
                break
        else:
            pPlace = input("Select where to put your new piece (ex: '0,3'): ")           
            if pPlace not in board.keys() or (getTopElement(pPlace) != "e" and (getPieceValue(pPlace) >= int(pieces[0][1]))):
                print("Invalid selection, try again")
                continue
            board[pPlace] = [[pieces[0]]] + board[pPlace]
            if team == 'b':
                seq = seq + ["Blue add " + pieces[0] + " piece to space " + pPlace]
            else:
                seq = seq + ["Red add " + pieces[0] + " piece to space " + pPlace]
            pieces = pieces[1:]
            break
    return [pieces, seq]

#Assume the robot knows nothing about opponents stored pieces
def robot(team, pieces, seq, diff, tl):
    #startTime = time.time()
    if diff == 0:
        pieceLocs = moving(team)
        currHeur = heuristic(board)
        opponent = getOpponent(team)
        opponentPieces = moving(opponent)                
        for loc in pieceLocs:
            if board[loc][1][0] == team:
                seq = robotMovePieceAnywhere(loc, opponentPieces, seq)
                return [pieces, seq]
            elif board[loc][1][0] == opponent:
                #compare the next piece in pieces to this piece and see if the placed piece can be optimized/is smaller
                putPiece = pieces[0]
                maxOpPiece = 'p0'
                for opLocation in opponentPieces:
                        if getPieceValue(opLocation) > int(maxOpPiece[1]) and int(maxOpPiece[1]) < int(piece[1]):
                            maxOpPiece = getTopElement(opLocation)
                            continue
                if maxOpPiece == 'p0':
                        for location in board.keys():
                            if board[location] == [['e']]:
                                piece = board[loc][0]
                                seq = seq + ["Move " + str(piece) + " from " + loc + " to " + opLocaiton]
                                board[opLlocation] = [piece] + board[opLocation]
                                board[loc] = board[loc][0]
                                return [pieces, seq]
                elif int(putPiece[1]) >= int(board[loc][0][1]):
                    for opLocation in opponentPieces:
                        if maxOpPiece == getTopElement(opLocation):
                            if team == 'b':
                                seq = seq + ["Blue add " + putPiece + " piece to space " + opLocation]
                            else:
                                seq = seq + ["Red add " + putPiece + " piece to space " + opLocation]
                            board[opLocation] = [putPiece] + board[opLocation]
                            return [pieces, seq]
                else:
                    for opLocation in opponentPieces:
                        if maxOpPiece == getTopElement(opLocation):
                            piece = board[loc][0]
                            seq = seq + ["Move " + str(piece) + " from " + loc + " to " + opLocation]
                            board[loc] = board[loc][1:]
                            board[opLocation] = [board[loc][0]] + board[opLocation]
                            return [pieces, seq]
            else: #Only element on this square
                maxOpPiece = 'p0'
                locVal = getPieceValue(loc)
                for opLocation in opponentPieces:
                    if getPieceValue(opLocation) > int(maxOpPiece[1]) and getPieceValue(opLocation) < locVal:
                        maxOpPiece = getTopElement(opLocation)
                        continue
                if maxOpPiece != 'p0':
                    for opLocation in opponentPieces:
                        if maxOpPiece == getTopElement(opLocation):
                            piece = getTopElement(loc)
                            seq = seq + ["Move " + str(piece) + " from " + loc + " to " + opLocation]
                            board[loc] = board[loc][1:]
                            board[opLocation] = [[piece]] + board[opLocation]
                            return [pieces, seq]
                
                
        putPiece = pieces[0]
        maxOpPiece = 'p0'
        print(putPiece)
        for opLocation in opponentPieces:
            if getPieceValue(opLocation) > int(maxOpPiece[1]) and getPieceValue(opLocation) < int(putPiece[1]):
                maxOpPiece = getTopElement(opLocation)
                continue
        if maxOpPiece == 'p0':
            for location in board.keys():
                if board[location] == [['e']]:
                        if team == 'b':
                            seq = seq + ["Blue add " + putPiece + " piece to space " + location]
                        else:
                            seq = seq + ["Red add " + putPiece + " piece to space " + location]
                        board[location] = [[putPiece]] + board[location]
                        pieces = pieces[1:]
                        return [pieces, seq]
        for opLocation in opponentPieces:
            print("Found some smaller")
            if maxOpPiece == getTopElement(opLocation):
                if team == 'b':
                    seq = seq + ["Blue add " + putPiece + " piece to space " + opLocation]
                else:
                    seq = seq + ["Red add " + putPiece + " piece to space " + opLocation]
                board[opLocation] = [[putPiece]] + board[opLocation]
                pieces = pieces[1:]
                return [pieces, seq]

def robotMovePieceAnywhere(oldLoc, opLocs, seq):
    for opLoc in opLocs:
        if getPieceValue(opLoc) >= getPieceValue(oldLoc):
            continue
        piece = board[oldLoc][0]
        seq = seq + ["Move " + str(piece) + " from " + oldLoc + " to " + opLoc]
        board[opLoc] = [piece] + board[opLoc]
        board[oldLoc] = board[oldLoc][1:]
        return seq
    for loc in board.keys():
        if board[loc] == [['e']]:
            piece = board[oldLoc][0]
            seq = seq + ["Move " + str(piece) + " from " + oldLoc + " to " + loc]
            board[loc] = [piece] + board[loc]
            board[oldLoc] = board[oldLoc][0]
            return seq
    
def getOpponent(team):
    if team == 'r':
        return 'b'
    else:
        return 'r'
    
def heuristic(dic):
    lsB = moving('b')
    lsR = moving('r')
    sumB = 0
    sumR = 0
    for item in lsB:
        sumB += getPieceValue(item)
    for item in lsR:
        sumR += getPieceValue(item)
    return sumB - sumR
    

def printBoard():
    print("\t" + getTopElement("0,3") + "\t|\t" + getTopElement("1,3") + "\t|\t" + getTopElement("2,3") + "\t|\t" + getTopElement("3,3") + "\n" +\
          "\t" + getTopElement("0,2") + "\t|\t" + getTopElement("1,2") + "\t|\t" + getTopElement("2,2") + "\t|\t" + getTopElement("3,2") + "\n" +\
          "\t" + getTopElement("0,1") + "\t|\t" + getTopElement("1,1") + "\t|\t" + getTopElement("2,1") + "\t|\t" + getTopElement("3,1") + "\n" +\
          "\t" + getTopElement("0,0") + "\t|\t" + getTopElement("1,0") + "\t|\t" + getTopElement("2,0") + "\t|\t" + getTopElement("3,0") + "\n")

def moving(player):
    s = []
    for key in board.keys():
        if board[key][0][0] != 'e' and board[key][0][0][0] == player:
            s = s + [key]
    return s
    
def exitCondition(seq):
    if len(seq) >= 2:
        if seq[-1] in seq[:len(seq) - 2]:
            return "draw"
    if board["0,0"][0][0] == board["1,1"][0][0] and board["2,2"][0][0] == board["3,3"][0][0] and board["0,0"][0][0] == board["3,3"][0][0]:
        if board["0,0"][0][0] != "e":
            return board["0,0"][0][0]
    if board["0,3"][0][0] == board["1,2"][0][0] and board["2,1"][0][0] == board["3,0"][0][0] and board["0,3"][0][0] == board["3,0"][0][0]:
        if board["0,3"][0][0] != "e":
            return board["0,3"][0][0]
    for i in range(0, 4):
        j = str(i)
        if board["0," + j][0][0][0] == board["1," + j][0][0][0] and board["2," + j][0][0][0] == board["3,"+ j][0][0][0] and board["0," + j][0][0][0] == board["3," + j][0][0][0]:
            if board["0," + j][0][0] != "e":
                return board["0," + j][0][0][0]
        elif board[j + ",0"][0][0][0] == board[j + ",1"][0][0][0] and board[j + ",2"][0][0][0] == board[j + ",3"][0][0][0] and board[j + ",0"][0][0][0] == board[j + ",3"][0][0][0]:
            if board[j + ",0"][0][0] != "e":
                return board[j + ",0"][0][0][0]
    return False

def getTopElement(loc):
    return board[loc][0][0]

def getPieceValue(loc):
    return int(getTopElement(loc)[1])
