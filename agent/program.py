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
        self._color = color
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")
        
        self._reds = {}
        self._blues = {}
        self._empty = set()

        random.seed(0)

        # Add all positions to _empty
        for r in range(7):
            for q in range(7):
                self._empty.add(HexPos(r,q))

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # match self._color:
        #     case PlayerColor.RED:
        #         if (self._reds): return SpreadAction(HexPos(3, 3), HexDir.Up)
        #         return SpawnAction(HexPos(3, 3))
        #     case PlayerColor.BLUE:
        #         return SpawnAction(HexPos(4, 2))
        return self.randomAction()
    
    def randomAction(self) -> Action:
        isEmpty = (len(self._reds)==0) if self._color==PlayerColor.RED else (len(self._blues)==0)
        if isEmpty:
            action = "SPAWN"
        else:
            action = random.choice(["SPAWN", "SPREAD"])

        match action:
            case "SPAWN":
                return SpawnAction(random.choice(list(self._empty)))
            case "SPREAD":
                return SpreadAction(random.choice(list(self._reds.keys()))
                                    if self._color == PlayerColor.RED else random.choice(list(self._blues.keys())),
                                    HexDir.DownRight)
        

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

        print(f"Testing: {color} SPAWN at {cell}")

        self._empty.remove(cell)

        match color:
            case PlayerColor.RED:
                self._reds[cell] = 1
            case PlayerColor.BLUE:
                self._blues[cell] = 1
    
    def spread(self, color: PlayerColor, cell: HexPos, dir: HexDir):
        print(self._empty)
        print(f"Testing: {color} SPREAD from {cell}, {dir}")

        match color:
            case PlayerColor.RED:
                spreadingCells = self._reds
                stayingCells = self._blues
            case PlayerColor.BLUE:
                spreadingCells = self._blues
                stayingCells = self._reds
        
        # assert(spreadingCells.get(cell))

        # Value of cell's power
        k = spreadingCells.pop(cell)
        self._empty.add(cell)

        # Update the cells in the direction of the SPREAD
        for i in range(1, k+1):

            cur = ((cell.r+i*dir.r)%7, (cell.q+i*dir.q)%7)
            pos = HexPos(cur[0],cur[1])

            if spreadingCells.get(pos):

                if spreadingCells[pos] == 6:
                    self._empty.add(pos)
                    spreadingCells.pop(pos)
                else:
                    spreadingCells[pos] += 1

            elif stayingCells.get(pos):

                val = stayingCells.pop(pos)
                if val < 6:
                    spreadingCells[pos] = val + 1
                else:
                    self._empty.add(pos)

            else:

                self._empty.remove(pos)
                spreadingCells[pos] = 1
