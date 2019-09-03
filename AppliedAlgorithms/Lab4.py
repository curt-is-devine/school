import random

def generateRandomNumbers(ls, n):
    for i in range(n):
        ls[i] = random.random()
        
def quickSort(A, low, high):
    
    #Base case: the list is either a singleton, in which case, return. Or the list is two elements long
    #in which case, partitioning is too much overhead and we can sort quickly    
    if high - low <= 1:
        return
    elif high - low == 2:
        if A[high - 1] < A[low]:
            swap(A, high - 1, low)
        return
    
    index = random.randint(low, high - 1)
    swap(A, low, index)
    
    p = partition(A, low, high)
    quickSort(A, low, p)
    quickSort(A, p+1, high)
    
def partition(A, low, high):
    i = low + 1
    j = high - 1
    pivot = A[low]
    
    if (i > j):
        return j
    if (i == j):
        if A[i] >= A[j]:
            swap(A, i, j)
            return j
    
    while (i < j):
        while(i < j and A[i] <= pivot):
            i += 1
        while(i <= j and A[j] >= pivot):
            j -= 1
        #Need to check if i is less than j because of tie situations, in the case that it isnt, then
        #we havent iterated through the whole list, And the current indices are both larger and smaller
        #Than the pivot respectively
        if (i < j):
            swap(A, i, j)
            
    #We have to change with j here because we will always reach the case where j < i in order to break
    #Out of the loop. Thus, we need to swap with the smaller element (j) in order to keep our sorting
    #correct. Swapping the larger index could result in some mixed in larger numbers
    swap(A, low, j)
    return j
    
def swap(A, i, j):
    temp = A[i]
    A[i] = A[j]
    A[j] = temp
    
   
inFile = open("lab4_test_sorting.txt")
nums = inFile.read().split("\n")[1:]
inFile.close()

nums = [int(nums[i]) for i in range(len(nums) - 1)]
quickSort(nums, 0, len(nums))

outFile = open("outlarge.txt", "w")
outFile.write(str(nums))
outFile.close()