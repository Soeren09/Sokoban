import copy
class Position:
    MAX_COL = 1000 # Shared value
    # Init Position with row and column number
    def __init__(self, row, col):
        self.row = copy.deepcopy(row)
        self.col = copy.deepcopy(col)
    # hashCode gives a unique number for each 2D position
    def hashCode(self):
        return self.MAX_COL*self.row + self.col
    # Check if two positions are equal
    def equal(self, pos):
        if ( pos is None ):
            return False
        if ( pos.hashCode() == self.hashCode() ):
            if ( pos.row == self.row and pos.col == self.col ):
                return True
        return False