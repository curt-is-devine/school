floorPlan = {'U' : ['L', 'C'], 'C' : ['U', 'I'], 'L' : ['U', 'D'], 'I' : ['C'], 'D' : ['L', 'K', 'F'], 'F' : ['D', 'E'], 'K' : ['D', 'G'], 'E' : ['F'], 'G' : ['K', 'H', 'J'], 'J' : ['G', 'B'], 'H' : ['G', 'B'], 'B' : ['J', 'H', 'A'], 'A' : ['B']}

#Problem 3.f, assuming that the robot starts in some roomo adjacent to U
#and does not re-scan already visited rooms i.e. it has some internal
#map to keep track of where it is in the floor plan
def DFS(adjList):
    visited = ['U']
    toVisit = list(adjList.keys())
    toVisit.remove('U')
    stack = adjList['U']
    while toVisit != []:
        print(stack)
        top = stack[-1]
        if top in toVisit:
            toVisit.remove(top)
            stack.pop()
            stack = stack + adjList[top]
            visited = visited + [top]
        elif top not in toVisit:
            stack.pop()
    scanned = " -> ".join(visited)
    print("Scanned rooms: " + scanned)



#Problem 3.g, assuming the robot starts in some room adjacent to U
#and does not have to account for travel on how it got there
def DFScost(adjList):
    visited = ['U']
    toVisit = list(adjList.keys())
    toVisit.remove('U')
    stack = adjList['U']
    cost = 0
    while (toVisit != []): #or stack != []):
        print(stack)
        top = stack[-1]
        if top in toVisit:
            toVisit.remove(top)
            stack.pop()
            stack = stack + adjList[top]
            visited = visited + [top]
            cost += 6
        elif top not in toVisit:
            if top == 'U':
                cost += 5
            else:
                cost += 2
            stack.pop()
    scanned = " -> ".join(visited)
    print("Scanned rooms: " + scanned)
    print()
    print(str(cost) + " minutes of use. " + '{0:.0%}'.format(1 - float(cost % 45)/45) + " of battery " + str(int(cost/45 + 1)) + " left charged.")

#Problem 3.h. Honestly, I have no idea how to accomplish this without risking
#entering an infinite loop    
def DFScostU(adjList):
    visited = ['U']
    toVisit = list(adjList.keys())
    toVisit.remove('U')
    stack = adjList['U']
    cost = 0
    while (toVisit != [] or stack != []):
        print(stack)
        top = stack[-1]
        if top in toVisit:
            toVisit.remove(top)
            stack.pop()
            stack = stack + adjList[top]
            visited = visited + [top]
            cost += 6
        elif top not in toVisit:
            if top == 'U':
                cost += 5
            else:
                cost += 2
    scanned = " -> ".join(visited)
    print("Scanned rooms: " + scanned)
    print()
    print(str(cost) + " minutes of use. " + '{0:.0%}'.format(1 - float(cost % 45)/45) + " of battery " + str(int(cost/45 + 1)) + " left charged.")

DFScostU(floorPlan)
#DFS(floorPlan) 
        
