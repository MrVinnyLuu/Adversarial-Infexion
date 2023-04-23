# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import random
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
        # random.seed(0)

        self._color = color

        self._gameState = GameState()

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        return self.randomAction()
    
    def randomAction(self) -> Action:

        if self._gameState.totalPower >= 49:
            action = "SPREAD"
        elif len(self._gameState.getCells(self._color)) == 0:
            action = "SPAWN"
        else:
            action = random.choices(["SPAWN", "SPREAD"], weights=[1,5], k=1)[0]

        match action:
            case "SPAWN":
                return SpawnAction(random.choice(list(self._gameState.empties)))
            case "SPREAD":
                return SpreadAction(
                    random.choice(list(self._gameState.getCells(self._color).keys())),
                    random.choice([d for d in HexDir]))
        

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