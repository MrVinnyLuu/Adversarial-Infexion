# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from Agent_MCTS.MCTS import *
from agent.GameState import *
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
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
        return self.MCTSAction()       
    
    def MCTSAction(self) -> Action:
        node = MCTSNode(state = GameState(self._gameState))
        return node.bestAction()