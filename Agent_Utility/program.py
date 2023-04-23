# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from Utilities.PriorityQueue import PriorityQueue, PQNode
from Utilities.GameState import *
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict) -> None:
        """
        Initialise the agent.
        """
        
        self._color = color

        self._gameState = GameState()

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
        return self.utilityAction()
    
    def utilityAction(self) -> Action:

        queue = PriorityQueue()

        self._gameState.hold()

        for action in self._gameState.getLegalActions(self._color):
            self._gameState.parseAction(self._color, action)
            node = PQNode(action, priority=self.utility())
            queue.add(node)
            self._gameState.revert()
        
        # for x in queue.heap:
        #     print(x.priority,x.value)

        return queue.pop()

    
    def utility(self) -> int:
        numAllies = len(self._gameState.getCells(self._color))
        numEnemies = 49 - len(self._gameState.empties) - numAllies
        return numEnemies/numAllies