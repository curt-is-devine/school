class GraphNode:      
    def __init__(self, iden):
        self.iden = iden
        self.visited = False
        self.neighbors = []
        self.distance = 0
 
    def add_neighbor(self, node_id):
        self.neighbors = self.neighbors + [node_id]

    def get_neighbors(self):
        return self.neighbors
    
def build_graph():
    graph = [i for i in range(50)]
    for elem in graph:
        graph[elem] = GraphNode(elem)
    
    inFile = open("lab10_test_BFS.txt")
    A = inFile.read().split("\n")
    inFile.close()
    A = A[:len(A) - 1]
    
    for line in A:
        (node1, node2) = line.split()
        graph[int(node1)].add_neighbor(int(node2))
    
    return graph

def bfs(graph, source_id, dest_id):
    if source_id == dest_id:
        return 0
    
    for elem in graph:
        elem.visited = False
        
    graph[source_id].visited = True
    graph[source_id].distance = 0
    
    q = [source_id]
    
    while q != []:
        node = graph[q[0]]
        curr_dist = node.distance
        
        for elem in node.get_neighbors():
            n = graph[elem]
            if n.iden == dest_id:
                return curr_dist + 1
            if not n.visited:
                n.visited = True
                n.distance = curr_dist + 1
                q = q + [n.iden]
                
        if len(q) > 1:
            q = q[1:]
        else:
            break
    
    return -1

graph = build_graph()

source1 = 15
source2 = 23
source3 = 39
dest1 = 38
dest2 = 11
dest3 = 4
print("Distance between " + str(source1) + " and " + str(dest1) + " is " + str(bfs(graph, source1, dest1)))
print("Distance between " + str(source2) + " and " + str(dest2) + " is " + str(bfs(graph, source2, dest2)))
print("Distance between " + str(source3) + " and " + str(dest3) + " is " + str(bfs(graph, source3, dest3)))
#'''