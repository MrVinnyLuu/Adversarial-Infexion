
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir
from Utilities.GameState import *

class MinimaxNode:
    def __init__(self, gameState: GameState, parent=None, parentAction:Action=None) -> None:
        self.gameState = gameState
        self.parent = parent
        self.parentAction = parentAction
        self.children = []
        self.is_expanded = False
        self.minimax_value = -float('inf')
        self.best_action = None
        self._untriedActions = self.gameState.getLegalActions()

    def expand(self):
        # Expand node to get all its children
        while (len(self._untriedActions) > 0):
            action = self._untriedActions.pop()
            childState = GameState(state=self.gameState)
            childState.parseAction(action)

            childNode = MinimaxNode(childState, parent=self, parentAction=action)
            self.children.append(childNode)
        
        self.is_expanded = True
    
    def isTerminalNode(self):
        return self.gameState.isGameOver()

    def getUtilityValue(self):
        return self.gameState.utility()

    def setMinimaxValue(self, value):
        self.minimax_value = value

    def setBestAction(self, action):
        self.best_action = action