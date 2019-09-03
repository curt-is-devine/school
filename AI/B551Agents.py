from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent
    
class B551Agent(Agent):

    def getAction(self, gameState):
        def getMin(gameState, depth, agentIndex, a, b):
            #Break when a win or loss occurs, or when the depth of the search tree is five levels
            if gameState.isWin() or gameState.isLose():
                return self.evaluationFunction(gameState)
            minScore = sys.maxsize - 1
            actions = gameState.getLegalActions(agentIndex)
            beta = b
            for action in actions:
                newState = gameState.generateSuccessor(agentIndex, action)
                if agentIndex == gameState.getNumAgents() - 1:
                    minScore = min(minScore, getMax(newState, depth, a, beta))
                    if minScore < a:
                        return minScore
                    beta = min(beta, minScore)
                else:
                    minScore = min(minScore, getMin(newState, depth, agentIndex + 1, a, beta))
                    if minScore < a:
                        return minScore
                    beta = min(beta, minScore)
            return minScore

        def getMax(gameState, depth, a, b):
            depth = depth+1
            if gameState.isWin() or gameState.isLose() or depth >= 2:
                return self.evaluationFunction(gameState)
            maxScore = -sys.maxsize + 1
            #Since pacman is the only max agent
            actions = gameState.getLegalActions(0)
            alpha = a
            for action in actions:
                newState = gameState.generateSuccessor(0, action)
                maxScore = max(maxScore, getMin(newState, depth, 1, alpha, b))
                if maxScore > b:
                    return maxScore
                alpha = max(alpha, maxScore)
            return maxScore

        actions = gameState.getLegalActions(0)
        currScore = -sys.maxsize
        nextAction = ''
        alpha = -sys.maxsize
        beta = sys.maxsize
        for action in actions:
            newState = gameState.generateSuccessor(0, action)
            if newState.isWin():
                return action
            newScore = getMin(newState, 0, 1, alpha, beta)
            if newScore > currScore:
                nextAction = action
                currScore = newScore
            if newScore > beta:
                return newAction
            alpha = max(alpha, newScore)
        return nextAction


    def evaluationFunction(self, currentGameState):

        if currentGameState.isWin():
            return sys.maxsize - 1
        if currentGameState.isLose():
            return -sys.maxsize + 1
        
        newPos = currentGameState.getPacmanPosition()
        newFood = currentGameState.getFood()
        newGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        currentScore = currentGameState.getScore()
        
        #saving MANY important variables w.r.t current and future foods, ghosts,
        #and power pellets/scared ghosts
        futFoodsLocs = newFood.asList()
        futFoodsDists = [manhattanDistance(newPos, pos) for pos in futFoodsLocs]
        futGhostDists = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]   
        #No real difference in behavior (+-) since the capsules are far away
        numCapsules = len(currentGameState.getCapsules())
        #+: he stays near the most food, -: chases the most food (doesnt eat in any case)
        sumFoodDists = sum(futFoodsDists)
        sumScared = sum(newScaredTimes)
        sumGhosts = sum(futGhostDists)
        #pursues the food, but depth is limited (dont use +)
        numFoodsLeft = len(futFoodsDists)
        numFoodsEaten = len(newFood.asList(False))
        meanDistToFood = sumFoodDists/numFoodsLeft
        #only moves if he has to, but towards the most food (dont use -)
        distToClosestFood = min(futFoodsDists)
        #+ run away, - chase the ghosts(works surprisingly well)
        distToClosestGhost = min(futGhostDists)

        #I found that including the game's score helps pacman keep moving
        #Instead of staying in one position. I want to thus increase the
        #game's score. Since eating a new pellet increases the actual score
        #by more htan one, adding numFoods left does not hurt Pacman going
        #after a new pellet, he will only want to minimize them        
        score = currentGameState.getScore() + numFoodsLeft
        
        #I want to make pacman move towards the concentration of foods, as
        #makes the above line work far better.
        if sumFoodDists > 0:
            score += 1.0 / sumFoodDists

        #If the ghosts are scared, I want pacman to stay away from the power
        #capsules and get closer to the ghosts so long as they are still scared.
        #As their timer goes down, pacman should move farther away from them
        if sumScared > 0:
            score += sumScared - numCapsules - sumGhosts
        #Otherwise stay away from ghosts and keep the power capsules until necessary
        else:
            score += sumGhosts + numCapsules

        return score
