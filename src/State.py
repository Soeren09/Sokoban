from Position import Position
import copy
class State:
    def __init__(self, boxes, player):
        self.boxes = copy.deepcopy(boxes)      # array of Positions
        self.player = copy.deepcopy(player)    # Position
    
    def hashCode(self):
        hash = 17
        for box in self.boxes:
            print(box.hashCode())
            hash = 37 * hash + box.hashCode()
        hash = 37 * hash + self.player.hashCode()
        return hash

    def equal(self, state):
        if ( state is None ):
            return False
        if ( state.hashCode() == self.hashCode() ):
            if ( state.boxes == self.boxes and state.player == self.player ):
                return True