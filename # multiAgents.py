from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.
    """

    def getAction(self, gameState: GameState):
        """
        Chooses among the best options according to the evaluation function.
        """
        legalMoves = gameState.getLegalActions()

        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [i for i in range(len(scores)) if scores[i] == bestScore]
        chosenIndex = random.choice(bestIndices)

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Evaluate the immediate successor state for a proposed action.
        Higher values are better.
        """
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        score = successorGameState.getScore()

        # Discourage stopping
        if action == Directions.STOP:
            score -= 20

        # Reward being closer to food and having less food left
        if newFood:
            minFoodDist = min(manhattanDistance(newPos, food) for food in newFood)
            score += 15.0 / (minFoodDist + 1)
            score -= 4 * len(newFood)

        # Ghost handling
        for ghostState in newGhostStates:
            ghostPos = ghostState.getPosition()
            dist = manhattanDistance(newPos, ghostPos)

            if ghostState.scaredTimer > 0:
                score += 20.0 / (dist + 1)
            else:
                if dist == 0:
                    score -= 1000
                elif dist == 1:
                    score -= 500
                elif dist == 2:
                    score -= 120
                else:
                    score += min(dist, 5)

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    Default evaluation function for adversarial search agents.
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    Common elements to all of your multi-agent searchers.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):

        def minimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth)
            return minValue(state, depth, agentIndex)

        def maxValue(state, depth):
            actions = state.getLegalActions(0)
            if not actions:
                return self.evaluationFunction(state)

            v = float('-inf')
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, minimax(successor, depth, 1))
            return v

        def minValue(state, depth, agentIndex):
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            v = float('inf')
            nextAgent = agentIndex + 1

            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)

                if nextAgent == state.getNumAgents():
                    v = min(v, minimax(successor, depth + 1, 0))
                else:
                    v = min(v, minimax(successor, depth, nextAgent))

            return v

        bestScore = float('-inf')
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = minimax(successor, 0, 1)

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):

        def alphabeta(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth, alpha, beta)
            return minValue(state, depth, agentIndex, alpha, beta)

        def maxValue(state, depth, alpha, beta):
            actions = state.getLegalActions(0)
            if not actions:
                return self.evaluationFunction(state)

            v = float('-inf')
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, alphabeta(successor, depth, 1, alpha, beta))

                if v > beta:
                    return v
                alpha = max(alpha, v)

            return v

        def minValue(state, depth, agentIndex, alpha, beta):
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            v = float('inf')
            nextAgent = agentIndex + 1

            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)

                if nextAgent == state.getNumAgents():
                    v = min(v, alphabeta(successor, depth + 1, 0, alpha, beta))
                else:
                    v = min(v, alphabeta(successor, depth, nextAgent, alpha, beta))

                if v < alpha:
                    return v
                beta = min(beta, v)

            return v

        bestScore = float('-inf')
        bestAction = None
        alpha = float('-inf')
        beta = float('inf')

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = alphabeta(successor, 0, 1, alpha, beta)

            if score > bestScore:
                bestScore = score
                bestAction = action

            alpha = max(alpha, bestScore)

        return bestAction


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):

        def expectimax(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)

            if agentIndex == 0:
                return maxValue(state, depth)
            return expValue(state, depth, agentIndex)

        def maxValue(state, depth):
            actions = state.getLegalActions(0)
            if not actions:
                return self.evaluationFunction(state)

            v = float('-inf')
            for action in actions:
                successor = state.generateSuccessor(0, action)
                v = max(v, expectimax(successor, depth, 1))
            return v

        def expValue(state, depth, agentIndex):
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            nextAgent = agentIndex + 1
            probability = 1.0 / len(actions)
            total = 0

            for action in actions:
                successor = state.generateSuccessor(agentIndex, action)

                if nextAgent == state.getNumAgents():
                    total += expectimax(successor, depth + 1, 0)
                else:
                    total += expectimax(successor, depth, nextAgent)

            return total * probability

        bestScore = float('-inf')
        bestAction = None

        for action in gameState.getLegalActions(0):
            successor = gameState.generateSuccessor(0, action)
            score = expectimax(successor, 0, 1)

            if score > bestScore:
                bestScore = score
                bestAction = action

        return bestAction


def betterEvaluationFunction(currentGameState: GameState):
    """
    Better evaluation function (question 5).

    Uses:
    - current game score
    - distance to nearest food
    - number of food pellets left
    - distance to capsules
    - number of capsules left
    - distance to ghosts, with different behavior for scared ghosts
    """
    score = currentGameState.getScore()

    pos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    ghostStates = currentGameState.getGhostStates()
    capsules = currentGameState.getCapsules()

    # Reward being closer to food and having less food left
    if foodList:
        minFoodDist = min(manhattanDistance(pos, food) for food in foodList)
        score += 10.0 / (minFoodDist + 1)
        score -= 4 * len(foodList)

    # Reward being closer to capsules and having fewer capsules left
    if capsules:
        minCapsuleDist = min(manhattanDistance(pos, cap) for cap in capsules)
        score += 5.0 / (minCapsuleDist + 1)
        score -= 20 * len(capsules)

    # Ghost logic
    for ghost in ghostStates:
        ghostPos = ghost.getPosition()
        dist = manhattanDistance(pos, ghostPos)

        if ghost.scaredTimer > 0:
            score += 20.0 / (dist + 1)
        else:
            if dist == 0:
                score -= 1000
            elif dist == 1:
                score -= 500
            elif dist == 2:
                score -= 200

    return score


# Abbreviation
better = betterEvaluationFunction