from array import array
from collections import deque   #deque is a list optimized for access at end points
nrows = 0
staticdata = ""
dynamicdata = ""
playerx = playery = 0

playerchar = '@'

def init(board):
    global playerx, playery, nrows, staticdata, dynamicdata
    data = board.splitlines()
    nrows = max(len(r) for r in data) # find length of longest row
    mapstatic = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' '} # Remove player, keep obstacles
    mapdynamic = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*'} # Keep player and goal, remove obstacles
    for ri, row in enumerate(data):
        for ci, ch in enumerate(row):
            staticdata += mapstatic[ch] # map into an array of chars
            dynamicdata += mapdynamic[ch]
            if ch == playerchar:
                playerx = ci
                playery = ri

def push(x,y,dx,dy,data): # check if obstacle is in the way
    # +2 since player position is x,y and the box is going to be placed +2 relative to this after a push
    if staticdata[(y+2*dy) * nrows + x+2*dx] == '#' or data[(y+2*dy) * nrows + x+2*dx] != ' ':
        return None
    # if push is okay:
    newstring = "" 
    newdata = list(data) # array of chars
    newdata[y*nrows + x] = ' ' # clear player pos
    newdata[(y+dy)*nrows + x+dx] = '@' # move player
    newdata[(y+2*dy)*nrows + x+2*dx] = '*' # move box
    return newstring.join(newdata) # return new 'state map' as string

def is_solved(data): # check if data string is a solution
    for i in range(len(data)): # loop through all data chars
        if (staticdata[i] == '.') != (data[i] == '*'): # check if all boxes in data is located on all goals in sdata
            return False # if just one box is not located in a goal
    return True # can only return true if all goals is occupied by a box

def solve_new(data, sata, px, py, bfs = True):
    open = deque([(data, "", px, py)])
    visited = set([data])
    actions = ((0, -1, 'u', 'U'), (1, 0, 'r', 'R'), (0, 1, 'd', 'D'), (-1, 0, 'l', 'L'))
    lnrows = nrows
    while open:
        cur, csol, x, y = open.popleft()
        for action in actions:
            temp = cur
            dx, dy = action[0], action[1]
            if temp[(y+dy) * lnrows + x+dx] == '*': #if action moves player to box
                temp = push(x,y,dx,dy,temp)
                if temp and temp not in visited: #if action was valid AND temp is a so far not visited state
                    if (is_solved(temp)):
                        return csol + action[3] # csol is current string of actions
                    if bfs:
                        open.append((temp, csol + action[3], x+dx, y+dy)) # add to open list with push..... bfs: .append,    dfs: .appendleft
                    else:
                        open.appendleft((temp, csol + action[3], x+dx, y+dy))
                    visited.add(temp)
            else:
                if sata[(y+dy) * lnrows + x+dx] == '#' or temp[(y+dy) * lnrows + x+dx] != ' ': #if actions leads to obstacle
                    continue
                newstr = "" 
                newdata = list(temp) # if next move is non obstacle AND not box
                newdata[y * lnrows + x] = ' '
                newdata[(y+dy) * lnrows + x+dx] = '@'
                temp = newstr.join(newdata)

                if temp not in visited: #if new move have not been visited
                    if ( is_solved(temp) ):
                        return csol+action[2] # if solved - return with new action (safety check - should be ok with check in box push)
                    open.append((temp, csol + action[2], x+dx, y+dy))
                    visited.add(temp)
    return "No solution" # if solution have not been found -- return (open list is empty and no solution found)

def solve(bfs=True): # input bfs or dfs
    open = deque([(dynamicdata, "", playerx, playery)]) # initialise open list with initial map and empty action list
    visited = set([dynamicdata])  # add initial map to visited list
    dirs = ((0, -1, 'u', 'U'), (1, 0, 'r', 'R'), (0, 1, 'd', 'D'), (-1, 0, 'l', 'L')) # action commands: (dx, dy, pl, bo)
    lnrows = nrows
    while open: #while open list is not empty
        cur, csol, x, y = open.popleft() #csol is current list of action

        for di in dirs: #check all actions for state
            temp = cur
            dx, dy = di[0], di[1]

            if temp[(y+dy) * lnrows + x+dx] == '*': #if action moves player to box
                temp = push(x,y,dx,dy,temp)
                if temp and temp not in visited: #if action was valid AND temp is a so far not visited state
                    if (is_solved(temp)):
                        return csol + di[3] # csol is current string of actions
                    if bfs:
                        open.append((temp, csol + di[3], x+dx, y+dy)) # add to open list with push..... bfs: .append,    dfs: .appendleft
                    else:
                        open.appendleft((temp, csol + di[3], x+dx, y+dy))
                    visited.add(temp)
            else:
                if staticdata[(y+dy) * lnrows + x+dx] == '#' or temp[(y+dy) * lnrows + x+dx] != ' ': #if actions leads to obstacle
                    continue
                newstr = "" 
                newdata = list(temp) # if next move is non obstacle AND not box
                newdata[y * lnrows + x] = ' '
                newdata[(y+dy) * lnrows + x+dx] = '@'
                temp = newstr.join(newdata)

                if temp not in visited: #if new move have not been visited
                    if ( is_solved(temp) ):
                        return csol+di[2] # if solved - return with new action (safety check - should be ok with check in box push)
                    open.append((temp, csol + di[2], x+dx, y+dy))
                    visited.add(temp)
    return "No solution" # if solution have not been found -- return (open list is empty and no solution found)

map = """\
#######
#     #
#     #
#. #  #
#. $$ #
#.$$  #
#.#  @#
#######"""

lastYearMap = """\
#######
#.    #
#     #
#.#. .#
#### ##
# $   #
# $   #
#  ####
# $ $@#
#     #
#   ###
#####"""

init(lastYearMap)
# bfs_heuristic returns length
print(len(solve2(dynamicdata, staticdata, playerx, playery)))
print(solve())