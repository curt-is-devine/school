class treeNode:
    def __init__(self):
        self.parent = None
        self.lc = None
        self.rc = None
        self.value = None

class BST:
    def __init__(self):   
        self.root = treeNode()     
        self.size = 0
    
    def inOrder(self, node):
        if node is None:
            return
        print(self.inOrderHelper(node))
        
    def inOrderHelper(self, node):
        if node is None:
            return []
        trav = []
        trav = trav + self.inOrderHelper(node.lc)
        trav = trav + [node.value]
        trav = trav + self.inOrderHelper(node.rc)
        return trav
        
    def search(self, val):
        curr = self.root
        while True:
            if curr is None:
                return False
            if curr.value == val:
                return True
            if curr.value > val:
                curr = curr.lc
            else:
                curr = curr.rc
        return False
    
    #assuming size is supposed to be number of nodes
    def insert(self, val):
        if self.size == 0:
            self.root.value = val
            self.size = 1
            return
        curr = self.root
        while curr is not None:
            if curr.value >= val:
                if curr.lc is None:
                    new = treeNode()
                    new.value = val
                    new.parent = curr
                    curr.lc = new
                    self.size += 1
                    break
                else:
                    curr = curr.lc
            else:
                if curr.rc is None:
                    new = treeNode()
                    new.value = val
                    new.parent = curr
                    curr.rc = new
                    self.size += 1
                    break
                else:
                    curr = curr.rc
        return

#This needs changed for the right file
inFile = open("lab6_test_BST.txt")
A = inFile.read().split("\n")[1:]
inFile.close()

A = [int(A[i]) for i in range(len(A) - 1)]
binTree = BST()
for i in A:
    binTree.insert(i)
    
#Search operation
missing = []
for i in range(1, 101):
    if not binTree.search(i):
        missing.append(i)
print("Missing set of elements in the range of 1 to 100: " + str(missing))

print("Inorder Traversal: ")
binTree.inOrder(binTree.root)