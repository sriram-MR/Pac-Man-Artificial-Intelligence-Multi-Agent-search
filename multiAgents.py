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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        current_food = currentGameState.getFood()
        food_score = 0.0

        for ghostState in newGhostStates:
            ghost_pos = ghostState.getPosition()
            ghost_dist = manhattanDistance(ghost_pos, newPos)
            if (ghost_dist<=1) and (ghostState.scaredTimer==0):
                  food_score=food_score-300
            elif (ghost_dist<=1) and (ghostState.scaredTimer!=0):
                food_score=food_score+1000

        capsule_pos= currentGameState.getCapsules()

        for capsule in capsule_pos:
            capsule_dist= manhattanDistance(capsule, newPos)
            if capsule_dist==0:
                food_score=food_score+200
            else:
                food_score=food_score+(1.0/capsule_dist)

        food_list = current_food.asList()

        for food in food_list:
            food_dist = manhattanDistance(food , newPos)
            if food_dist ==0:
                food_score=food_score+200
            else:
                food_score=food_score+(1.0/food_dist)

        return food_score 


        #"*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

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
      Your minimax agent (question 2)
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
        """
        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()
        score,next_move=self.maximum_function(gameState,self.depth)
        return next_move



    def maximum_function(self,gameState, depth):
        max_value=[]
        max_index=[]
        if gameState.isWin() or gameState.isLose() or depth==0:
          return self.evaluationFunction(gameState)

        legal_action=gameState.getLegalActions()

        for action in legal_action:
            max_value.append(self.minimum_function(gameState.generateSuccessor(self.index,action), depth,1))
        maximum_value=max(max_value)
        
        for i in range(len(max_value)):
            if max_value[i] == maximum_value:
                max_index.append(i)

        max_num = max_index[len(max_index)-1]

        next_move = legal_action[max_num]

        return maximum_value, next_move



    def minimum_function(self,gameState, depth ,agentIndex):
        legal_action=gameState.getLegalActions(agentIndex)
        min_value=[]
        min_index=[]
        num_of_agents = gameState.getNumAgents()-1

        if gameState.isWin() or gameState.isLose() or depth==0:
          return self.evaluationFunction(gameState)

        
        if(agentIndex==num_of_agents):
            for action in legal_action:
                
                min_value.append(self.maximum_function(gameState.generateSuccessor(agentIndex,action),(depth-1)))
        else:
            for action in legal_action:
                min_value.append(self.minimum_function(gameState.generateSuccessor(agentIndex,action),depth,agentIndex+1))
        minimum_value=min(min_value)

        for i in range(len(min_value)):
             if min_value[i] == minimum_value:
                min_index.append(i)

        min_num = min_index[len(min_index)-1]
        next_move = legal_action[min_num]

        return minimum_value, next_move

   


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        #"*** YOUR CODE HERE ***"
        agentIndex = 0
        legal_action= gameState.getLegalActions(agentIndex)
        value = -(float("inf"))
        alpha = -(float("inf"))
        beta = float("inf")
        next_move = ""
        for action in legal_action :
            ghost_pos = self.pruning_function(gameState.generateSuccessor(0, action), 0, 1, alpha, beta)
            if ghost_pos > value:
                value,next_move = ghost_pos,action
            if value > beta:
                return value
            alpha = max(alpha, value)
        return next_move

    def pruning_function(self, gameState, depth ,agentIndex, alpha, beta):

        if agentIndex == 0:
            return self.maximum_function(gameState, depth ,agentIndex, alpha, beta)
        else:
            return self.minimum_function(gameState, depth ,agentIndex, alpha, beta)

    

    def maximum_function(self, gameState, depth ,agentIndex, alpha, beta):
        legal_action= gameState.getLegalActions(agentIndex)
        maximum_value = -(float("inf"))
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        for action in legal_action:
            maximum_value = max(maximum_value, self.pruning_function( gameState.generateSuccessor(agentIndex, action),depth,  1, alpha, beta))
            if maximum_value > beta:
                return maximum_value
            alpha = max(alpha, maximum_value)
        return maximum_value

    

    def minimum_function(self, gameState, depth ,agentIndex, alpha, beta):
        minimum_value = (float("inf"))
        legal_action= gameState.getLegalActions(agentIndex)
        next_agent = agentIndex + 1
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return self.evaluationFunction(gameState)
        if gameState.getNumAgents() == next_agent:
            next_agent = 0
        if next_agent == 0:
            depth = depth + 1
        for action in legal_action:
            minimum_value = min(minimum_value, self.pruning_function(gameState.generateSuccessor(agentIndex, action),depth,  next_agent, alpha, beta))
            if minimum_value < alpha:
                return minimum_value
            beta = min(beta, minimum_value)
        return minimum_value

    

        
        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction
          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        #"*** YOUR CODE HERE ***"
        max_score, next_move = self.expectimax_function(gameState, self.depth, 0)
        return next_move

    def expectimax_function(self, gameState, depth, agentIndex):
        total_agent = gameState.getNumAgents()
        num_of_agents = total_agent-1
        legal_action = gameState.getLegalActions(agentIndex)
        current_state= agentIndex
        next_move = "South"
        next_state = (current_state + 1) % total_agent

        if depth == 0 or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), ""
       
        if current_state == num_of_agents:
            depth =depth - 1
        if current_state != 0:
            max_score = 0
        else:
            max_score = -(float("inf"))
        

        for action in legal_action:
            value = self.expectimax_function(gameState.generateSuccessor(current_state, action), depth, next_state)[0]
            if current_state != 0:
                max_score = max_score+(value/len(legal_action))
                next_move = action
                
            else:
                if max_score < value :
                    max_score = value
                    next_move = action
                
        return max_score, next_move

        # "*** YOUR CODE HERE ***"
        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <This evaluation function executes the pacman problem by finding the states, this is done by calculating the
                    manhattan distance between the pacman position and the relative ghost and the food pellets. The shost is 
                    asked to keep atleast 3 points away from the pacman and the scores are calculated in relation with food pellets
                    , ghosts and the power-up capsule>
    """
    #"*** YOUR CODE HERE ***"
    #util.raiseNotDefined()

    
    current_Pos = currentGameState.getPacmanPosition()
    score = currentGameState.getScore()

    nearest_food = -(float("inf"))
    food_list = currentGameState.getFood().asList()
    for food in food_list:
        food_dist = util.manhattanDistance(food , current_Pos)
        if food_dist < nearest_food:
            nearest_food = food_dist
        
        elif nearest_food == -(float("inf")):
            nearest_food = food_dist
        
        else:
            pass
    score = score+(1.0 / (nearest_food))

    
    current_ghost = currentGameState.getGhostPositions()
    ghost_dist = [3.0]
    for ghostState in current_ghost:
        distance = util.manhattanDistance(ghostState, current_Pos)
        ghost_dist.append(distance)
    score = score-(1.0 / (sum(ghost_dist)))

    
    Capsules = len(currentGameState.getCapsules())
    score = score - Capsules
    
    return score

# Abbreviation
better = betterEvaluationFunction

