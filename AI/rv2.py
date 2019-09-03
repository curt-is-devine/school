bluePrints = open("f.txt", "r")
floorScan = []
for length in bluePrints:
    floorScan += length.split()

location = [1]
i = 0
while i < len(floorScan[len(floorScan) - 1]):
    if floorScan[len(floorScan) - 1][i] == '0':
        location = [i + 1, 1]
    i += 1
for line in floorScan:
    print(line)
    
i = len(floorScan) - 1
newFloorPlan = []
while i >= 0:
    newFloorPlan.append(floorScan[i])
    i -= 1

def findExits(floorPlan):
    i = 0
    exits = []
    while i < len(floorPlan):
        if floorPlan[i][0] == '0':
            exits.append([1, i + 1])
        if floorPlan[len(floorPlan) - 1][i] == '0':
            exits.append([i + 1, len(floorPlan)])
        i += 1
    for line in floorPlan:
        if line[len(line) - 1] == '0':
            exits.append([floorPlan.get(line), len(line)])
    return exits

def findHeuristic(location, exits):
    distances = []
    for ex in exits:
        dist = abs(int(ex[0]) - location[0]) + abs(int(ex[1]) - location[1])
        distances.append(dist)
    return min(distances)

def move(position, direction, newFloorPlan):
    newPosition = []
    if direction == 'n':
        newPosition = [position[0], position[1] + 1]
    elif direction == 'e':
        newPosition = [position[0] + 1, position[1]]
    elif direction == 's':
        newPosition = [position[0], position[1] - 1]
    else:
        newPosition = [position[0] - 1, position[1]]
    if newFloorPlan[newPosition[1] - 1][newPosition[0] - 1] == '1':
        return False
    return newPosition

def successors(position, newFloorPlan, dirtyRooms):
    pose = [position[0] + 1, position[1]]
    posn = [position[0], position[1] + 1]
    poss = [position[0], position[1] - 1]
    posw = [position[0] - 1, position[1]]
    successors = []
    if newFloorPlan[pose[1] - 1][pose[0] - 1] != '1' and pose not in dirtyRooms:
        successors.append(pose)
    if newFloorPlan[posn[1] - 1][posn[0] - 1] != '1' and posn not in dirtyRooms:
        successors.append(posn)
    if newFloorPlan[poss[1] - 1][poss[0] - 1] != '1' and poss not in dirtyRooms:
        successors.append(poss)
    if newFloorPlan[posw[1] - 1][posw[0] - 1] != '1' and posw not in dirtyRooms:
        successors.append(posw)
    return successors
    
def rotate(direction):
    if direction == 'n':
        return 'e'
    if direction == 'e':
        return 's'
    if direction == 's':
        return 'w'
    else:
        return 'n'

outs = findExits(newFloorPlan)
if len(location) == 1:
    print("Invalid floor plan. R cannot enter form the south")
    print(False)
else:
    doit = False
    path = [[location], 1]
    visited = [location]
    memory = []
    while True:
        if path[1] == 0:
            doit = True
            break
        succs = successors(location, newFloorPlan, visited)
        locations = path[0]
        for succ in succs:
            locations.append(succ)
            memory += [[locations, findHeuristic(succ, outs)]]
            locations = locations[:len(locations)-1]
            visited.append(succ)
        if memory == []:
            print(False)
            break
        mn = memory[0][-1]
        for item in memory:
            if item[-1] < mn:
                mn = item[-1]
        for route in memory:
            if route[-1] == mn:
                path = route
        memory.remove(path)
        location = path[0][-1]

if doit == True:
    i = 0
    schematic = ['n']
    direction = 'n'
    while i < len(path[0]) - 1:
        schematic.append(path[0][i])
        if move(path[0][i], direction, newFloorPlan) == path[0][i + 1]:
            i += 1
            continue
        while move(path[0][i], direction, newFloorPlan) != path[0][i + 1]:
            direction = rotate(direction)
        schematic.append(direction)
        i += 1
    print(schematic)
        
