class treeNode:
    def __init__(self):
        self.parent = None
        self.lc = None
        self.rc = None
        self.value = None
        self.height = 0;

class RBST:
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
                return None
            if curr.value == val:
                return curr
            if curr.value > val:
                curr = curr.lc
            else:
                curr = curr.rc
        return None
    
    #Need to adjust heights
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
                    self.updateHeight(curr)
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
                    self.updateHeight(curr)
                    break
                else:
                    curr = curr.rc
        return
    
    def rotate(self, node):
        
        if node is None or (node.rc is None and node.lc is None):
            return
        
        if node is self.root:
            return
        elif node is node.parent.rc:
            self.rotate_left(node)
        else:
            self.rotate_right(node)
    
    def rotate_left(self, node):
        x = node.parent
        z = node.lc
        xPar = x.parent
        
        if xPar is None:
            self.root = node
        elif xPar.lc is x:
            xPar.lc = node
        else:
            xPar.rc = node
            
        node.parent = xPar
        node.lc = x
        x.parent = node
        x.rc = z
        
        if z is not None:
            z.parent = x
            
        self.updateHeight(x)
        self.updateHeight(node)
        return False
    
    def rotate_right(self, node):
        y = node.parent
        z = node.rc
        yPar = y.parent
        
        if yPar is None:
            self.root = node
        elif yPar.lc is y:
            yPar.lc = node
        else:
            yPar.rc = node
            
        node.parent = yPar
        node.rc = y
        y.parent = node
        y.lc = z
        
        if z is not None:
            z.parent = y
            
        self.updateHeight(y)
        self.updateHeight(node)
    
    def updateHeight(self, node):
        if node is None:
            return
        
        oldHeight = node.height
        leftHeight = 0
        if node.lc is None:
            leftHeight = -1
        else:
            leftHeight = node.lc.height
        rightHeight = 0
        if node.rc is None:
            rightHeight = -1
        else:
            rightHeight = node.rc.height
            
        newHeight = 1 + max(leftHeight, rightHeight)
        if (oldHeight == newHeight):
            return
        node.height = newHeight
        self.updateHeight(node.parent)
        return True

#This needs changed for the right file
inFile = open("lab7_test_RBST.txt")
A = inFile.read().split("\n")[2:]
inFile.close()

A = [int(A[i]) for i in range(len(A) - 1)]
rBinTree = RBST()
for i in A:
    rBinTree.insert(i)
    
sNr = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 1000]
for e in sNr:
    rBinTree.rotate(rBinTree.search(e))

print("Inorder Traversal: ")
rBinTree.inOrder(rBinTree.root)

print("Root value: " + str(rBinTree.root.value))
print("Root height: " + str(rBinTree.root.height))