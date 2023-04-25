
from Utilities.PriorityQueue import PriorityQueue, PQNode
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class GameState:

    def __init__(self, state=None, turnNum = 1, totalPower = 0,
                 reds = {}, blues = {}, empties:set = None) -> None:
        
        if state:
            self.turnNum = state.turnNum
            self.totalPower = state.totalPower
            self.reds = dict(state.reds)
            self.blues = dict(state.blues)
            self.empties = set(state.empties)
            return

        self.turnNum = turnNum
        self.totalPower = totalPower
        self.reds = reds
        self.blues = blues

        if empties != None:
            self.empties = empties
        else:
            self.empties = set([HexPos(r,q) 
                                for r in range(7)
                                for q in range(7)])
    
    def hold(self):
        self.ogTurnNum = self.turnNum
        self.ogPower = self.totalPower
        self.ogReds = dict(self.reds)
        self.ogBlues = dict(self.blues)
        self.ogEmpties = set(self.empties)
    
    def revert(self):
        self.turnNum = self.ogTurnNum
        self.totalPower = self.ogPower
        self.reds = dict(self.ogReds)
        self.blues = dict(self.ogBlues)
        self.empties = set(self.ogEmpties)
    
    def isGameOver(self):
        return self.turnNum > 2 and (len(self.reds) == 0 or len(self.blues) == 0
                                     or self.turnNum > 343)
    
    def gameResult(self):

        if len(self.reds) == 0 and len(self.blues) == 0:
            return 0
        elif self.turnNum > 343 and \
            abs(sum(self.reds.values())-sum(self.blues.values())) < 2:
            return 0
                
        winner = PlayerColor.RED if len(self.reds) > len(self.blues) else PlayerColor.BLUE

        curPlayer = PlayerColor.RED if (self.turnNum-1)%2 == 1 else PlayerColor.BLUE

        return 1 if curPlayer == winner else -1

    def getCells(self, color: PlayerColor):
        match color:
            case PlayerColor.RED:
                return self.reds
            case PlayerColor.BLUE:
                return self.blues
    
    def getLegalActions(self):

        actions = []
        color = PlayerColor.RED if self.turnNum%2 == 1 else PlayerColor.BLUE

        if self.totalPower < 49:
            for cell in self.empties:
                actions.append(SpawnAction(cell))

        for cell in self.getCells(color).keys():
            for dir in HexDir:
                actions.append(SpreadAction(cell, dir))
        
        return actions

    def parseAction(self, action: Action):
        color = PlayerColor.RED if self.turnNum%2 == 1 else PlayerColor.BLUE
        if "SPAWN" in str(action):
            self.spawn(color, action.cell)
        elif "SPREAD" in str(action):
            self.spread(color, action.cell, action.direction)
    
################################################################################
    def utilityAction(self) -> Action:

        bestAction = None
        bestUtility = -1

        self.hold()

        for action in self.getLegalActions():
            self.parseAction(action)
            utility = self.utility()
            if utility < bestUtility or bestUtility == -1:
                bestUtility = utility
                bestAction = action
            self.revert()

        return bestAction
################################################################################

    def utility(self) -> int:

        color = PlayerColor.RED if (self.turnNum-1)%2 == 1 else PlayerColor.BLUE

        powerAllies = sum(self.getCells(color).values())
        powerEnemies = self.totalPower - powerAllies
        numAllies = len(self.getCells(color))
        numEnemies = 49 - len(self.empties) - numAllies

        if powerAllies == 0: return -1
        
        return (numEnemies + powerEnemies)/(numAllies + powerAllies)

    def spawn(self, color: PlayerColor, cell: HexPos):

        self.turnNum += 1
        self.totalPower += 1
        self.empties.remove(cell)

        match color:
            case PlayerColor.RED:
                self.reds[cell] = 1
                pass
            case PlayerColor.BLUE:
                self.blues[cell] = 1
                pass
    
    def spread(self, color: PlayerColor, cell: HexPos, dir: HexDir):
        
        self.turnNum += 1

        match color:
            case PlayerColor.RED:
                spreadingCells = self.reds
                stayingCells = self.blues
                pass
            case PlayerColor.BLUE:
                spreadingCells = self.blues
                stayingCells = self.reds
                pass
        
        # Value of cell's power
        k = spreadingCells.pop(cell)
        self.empties.add(cell)
        self.totalPower -= k

        # Update the cells in the direction of the SPREAD
        for i in range(1, k+1):

            cur = ((cell.r+i*dir.r)%7, (cell.q+i*dir.q)%7)
            pos = HexPos(cur[0],cur[1])

            if spreadingCells.get(pos):

                if spreadingCells[pos] == 6:
                    self.empties.add(pos)
                    spreadingCells.pop(pos)
                    self.totalPower -= 6
                else:
                    spreadingCells[pos] += 1
                    self.totalPower += 1

            elif stayingCells.get(pos):
                
                val = stayingCells.pop(pos)
                if val < 6:
                    spreadingCells[pos] = val + 1
                    self.totalPower += 1
                else:
                    self.empties.add(pos)
                    self.totalPower -= 6

            else:

                self.empties.remove(pos)
                spreadingCells[pos] = 1
                self.totalPower += 1