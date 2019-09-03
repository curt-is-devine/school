class BinaryHeap:
    
    def __init__(self, array, n):   
        self.__size = n     
        self.heap = [0] + array
        i = n
        while i > 0:
            self.siftDown(i)
            i -= 1
    def size(self):
        return self.__size
    
    def siftDown(self, i):
        if (i > self.size()):
            return
        left = 2 * i
        right = 2 * i + 1
        if right <= self.size(): #If the right child is still in the heap, we can compare both left and right children
            maxChild = max(self.heap[right], self.heap[left]) #for ease of reading
            if maxChild > self.heap[i] and maxChild == self.heap[right]: #If the max child is greater than the node and the right child equals the max, swap them
                self.swap(i, right)    
                self.siftDown(right)
            elif maxChild > self.heap[i]: #If the max child is greater than the node, but not the right, it has to be the left child
                self.swap(i, left)
                self.siftDown(left)
            else: #the max child is less than the current node, so stop
                return
        elif left <= self.size(): #If there is no right child, but a left, we can just compare them
            if self.heap[left] > self.heap[i]:
                self.swap(i, left)
                return #Dont need to recur since the left child would HAVE to be the final element by our design
        else: #there are no valid children:
            return
            
        
    def delMax(self):
        res = self.heap[1]
        self.swap(1, self.size())
        self.__size -= 1
        self.siftDown(1)
        return res
    
    def swap(self, i, j):
        temp = self.heap[i]
        self.heap[i] = self.heap[j]
        self.heap[j] = temp

        
inFile = open("lab5_test_heap.txt")
A = inFile.read().split("\n")[1:]
inFile.close()

A = [int(A[i]) for i in range(len(A) - 1)]
binHeap = BinaryHeap(A, len(A))
print(binHeap.size)

outFile = open("out.txt", "w")
for i in range(20):
    outFile.write(str(binHeap.delMax()) + " ")
outFile.close()        