# Adapted from https://ai-boson.github.io/mcts/

from collections import defaultdict
from math import sqrt, log
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
        nextState = GameState(self.state)
        nextState.parseAction(action)

        childNode = MCTSNode(nextState, parent=self, parentAction=action)

        self.children.append(childNode)

        return childNode

    def isTerminalNode(self):
        return self.state.isGameOver()

    def rollout(self):
        curRolloutState = self.state

        self.state.hold()

        while not curRolloutState.isGameOver():

            actions = curRolloutState.getLegalActions()
            # action = 

        return curRolloutState.gameResult()
    
    def utilityAction(self) -> Action:

        queue = PriorityQueue()

        self.state.hold()

        for action in self.state.getLegalActions():
            self.state.parseAction(action)
            node = PQNode(action, priority=self.utility())
            queue.add(node)
            self.state.revert()
        
        # for x in queue.heap:
        #     print(x.priority,x.value)

        return queue.pop()
    
    def backpropagate(self, result):
        self._numVisits += 1
        self._results[result] += 1

        if self.parent: self.parent.backpropagate(result)
    
    def isFullyExpanded(self):
        return len(self._untriedActions) == 0
    
    def bestChild(self, c_param=0.1):

        choicesWeights = [(c.q() / c.n()) 
                          + c_param * sqrt((2 * log(self.n()) / c.n())) 
                          for c in self.children]

        idx_max = choicesWeights.index(max(choicesWeights))

        return self.children[idx_max]

    def _treePolicy(self):

        cur = self

        while not cur.isTerminalNode():

            if not cur.isFullyExpanded():
                return cur.expand()
            else:
                cur = cur.bestChild()
        
        return cur

    def bestAction(self):

        simulationNum = 100

        for i in range(simulationNum):

            v = self._treePolicy()
            reward = v.rollout()
            v.backpropagate(reward)
        
        return self.bestChild()
    
    def main():
        root = MCTSNode(state = GameState())
        selectedNode = root.bestAction()
        return
    
    