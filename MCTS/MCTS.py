# Adapted from https://ai-boson.github.io/mcts/

import random
from collections import defaultdict
from math import sqrt, log
from Utilities.GameState import *
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class MCTSNode:

    def __init__(self, state: GameState, parent=None,
                 parentAction:Action=None) -> None:
        
        self.state = state
        self.parent = parent
        self.parentAction = parentAction
        self.children = []

        self._numVisits = 0
        self._results = defaultdict(int)
        self._results[1] = 0 # wins
        self._results[0] = 0 # ties
        self._results[-1] = 0 # loses
        self._untriedActions = self.state.getLegalActions()

    def q(self):
        wins = self._results[1]
        loses = self._results[-1]
        return wins-loses
    
    def n(self):
        return self._numVisits

    def expand(self):

        action = self._untriedActions.pop()
        childState = GameState(state=self.state)
        childState.parseAction(action)

        childNode = MCTSNode(childState, parent=self, parentAction=action)

        self.children.append(childNode)

        return childNode

    def rollout(self):

        curRolloutState = GameState(state=self.state)
        color = PlayerColor.RED if (self.state.turnNum-1)%2 == 1 else PlayerColor.BLUE

        while not curRolloutState.isGameOver():
            action = curRolloutState.utilityAction()
            curRolloutState.parseAction(action)

        return curRolloutState.gameResult(color)

    def backpropagate(self, result):
        self._numVisits += 1
        self._results[result] += 1

        if self.parent: self.parent.backpropagate(result)
    
    def bestChild(self, c_param=0.1):

        choicesWeights = [(c.q() / c.n()) 
                          + c_param * sqrt((2 * log(self.n()) / c.n())) 
                          for c in self.children]

        idx_max = choicesWeights.index(max(choicesWeights))

        return self.children[idx_max]

    def _treePolicy(self):

        cur = self
        
        while not cur.state.isGameOver():
            if len(cur._untriedActions) > 0:
                return cur.expand()
            else:
                cur = cur.bestChild()

        return cur

    def bestAction(self):

        simulationNum = 100

        for _ in range(simulationNum):

            v = self._treePolicy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        # for c in self.children:
        #     print(c.parentAction,c._results[1],c._results[-1],c._numVisits)

        return self.bestChild().parentAction