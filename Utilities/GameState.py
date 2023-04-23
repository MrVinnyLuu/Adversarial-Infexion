
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir

class GameState:

    def __init__(self, totalPower=0, reds={}, blues={}, empties=None) -> None:
        self.totalPower = totalPower
        self.reds = reds
        self.blues = blues
        if empties:
            self.empties = empties
        else:
            self.empties = \
                set([HexPos(r,q) for r in range(7) for q in range(7)])
    
    def hold(self):
        self.ogPower = self.totalPower
        self.ogReds = dict(self.reds)
        self.ogBlues = dict(self.blues)
        self.ogEmpties = set(self.empties)
    
    def revert(self):
        self.totalPower = self.ogPower
        self.reds = dict(self.ogReds)
        self.blues = dict(self.ogBlues)
        self.empties = set(self.ogEmpties)
    
    def getCells(self, color: PlayerColor):
        match color:
            case PlayerColor.RED:
                return self.reds
            case PlayerColor.BLUE:
                return self.blues
    
    def spawn(self, color: PlayerColor, cell: HexPos):
        
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