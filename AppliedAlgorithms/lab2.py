import time

def minIndex(A, begin, end):
    #reduce search space to either the specified end or the length of the list
    l = min(end, len(A))
    #If the min above is 0 or begin is further than it, fail
    if l == 0 or begin > l:
        return False
    #The minimum value has to be at least at the beginning of the search space
    m = begin
    for i in range(begin + 1, l):
        if int(A[i]) < int(A[m]):
            #Store the index, not the actual value of the minimum so far
            m = i
    return m

def swap(A, i, j):
    if i < 0 or j < 0 or j > len(A) - 1 or i > len(A) - 1:
        return False
    temp = A[i]
    A[i] = A[j]
    A[j] = temp
    return True

def selectionSort(A):
    n = len(A)
    if n == 0:
        return True
    for i in range(0, n):
        mIndex = minIndex(A, i, n)
        swap(A, i, mIndex)
    return True
    
def unknown(a):
    n = len(a)-1
    for j in range(0, n - 1):
        if a[n] < a[j]:
            swap(a, j, n)
            print(a)

def insertionSort(A):
    n = len(A)
    if n == 0:
        return True
    for i in range(0, n):
        j = i
        while j > 0 and int(A[j - 1]) > int(A[j]):
            swap(A, j-1, j)
            j -= 1
        
inFile = open("lab2_test_sorting.txt")
selectA = inFile.read().split("\n")[1:]
inFile.close()

selectA = selectA[:len(selectA) - 1]
insertA = selectA.copy()

selectionSort(selectA)
insertionSort(insertA)

outFile = open("out.txt", "w")
outFile.write("SelectionSort output: " + str(selectA) + "\n")
outFile.write("InsertionSort output: " + str(insertA) + "\n")
outFile.write("Are they the same? " + str(selectA == insertA))
outFile.close()

#comparison trial
compare = [i for i in range(0, 10**3)]
start = time.time()
selectionSort(compare)
end = time.time()
print("Selection sort took: " + str(end - start) + "seconds.")
start = time.time()
insertionSort(compare)
end = time.time()
print("Insertion sort took: " + str(end - start) + "seconds.")
