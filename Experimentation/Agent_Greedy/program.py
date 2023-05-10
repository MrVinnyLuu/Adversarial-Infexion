# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import random
from agent.GameState import *
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
        # random.seed(30024)
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

        bestAction = None
        bestUtility = -float('inf')

        self._gameState.hold()

        for action in self._gameState.getLegalActions():

            self._gameState.parseAction(action)
            utility = self._gameState.evaluate(self._color)

            if utility > bestUtility or \
                (utility == bestUtility and random.choice([True, False])): 
                bestUtility = utility
                bestAction = action

            self._gameState.revert()

        return bestAction