from array import array
from collections import deque   #deque is a list optimized for access at end points
from memory_profiler import memory_usage
import time
import statistics
import threading
import matplotlib.pyplot as plt 
import numpy as np

nrows = 0
staticdata = ""
dynamicdata = ""
playerx = playery = 0

player   = 'M'
wall     = 'X'
jewel    = 'J'
goal     = 'G'
clear    = '.'

def init(board):
    global playerx, playery, nrows, staticdata, dynamicdata
    data = board.splitlines()
    nrows = max(len(r) for r in data) # find length of longest row
    mapstatic   = {clear:clear, goal: goal,  player:clear,  wall:wall,  jewel:clear} # Remove player, keep obstacles
    mapdynamic  = {clear:clear, goal: clear, player:player, wall:clear, jewel:jewel} # Keep player and goal, remove obstacles
    #mapstatic  = {' ':' ', '.': '.', '@':' ', '#':'#', '$':' '} # Remove player, keep obstacles
    #mapdynamic = {' ':' ', '.': ' ', '@':'@', '#':' ', '$':'*'} # Keep player and goal, remove obstacles
    for ri, row in enumerate(data):
        for ci, ch in enumerate(row):
            staticdata += mapstatic[ch] # map into an array of chars
            dynamicdata += mapdynamic[ch]
            if ch == player:
                playerx = ci
                playery = ri


def push(x,y,dx,dy,data): # check if obstacle is in the way
    # +2 since player position is x,y and the box is going to be placed +2 relative to this after a push
    if staticdata[(y+2*dy) * nrows + x+2*dx] == wall or data[(y+2*dy) * nrows + x+2*dx] != clear:
        return None
    # if push is okay:
    newstring = "" 
    newdata = list(data) # array of chars
    newdata[y*nrows + x] = clear # clear player pos
    newdata[(y+dy)*nrows + x+dx] = player # move player
    newdata[(y+2*dy)*nrows + x+2*dx] = jewel # move box
    return newstring.join(newdata) # return new 'state map' as string

def is_solved(data): # check if data string is a solution
    for i in range(len(data)): # loop through all data chars
        if (staticdata[i] == goal) != (data[i] == jewel): # check if all boxes in data is located on all goals in sdata
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
            if temp[(y+dy) * lnrows + x+dx] == jewel: #if action moves player to box
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
                if sata[(y+dy) * lnrows + x+dx] == wall or temp[(y+dy) * lnrows + x+dx] != clear: #if actions leads to obstacle
                    continue
                newstr = "" 
                newdata = list(temp) # if next move is non obstacle AND not box
                newdata[y * lnrows + x] = clear
                newdata[(y+dy) * lnrows + x+dx] = player
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
            if temp[(y+dy) * lnrows + x+dx] == jewel: #if action moves player to box
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
                if staticdata[(y+dy) * lnrows + x+dx] == wall or temp[(y+dy) * lnrows + x+dx] != clear: #if actions leads to obstacle
                    continue
                newstr = "" 
                newdata = list(temp) # if next move is non obstacle AND not box
                newdata[y * lnrows + x] = clear
                newdata[(y+dy) * lnrows + x+dx] = player
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
        if (ch == jewel):
            col = i % nrows
            row = i // nrows
            boxes.append((row, col))
    for i, ch in enumerate(staticdata):
        if (ch == goal):
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


# goal = G = .
# box = J = $
# player = M = @
#solution = solve(dynamicdata, staticdata, playerx, playery)
#print(len(solution))
#print(solution)

#solution = "llllUddlluRRRRRdrUUruulldRRdldlluLuulldRurDDullDRdRRRdrUUruurrdLulDulldRddlllluurDldRRRdrUUdlllldlluRRRRRdrU"
#print(map_2019)
def translateCommand(commands): # no predined
    prev_is_upper = False
    prev_command = 'N'
    translated = ""
    for i in range(len(commands)):
        if ( ord(commands[i]) >= 65 and ord(commands[i]) <= 90 ):
            if ( prev_is_upper and prev_command == commands[i] ): # upper and equal to last -> for consecutive uppers add 1
                translated += commands[i].lower()
                prev_is_upper = True
                prev_command = commands[i]
            else: ## Upper not equal to last -> first upper add 2
                translated += commands[i].lower()
                translated += commands[i].lower()
                prev_is_upper = True
                prev_command = commands[i]
            # check if current is last push -> add x (reverse)
            if ( i+1 < len(commands) and commands[i+1] != prev_command):
                translated += 'x'
        else: # not upper
            translated += commands[i]
            prev_is_upper = False
            prev_command = 'N'
    return translated

def translateCommandPreDef(commands): # using predefined push length
    prev_is_upper = False
    prev_command = 'N'
    translated = ""
    for i in range(len(commands)):
        if ( ord(commands[i]) >= 65 and ord(commands[i]) <= 90 ):
            if ( prev_is_upper and prev_command == commands[i] ): # upper and equal to last -> for consecutive uppers add 1
                translated += commands[i].lower()
                prev_is_upper = True
                prev_command = commands[i]
            else: ## Upper not equal to last -> first upper add 2
                translated += commands[i].lower()
                translated += commands[i].lower()
                prev_is_upper = True
                prev_command = commands[i]
            # check if current is last push -> add x (reverse)
            if ( i+1 < len(commands) and commands[i+1] != prev_command):
                translated += 'x'
        else: # not upper
            translated += commands[i]
            prev_is_upper = False
            prev_command = 'N'
    return translated

