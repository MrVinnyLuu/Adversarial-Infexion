from referee.game import PlayerColor, Action
from .GameState import *

class MinimaxNode:
    def __init__(self, gameState: GameState, color: PlayerColor,
                 utilityValue:float=0, parentAction:Action=None) -> None:
        
        self.gameState = gameState
        self.color = color
        self.parentAction = parentAction
        
        self._untriedActions = self.gameState.getLegalActions()
        self.children = []
        self.isExpanded = False
        
        self.utilityValue = utilityValue
        self.minimaxValue = -float('inf')
        self.bestAction = None

    def expand(self):
        
        # Expand node to get all its children
        for action in self._untriedActions:
            childState = GameState(state=self.gameState)
            childState.parseAction(action)
            childNode = MinimaxNode(childState, self.color,
                                    utilityValue=childState.evaluate(self.color),
                                    parentAction=action)
            self.children.append(childNode)

        self.is_expanded = True

    def isTerminalNode(self):
        return self.gameState.isGameOver()

    def setMinimaxValue(self, value):
        self.minimaxValue = value

    def setBestAction(self, action):
        self.bestAction = action
        