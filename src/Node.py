import copy
import State

class Node:
    def __init__(self, state, parent, cost, move):
        self.state = copy.deepcopy(state)   # state
        self.parent = copy.deepcopy(parent) # Parent node, used to backtrace solution.
        self.cost = copy.deepcopy(cost)
        self.move = copy.deepcopy(move)

    def equal(self, s): # check if the node's state is equal to input state
        return self.state.equal(s)   