# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import random
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

        self._totalPower = 0

        self._allyCells = {}
        self._enemyCells = {}
        self._emptyCells = \
            set([HexPos(r,q) for r in range(7) for q in range(7)])

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        return self.randomAction()
    
    def randomAction(self) -> Action:

        if self._totalPower >= 49:
            action = "SPREAD"
        elif len(self._allyCells) == 0:
            action = "SPAWN"
        else:
            action = random.choices(["SPAWN", "SPREAD"], weights=[1,5], k=1)[0]

        match action:
            case "SPAWN":
                return SpawnAction(random.choice(list(self._emptyCells)))
            case "SPREAD":
                return SpreadAction(random.choice(list(self._allyCells.keys())),
                                    random.choice([d for d in HexDir]))
        

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self.spawn(color, cell)
                pass
            case SpreadAction(cell, direction):
                self.spread(color, cell, direction)
                pass

    def spawn(self, color: PlayerColor, cell: HexPos):
        
        self._totalPower += 1
        self._emptyCells.remove(cell)

        if self._color == color:
            self._allyCells[cell] = 1
        else:
            self._enemyCells[cell] = 1
    
    def spread(self, color: PlayerColor, cell: HexPos, dir: HexDir):

        if self._color == color:
            spreadingCells = self._allyCells
            stayingCells = self._enemyCells
        else:
            spreadingCells = self._enemyCells
            stayingCells = self._allyCells
        
        # Value of cell's power
        k = spreadingCells.pop(cell)
        self._emptyCells.add(cell)
        self._totalPower -= k

        # Update the cells in the direction of the SPREAD
        for i in range(1, k+1):

            cur = ((cell.r+i*dir.r)%7, (cell.q+i*dir.q)%7)
            pos = HexPos(cur[0],cur[1])

            if spreadingCells.get(pos):

                if spreadingCells[pos] == 6:
                    self._emptyCells.add(pos)
                    spreadingCells.pop(pos)
                    self._totalPower -= 6
                else:
                    spreadingCells[pos] += 1
                    self._totalPower += 1

            elif stayingCells.get(pos):
                
                val = stayingCells.pop(pos)
                if val < 6:
                    spreadingCells[pos] = val + 1
                    self._totalPower += 1
                else:
                    self._emptyCells.add(pos)
                    self._totalPower -= 6

            else:

                self._emptyCells.remove(pos)
                spreadingCells[pos] = 1
                self._totalPower += 1
