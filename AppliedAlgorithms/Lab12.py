parent = [i for i in range(500)]
size = [1 for i in range(500)]
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
            if self.queue[i][2] > tup[2]:
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

def build_queue():
    q = PriorityQueue()
    
    inFile = open("lab12_test_mst.txt")
    A = inFile.read().split("\n")
    inFile.close()
    A = A[:len(A) - 1]
    
    for line in A:
        (node1, node2, weight) = line.split()
        q.push((int(node1), int(node2), int(weight)))
    
    return q

def find(node_id):
    if parent[node_id] != node_id:
        parent[node_id] = find(parent[node_id])
    return parent[node_id]
    
def union(u, v):
    paru = find(u)
    parv = find(v)
    if paru != parv:
        if size[paru] >= size[parv]:
            parent[parv] = paru
        else:
            parent[paru] = parv
        if size[paru] == size[parv]:
            size[paru] += 1


edges = build_queue()
mst_weight = 0
for e in edges.queue:
    node1 = e[0]
    node2 = e[1]
    if find(node1) != find(node2):
        union(node1, node2)
        mst_weight = mst_weight + e[2]
print("The total weight for the MST is " + str(mst_weight))
