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
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        
        self._color = color

        self._gameState = GameState()

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        return self.heuristicAction()
    
    def heuristicAction(self) -> Action:

        actions = PriorityQueue()

        self._gameState.hold()

        
        allies = dict(self._gameState.getCells(self._color))

        if self._gameState.ogPower < 49:
            for cell in self._gameState.ogEmpties:
                self._gameState.spawn(self._color, cell)
                node = PQNode(SpawnAction(cell), priority=self.utility())
                actions.add(node)
                self._gameState.revert()

        for cell in allies.keys():
            for dir in HexDir:
                self._gameState.spread(self._color, cell, dir)
                node = PQNode(SpreadAction(cell, dir), priority=self.utility())
                actions.add(node)
                self._gameState.revert()
        
        # for x in actions.heap:
        #     print(x.priority,x.value)

        return actions.pop()

    
    def utility(self) -> int:
        numAllies = len(self._gameState.getCells(self._color))
        numEnemies = 49 - len(self._gameState.empties) - numAllies
        return numEnemies/numAllies

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