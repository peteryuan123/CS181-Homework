# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        print("newpso:",newPos)
        print("newfood:",type(currentGameState))
        print("newgoststate:",newGhostStates)
        print("newscaredtimes:", newScaredTimes)
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 1)
    """

    def getAction(self, gameState):
        
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        pac_legalActions = gameState.getLegalActions(0)
        pac_scores = []
        for act in pac_legalActions:
            successor = gameState.generateSuccessor(0,act)
            pac_scores.append(self.value(successor,1,self.depth))
        bestscore = max(pac_scores)
        bestIndices = [index for index in range(len(pac_scores)) if pac_scores[index] == bestscore]
        chosenIndex = random.choice(bestIndices)

        return pac_legalActions[chosenIndex] 

    def value(self,gameState,agentIndex,depth):
        if(gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0 and depth == 0):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0):
            return self.max_value(gameState,agentIndex,depth)
        else:
            return self.min_value(gameState,agentIndex,depth)
    
    def max_value(self,gameState,agentIndex,depth):
        v = float("-Inf")
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth

        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v = max(v,self.value(successor,next_agent, new_depth))

        return v

    def min_value(self,gameState,agentIndex,depth):
        v = float("Inf")
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth

        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v = min(v,self.value(successor,next_agent, new_depth))
        
        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        pac_legalActions = gameState.getLegalActions(0)
        pac_scores = []
        alpha = float("-Inf")
        beta = float("Inf")
        for act in pac_legalActions:
            successor = gameState.generateSuccessor(0,act)
            v = self.value(successor,1,self.depth,alpha,beta)
            pac_scores.append(v)
            if(v >= beta):
                break
            alpha = max(alpha,v)
            
        bestscore = max(pac_scores)
        bestIndices = [index for index in range(len(pac_scores)) if pac_scores[index] == bestscore]
        chosenIndex = random.choice(bestIndices)

        return pac_legalActions[chosenIndex] 

    def value(self,gameState,agentIndex,depth,alpha,beta):
        if(gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0 and depth == 0):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0):
            return self.max_value(gameState,agentIndex,depth,alpha,beta)
        else:
            return self.min_value(gameState,agentIndex,depth,alpha,beta)
    
    def max_value(self,gameState,agentIndex,depth,alpha,beta):
        v = float("-Inf")
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth

        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v = max(v,self.value(successor,next_agent, new_depth,alpha,beta))
            if(v > beta):
                return v
            alpha = max(alpha,v)
        return v

    def min_value(self,gameState,agentIndex,depth,alpha,beta):
        v = float("Inf")
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth

        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v = min(v,self.value(successor,next_agent, new_depth,alpha,beta))
            if(v < alpha):
                return v
            beta = min(beta,v)
        return v


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pac_legalActions = gameState.getLegalActions(0)
        pac_scores = []
        for act in pac_legalActions:
            successor = gameState.generateSuccessor(0,act)
            pac_scores.append(self.value(successor,1,self.depth))
        bestscore = max(pac_scores)
        bestIndices = [index for index in range(len(pac_scores)) if pac_scores[index] == bestscore]
        """ print(bestscore)
        print(pac_scores)
        print(bestIndices)"""
        chosenIndex = random.choice(bestIndices)

        return pac_legalActions[chosenIndex] 

    def value(self,gameState,agentIndex,depth):
        if(gameState.isLose() or gameState.isWin()):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0 and depth == 0):
            return self.evaluationFunction(gameState)
        if(agentIndex == 0):
            return self.max_value(gameState,agentIndex,depth)
        else:
            return self.exp_value(gameState,agentIndex,depth)
    
    def max_value(self,gameState,agentIndex,depth):
        v = float("-Inf")
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth

        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v = max(v,self.value(successor,next_agent, new_depth))

        return v

    def exp_value(self,gameState,agentIndex,depth):
        v = 0
        actions = gameState.getLegalActions(agentIndex)

        if(agentIndex == gameState.getNumAgents() - 1):
            next_agent = 0
            new_depth = depth - 1
        else:
            next_agent = agentIndex + 1
            new_depth = depth
        p = float(1) / float(len(actions))
        for act in actions:
            successor = gameState.generateSuccessor(agentIndex,act)
            v += p * self.value(successor,next_agent,new_depth)
        
        return v

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 4).

    DESCRIPTION: <write something here so we know what you did>
    """
    # Useful information you can extract from a GameState (pacman.py)
    if(currentGameState.isWin()):
        return float("Inf")
    if(currentGameState.isLose()):
        return float("-Inf")
    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    capsules = currentGameState.getCapsules()

    foodscore = Food.count(False)
           
    capscore = 0
    for capsule in capsules:
        capscore -= manhattanDistance(Pos,capsule)

    ghost_num = len(GhostStates)
    ghost_p = float(1) / float(ghost_num)
    ghost_score = 0
    for ghost in GhostStates:
        steps = manhattanDistance(currentGameState.getPacmanPosition(),ghost.getPosition())
        ghost_score += ghost_p * steps
    
    scaredtime_score = 0
    for time in ScaredTimes:
        scaredtime_score += ghost_p * time
    scaredtime_score = -0.005 * scaredtime_score



    score = 0.8 * foodscore + 0.7 * capscore + scaredtime_score * ghost_score + currentGameState.getScore()


    return score
    

# Abbreviation
better = betterEvaluationFunction
