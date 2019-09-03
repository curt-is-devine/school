class PriorityQueue:
    def __init__(self):
        self.queue = []
        
    def isEmpty(self):
        return len(self.queue) == 0
    
    def push(self, tup):
        if len(self.queue) == 0:
            self.queue = [tup]
            return
        for i in range(len(self.queue)):
            if self.queue[i][1] > tup[1]:
                self.queue = self.queue[:i] + [tup] + self.queue[i:]
                return
        self.queue = self.queue + [tup]
        
    def pop(self):
        if len(self.queue) >= 1:
            temp = self.queue[0]
            self.queue = self.queue[1:]
            return temp
        else:
            return False 
        

class GraphNode:      
    def __init__(self, iden):
        self.id = iden
        self.visited = False
        self.neighbors = []
        self.distance = 0
 
    def add_neighbor(self, node_id, weight):
        self.neighbors = self.neighbors + [(node_id, weight)]
    def get_neighbors(self):
        return self.neighbors

def build_graph():
    graph = [i for i in range(50)]
    for elem in graph:
        graph[elem] = GraphNode(elem)
    
    inFile = open("lab11_test_dijkstra.txt")
    A = inFile.read().split("\n")
    inFile.close()
    A = A[:len(A) - 1]
    
    for line in A:
        (node1, node2, weight) = line.split()
        graph[int(node1)].add_neighbor(int(node2), int(weight))
    
    return graph

def dijkstra(graph, s, t):
    if s == t:
        return 0
    
    for elem in graph:
        elem.visited = False
        elem.distance = 1000000000
        
    graph[s].distance = 0
    
    q = PriorityQueue()
    q.push((s, 0))
        
    while not q.isEmpty():
        temp = q.pop()
        if temp == False:
            continue
        (node_id, node_weight) = temp
        
        while not q.isEmpty() and (graph[node_id].visited == True) :
            (node_id, node_weight) = q.pop()
        
        if node_id == t:
            return graph[t].distance
        
        graph[node_id].visited = True
        
        for (nb_node_id, weight) in graph[node_id].neighbors:
            if (graph[nb_node_id].visited == False) and (graph[node_id].distance + weight < graph[nb_node_id].distance):
                    graph[nb_node_id].distance = graph[node_id].distance + weight
                    q.push((nb_node_id, graph[nb_node_id].distance))
                    
    
    return graph[t].distance

graph = build_graph()
for i in range(50):
    print("Distance between node 30 and node " + str(i) + " is " + str(dijkstra(graph, 30, i)))