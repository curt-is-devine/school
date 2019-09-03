import random

class treeNode:
    def __init__(self):
        self.parent = None
        self.lc = None
        self.rc = None
        self.data = None
        self.height = 0
        self.priority = random.random()

class Treap:
    def __init__(self):   
        self.root = treeNode()     
        self.size = 0
    
    #Need to adjust heights
    #assuming size is supposed to be number of nodes
    def insert(self, val):
        if self.size == 0:
            self.root.data = val
            self.size = 1
            return
        curr = self.root
        while curr is not None:
            if curr.data >= val:
                if curr.lc is None:
                    self.addLeaf(curr, "lc", val)
                    break
                else:
                    curr = curr.lc
            else:
                if curr.rc is None:
                    self.addLeaf(curr, "rc", val)
                    break
                else:
                    curr = curr.rc
        return
    
    def addLeaf(self, curr, child, val):
        new = treeNode()
        new.data = val
        new.parent = curr
        if child == "lc":
            curr.lc = new
        else:
            curr.rc = new
        self.size += 1
        self.updateHeight(curr)
        self.siftUp(new)
        
    def siftUp(self, node):
        while (node.parent is not None) and (node.parent.priority < node.priority):
            self.rotate(node)
    
    def rotate(self, node):
        
        if node is None or node is self.root:
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

for j in range(5):
    treap = Treap()
    for i in range(100000):
        treap.insert(i)
    
    print("Root data: "+str(treap.root.data)+", priority: " + str(treap.root.priority) + ", height: " + str(treap.root.height))
    if treap.root.lc is not None:
        print("Root left child data: "+str(treap.root.lc.data)+", priority: " + str(treap.root.lc.priority) + ", height: " + str(treap.root.lc.height))
    if treap.root.rc is not None:
        print("Root right child data: "+str(treap.root.rc.data)+", priority: " + str(treap.root.rc.priority) + ", height: " + str(treap.root.rc.height))
    print()