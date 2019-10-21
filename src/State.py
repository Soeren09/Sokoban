from Position import Position
class State:
    def __init__(self, boxes, player):
        self.boxes = boxes      # array of Positions
        self.player = player    # Position
    
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


box1 = Position(1,1)
box2 = Position(1,2)
box3 = Position(1,3)
box4 = Position(1,4)
box5 = Position(1,5)
boxes = []
boxes.append(box1)
boxes.append(box2)
boxes.append(box3)
boxes.append(box4)
boxes.append(box5)
player = Position(2,2)
s1 = State(boxes, player)

#boxes.pop(2)
#boxes.append(Position(1,9))
#print(boxes[4].hashCode())
s2 = State(boxes, player)

print(s1.hashCode())
print(s2.hashCode())
#print(s1.equal(s2))