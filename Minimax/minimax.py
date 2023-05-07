
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from Utilities.GameState import *

class MinimaxNode:
    def __init__(self, gameState: GameState, color: PlayerColor,
                 parent=None, parentAction:Action=None) -> None:
        self.gameState = gameState
        self.color = color
        self.parent = parent
        self.parentAction = parentAction
        self.children = []
        self.isExpanded = False
        self.minimaxValue = -float('inf')
        self.bestAction = None
        self._untriedActions = self.gameState.getLegalActions()

    def expand(self):
        
        # Expand node to get all its children
        for action in self._untriedActions:
            childState = GameState(state=self.gameState)
            childState.parseAction(action)
            childNode = MinimaxNode(childState, self.color,
                                    parent=self, parentAction=action)
            self.children.append(childNode)

        self.is_expanded = True

    def isTerminalNode(self):
        return self.gameState.isGameOver()

    def getUtilityValue(self):
        return self.gameState.utility()

    def setMinimaxValue(self, value):
        self.minimaxValue = value

    def setBestAction(self, action):
        self.bestAction = action
    
    def evaluate(self):
        # return 10 - self.gameState.utility(self.color)
        return self.gameState.evaluate(self.color)
        