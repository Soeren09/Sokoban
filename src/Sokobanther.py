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

def solve(data, sata, px, py, bfs = True):
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

def astar(dynamicdata, staticdata, playerx, playery):
    g = 0
    h = manhattan_dist_metric(dynamicdata, staticdata)
    #manhattan dist from dynamicdata and staticdata
    cost = g+h
    open = []
    open.append((cost , dynamicdata, "", playerx, playery))
    visited = set([dynamicdata])
    actions = ((0, -1, 'u', 'U'), (1, 0, 'r', 'R'), (0, 1, 'd', 'D'), (-1, 0, 'l', 'L'))
    lnrows = nrows
    while open:
        cost, cur, csol, x, y = open.pop(0) #data.sort(key=lambda tup: tup[1])
        g = g + 1
        if (is_solved(cur)):
            return csol
        
        for action in actions:
            temp = cur
            dx, dy = action[0], action[1]
            if temp[(y+dy) * lnrows + x+dx] == '*': #if action moves player to box
                temp = push(x,y,dx,dy,temp)
                if temp and temp not in visited: #if action was valid AND temp is a so far not visited state
                    cost = g + manhattan_dist_metric(temp, staticdata)
                    added = False
                    for indx, (ci, curi, csoli, xi, yi) in enumerate(open):
                        if cost < ci:
                            added = True
                            open.insert(indx, (cost, temp, csol + action[3], x+dx, y+dy))
                            break
                    if not added:
                        open.append((cost, temp, csol + action[3], x+dx, y+dy))
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
                        return csol+action[2] # if solved - return with new action (safety check - should be ok with check in box push)
                    added = False
                    for indx, (ci, curi, csoli, xi, yi) in enumerate(open):
                        if cost < ci:
                            added = True
                            open.insert(indx, (cost, temp, csol + action[2], x+dx, y+dy))
                            break
                    if not added:
                        open.append((cost, temp, csol + action[2], x+dx, y+dy))
                    visited.add(temp)
    return "No solution" # if solution have not been found -- return (open list is empty and no solution found)    

def manhattan_dist_metric(dynamicdata, staticdata, stackable=True):
    boxes = []
    goals = []
    for i, ch in enumerate(dynamicdata):
        if (ch == '*'):
            col = i % nrows
            row = i // nrows
            boxes.append((row, col))
    for i, ch in enumerate(staticdata):
        if (ch == '.'):
            col = i % nrows
            row = i // nrows
            goals.append((row, col))
    box2GoalDistSum = 0
    for (boxrow, boxcol) in boxes:
        minDist = 99999999
        minGoal = (0,0)
        for (goalrow, goalcol) in goals:
            if stackable:
                curDist = abs(goalrow-boxrow) + abs(goalcol-boxcol)
                if ( curDist < minDist ):
                    minDist = curDist
                    minGoal = (goalrow, goalcol)
            else:
                pass
                #write routine to handle non stackable boxes
        box2GoalDistSum = box2GoalDistSum + minDist
    return box2GoalDistSum


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
solution = solve(dynamicdata, staticdata, playerx, playery)
print(len(solution))
print(solution)


#print(manhattan_dist_metric(dynamicdata, staticdata))