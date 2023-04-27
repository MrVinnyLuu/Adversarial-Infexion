# Implementation of pseudocode from https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from Utilities import *
from agent.minimax import *

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._gameState = GameState()
        self._maxDepth = 3

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
        return self.minimaxAction();

    def minimaxAction(self) -> Action:
        root_node = MinimaxNode(gameState = GameState(state=self._gameState))
        self.maximise(root_node, 1)
        return root_node.bestAction

    def maximise(self, node, depth, alpha=-float('inf'), beta=float('inf')):
        #print("depth:", depth)
        # Reached terminal node
        if node.isTerminalNode() or depth >= self._maxDepth:
            node.setMinimaxValue(node.gameState.utility())
            return node

        if not node.isExpanded:
            node.expand()

        # Find child node with maximum value
        max_value = -float('inf')
        max_node = None
        for child_node in node.children:
            child_value = self.minimise(child_node, depth+1, alpha, beta).minimaxValue
            if child_value > max_value:
                max_value = child_value
                max_node = child_node

            # Alpha-beta pruning
            if max_value > beta:
                break

            alpha = max(alpha, max_value)

        node.setMinimaxValue(max_value)
        node.setBestAction(max_node.parentAction)

        return node

    def minimise(self, node, depth, alpha, beta):
        #print("depth:", depth)
        # Reached terminal node
        if node.isTerminalNode() or depth >= self._maxDepth:
            node.setMinimaxValue(node.gameState.utility())
            return node

        if not node.isExpanded:
            node.expand()
        
        # Find child node with minimum value
        min_value = float('inf')
        min_node = None
        for child_node in node.children:
            child_value = self.maximise(child_node, depth+1, alpha, beta).minimaxValue
            if child_value < min_value:
                min_value = child_value
                min_node = child_node

            # Alpha-beta pruning
            if min_value < alpha:
                break

            beta = min(beta, min_value)

        node.setMinimaxValue(min_value)
        node.setBestAction(min_node.parentAction)

        return node