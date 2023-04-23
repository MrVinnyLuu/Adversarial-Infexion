# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

import random
from heapq import heappush, heappop
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

# PriorityQueue implemented using heapq
# The closer the priority value is to 0, the higher its priority (ignoring negative numbers)
# Each item is a tuple of (priority, value)
class PQNode:

    def __init__(self, value, priority=0):
        self.value = value
        self.priority = priority
    
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        else:
            return random.choice([True, False])

class PriorityQueue:

    def __init__(self):
        self.heap = []
    
    def add(self, node: PQNode):
        heappush(self.heap, node)
    
    def pop(self):
        return None if not self.heap else heappop(self.heap).value


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
        return self.heuristicAction()
    
    def heuristicAction(self) -> Action:

        actions = PriorityQueue()

        ogPower = self._totalPower
        ogAllies = dict(self._allyCells)
        ogEnemies = dict(self._enemyCells)
        ogEmpties = set(self._emptyCells)

        def revert():
            self._totalPower = ogPower
            self._allyCells = dict(ogAllies)
            self._enemyCells = dict(ogEnemies)
            self._emptyCells = set(ogEmpties)

        if ogPower < 49:
            for cell in ogEmpties:
                action = SpawnAction(cell)
                self.spawn(self._color, cell)
                priority = self.heuristic()
                node = PQNode(action, priority=priority)
                actions.add(node)
                revert()
        
        for cell in ogAllies:
            for dir in HexDir:
                action = SpreadAction(cell, dir)
                self.spread(self._color, cell, dir)
                priority = self.heuristic()
                node = PQNode(action, priority=priority)
                actions.add(node)
                revert()

        return actions.pop()

    
    def heuristic(self) -> int:
        # return len(self._enemyCells)/len(self._allyCells)
        # In each axis, find which lines has enemies
        EoccupiedR = [0]*7
        EoccupiedQ = [0]*7
        EoccupiedP = [0]*7       
        for pos in self._enemyCells.keys():
            EoccupiedR[pos.r] = 1
            EoccupiedQ[pos.q] = 1
            EoccupiedP[(pos.r+pos.q)%7] = 1

        # In each axis, find which lines has allies
        AoccupiedR = [0]*7
        AoccupiedQ = [0]*7
        AoccupiedP = [0]*7
        for pos in self._allyCells.keys():
            AoccupiedR[pos.r] = 1
            AoccupiedQ[pos.q] = 1
            AoccupiedP[(pos.r+pos.q)%7] = 1

        Rs = Qs = Ps = 0
        missingInR = missingInQ = missingInP = 0
        
        for i,x in enumerate(EoccupiedR):
            if x != 0:
                if not AoccupiedR[i]: missingInR = 1
                Rs += 1

        for i,x in enumerate(EoccupiedQ):
            if x != 0:
                if not AoccupiedQ[i]: missingInQ = 1
                Qs += 1

        for i,x in enumerate(EoccupiedP):
            if x != 0:
                if not AoccupiedP[i]: missingInP = 1
                Ps += 1

        return min(Rs+missingInR, Qs+missingInQ, Ps+missingInP)
        

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