###############################################
#           USAGE OF SOLVER                   # 
###############################################
map_2019 = """\
XXXXXXXXXXXX
XX...X.....X
XX...X.GG..X
XXJJJ.XGGXXX
X.J....MXXXX
X...X...XXXX
XXXXXXXXXXXX"""

print("--- Solve 2019 competition map ---")
init(map_2019)
solution = solve(dynamicdata, staticdata, playerx, playery)
print(translateCommandPreDef(solution))


###############################################
#           TEST OF SOLVER BELOW THIS         # 
###############################################
print("--- Running tests of Solver ---")
map1 = """\
XXXXXXXXXXXX
XX...X.....X
XX...X.GG..X
XXJJJ.XGGXXX
X.J....MXXXX
X...X...XXXX
XXXXXXXXXXXX"""

map2 = """\
XXXXXXX
XG....X
X.....X
XGXG.GX
XXXX.XX
X.J...X
X.J...X
X..XXXX
X.J.JMX
X.....X
X...XXX
XXXXX"""

map3 = """\
XXXXXXXX
X...X..X
XJX.X..X
X...XJ.X
XG.X..XX
X....JGX
XXG.XM.X
XXXXXXXX
"""

map4 = """\
XXXXXXXX
X...X..X
X.X.XJ.X
X...GG.X
XXX.XXXX
XMJ.XXXX
X...XXXX
XXXXXXXX
"""

map5 = """\
XXXXXXXXXXX
XG.....XM.X
X..J...JJ.X
XXXXX.XX..X
XXXXXJXGGGX
XXXXX...GJX
XXXXXXX...X
XXXXXXXXXXX
"""


map_jewels_1 = """\
XXXXXXXXXXXX
XX...X.....X
XX...X.G...X
XX.J..X..XXX
X......MXXXX
X...X...XXXX
XXXXXXXXXXXX"""

map_jewels_2 = """\
XXXXXXXXXXXX
XX...X.....X
XX...X.G...X
XXJJ..X.GXXX
X......MXXXX
X...X...XXXX
XXXXXXXXXXXX"""

map_jewels_3 = """\
XXXXXXXXXXXX
XX...X.....X
XX...X.GG..X
XXJJJ.X.GXXX
X......MXXXX
X...X...XXXX
XXXXXXXXXXXX"""

map_jewels_4 = map1

map_jewels_5 = """\
XXXXXXXXXXXX
XXG..X.....X
XX...X.GGJ.X
XXJJJ.XGGXXX
X.J....MXXXX
X...X...XXXX
XXXXXXXXXXXX
"""

map_jewels_6 = """\
XXXXXXXXXXXX
X....X..G..X
XXJ..X.....X
XX...X.GGJ.X
XXJJJ.XGGXXX
X.J...MGXXXX
X...X...XXXX
XXXXXXXXXXXX
"""
init(map_jewels_5)
if __name__ == '__main__':
    mem_usage = memory_usage( (solve, (dynamicdata, staticdata, playerx, playery,),{'bfs' : True}) )
    max_mem = max(mem_usage)
    start_time = time.time()
    solution = solve(dynamicdata, staticdata, playerx, playery)
    elapsed_time = time.time() - start_time
    solutionLength = len(solution)
    print(solution)
    print('Maximum memory usage: %s [MiB], execution time: %s [s], solution length: %s [actions]' % (max_mem, elapsed_time,solutionLength))

if __name__ == '__main__':
    mem_usage = memory_usage((solve, (dynamicdata, staticdata, playerx, playery,),{'bfs' : True}), interval=.01)
    plt.plot(np.arange(len(mem_usage)) * .01, mem_usage, label='BFS')
    plt.xlabel('Time [s]')
    plt.ylabel('Memory usage [MiB]')
    plt.show()


if __name__ == '__main__':
    memory = list()
    times = list()
    solutionsLengths = list()
    for i in range(10):
        mem_usage = memory_usage( (solve, (dynamicdata, staticdata, playerx, playery,),{'bfs' : False}) )   # Switch BFS to true/false depending on BFS or DFS
        max_mem = max(mem_usage)

        start_time = time.time()
        solution = solve(dynamicdata, staticdata, playerx, playery)
        elapsed_time = time.time() - start_time
        solutionLength = len(solution)
        times.append(elapsed_time)
        memory.append(max_mem)
        
        solutionsLengths.append(solutionLength)
        print('Iteration: %s, maximum memory usage: %s [MiB], execution time: %s [s], solution length: %s [actions]' % (i, max_mem, elapsed_time,solutionLength))
    mem_mean = statistics.mean(memory)
    mem_std = statistics.stdev(memory)
    time_mean = statistics.mean(times)
    time_std = statistics.stdev(times)
    solution_mean = statistics.mean(solutionsLengths)
    solution_std = statistics.stdev(solutionsLengths)
    print('(MEMORY) Mean: %s [MiB], Standard deviation: %s [MiB]' % (mem_mean, mem_std))
    print('(TIME) Mean: %s [s], Standard deviation: %s [s]' % (time_mean, time_std))
    print('(SOLUTION LENGTH) Mean: %s [actions], Standard deviation: %s [actions]' % (solution_mean, solution_std))