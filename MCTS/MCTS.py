# Adapted from https://ai-boson.github.io/mcts/

from collections import defaultdict
from Utilities.GameState import *
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class MCTSNode:
    def __init__(self, state: GameState, parent:GameState=None,
                 parentAction:Action=None) -> None:
        
        self.state = state
        self.parent = parent
        self.parentAction = parentAction
        self.children = []

        self._numVisits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untriedActions = self.untriedActions()

    def untriedActions(self):
        self._untriedActions = self.state.getLegalActions()
        return self._untriedActions

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins-loses

    def n(self):
        return self._numVisits

    def expand(self):
        action = self._untriedActions.pop()
