# Loose adaptation of pseudocode from https://en.wikipedia.org/wiki/Minimax and
# https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

import random
from referee.game import PlayerColor, Action, SpawnAction, SpreadAction
from .GameState import *
from .minimax import *

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._gameState = GameState()
        self._maxDepth = 4 # Depth cutoff

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self._gameState.spawn(color, cell)
                pass
            case SpreadAction(cell, direction):
                self._gameState.spread(color, cell, direction)
                pass

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        rootNode = MinimaxNode(gameState = GameState(state=self._gameState),
                               color = self._color)
        self.maximise(rootNode)
        return rootNode.bestAction        

    def maximise(self, node, depth=1, alpha=-float('inf'), beta=float('inf')):
        # Reached terminal node
        if node.isTerminalNode() or depth >= self._maxDepth:
            node.setMinimaxValue(node.utilityValue)
            return node

        if not node.isExpanded:
            node.expand()
            # Pre-sort moves (descending order)
            node.children.sort(key=lambda x: x.utilityValue, reverse=True)

        # Find child node with maximum value
        maxValue = -float('inf') # Fail-soft
        maxNode = None

        for childNode in node.children:

            # Instant termination
            if childNode.utilityValue == float('inf'):
                childNode.setMinimaxValue(float('inf'))
                node.setBestAction(childNode.parentAction)
                return childNode
            
            childValue = \
                self.minimise(childNode, depth+1, alpha, beta).minimaxValue

            if not maxNode or childValue > maxValue or \
                (childValue == maxValue and random.choice([True, False, False])):
                maxValue = childValue
                maxNode = childNode

            alpha = max(alpha, maxValue)

            # Alpha-beta pruning
            if maxValue >= beta: break

        node.setMinimaxValue(maxValue)
        node.setBestAction(maxNode.parentAction)

        return node

    def minimise(self, node, depth, alpha, beta):
        # Reached terminal node
        if node.isTerminalNode() or depth >= self._maxDepth:
            node.setMinimaxValue(node.utilityValue)
            return node

        if not node.isExpanded:
            node.expand()
            # Pre-sort moves (ascending order)
            node.children.sort(key=lambda x: x.utilityValue)
        
        # Find child node with minimum value
        minValue = float('inf') # Fail-soft
        minNode = None
        
        for childNode in node.children:

            # Instant termination
            if childNode.utilityValue == -float('inf'):
                childNode.setMinimaxValue(-float('inf'))
                node.setBestAction(childNode.parentAction)
                return childNode

            childValue = \
                self.maximise(childNode, depth+1, alpha, beta).minimaxValue
    
            if not minNode or childValue > minValue or \
                (childValue == minValue and random.choice([True, False, False])):
                minValue = childValue
                minNode = childNode

            beta = min(beta, minValue)

            # Alpha-beta pruning
            if minValue <= alpha: break

        node.setMinimaxValue(minValue)
        node.setBestAction(minNode.parentAction)

        return node