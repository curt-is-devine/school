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

def move(position, direction, newFloorPlan, dirtyRooms):
    newPosition = []
    if direction == 'n':
        newPosition = [position[0], position[1] + 1]
    elif direction == 'e':
        newPosition = [position[0] + 1, position[1]]
    elif direction == 's':
        newPosition = [position[0], position[1] - 1]
    else:
        newPosition = [position[0] - 1, position[1]]
    if newFloorPlan[newPosition[1] - 1][newPosition[0] - 1] == '1' or newPosition in dirtyRooms:
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

def pathStructure(position, newFloorPlan, dirtyRooms):
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
    if len(successors) == 0:
        return "Stuck"
    if len(successors) == 1:
        return 'isDeadEnd'
    if len(successors) == 2:
        return 'isOneWay'
    
if len(location) == 1:
    print("Invalid floor plan. R cannot enter form the south")
else:    
    direction = 'n'
    path = [location, direction]
    visited = [[location]]
    dirtyLocations = [location]
    while True:
        oldLocation = [location[0], location[1]]
        location = move(location, direction, newFloorPlan, dirtyLocations)
        if location != oldLocation:
            visited.append([location]) 
        path.append(location)
        if location[0] == 1 or location[0] == len(newFloorPlan[location[1] - 1]) or location[1] == len(newFloorPlan):
            print(True)
            print(path)
            break
        if move(location, direction, newFloorPlan, dirtyLocations) == False:
            if pathStructure(location, newFloorPlan, dirtyLocations) == 'isDeadEnd':
                dirtyLocations.append(location)
                direction = rotate(rotate(direction))
            elif pathStructure(location, newFloorPlan, dirtyLocations) == 'isOneWay':
                storeDirection = rotate(rotate(direction))
                direction = rotate(direction)
                while move(location, direction, newFloorPlan, dirtyLocations) == False or direction == storeDirection:
                    direction = rotate(direction)
            elif pathStructure(location, newFloorPlan, dirtyLocations) == 'Stuck':
                print(False)
                break
            else:
                for successor in successors(location, newFloorPlan, dirtyLocations):
                    if successor not in visited:
                        while move(location, direction, newFloorPlan, dirtyLocations) != successor:
                            direction = rotate(direction)
            path.append(direction)
                
            

    


