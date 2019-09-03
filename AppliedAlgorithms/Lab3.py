def mergeSort(a, aux, low, high):
    if high - low <= 1:
        return
    mid = (low + high)//2
    mergeSort(a, aux, low, mid)
    mergeSort(a, aux, mid, high)
    merge(a, aux, low, mid, high)
    
def merge(a, aux, low, mid, high):
    for l in range(low, high):
        aux[l] = a[l]
    i = low
    j = mid
    k = low
    while i < mid and j < high:
        if int(aux[i]) <= int(aux[j]):
            a[k] = aux[i]
            k += 1
            i += 1
        else:
            a[k] = aux[j]
            k += 1
            j += 1
    while i < mid:
        a[k] = aux[i]
        k += 1
        i += 1
    while j < high:
        a[k] = aux[j]
        k += 1
        j += 1
        
inFile = open("lab3_test_large.txt")
nums = inFile.read().split("\n")[1:]
inFile.close()

nums = nums[:len(nums) - 1]
mergeSort(nums, [0 for i in range(len(nums))], 0, len(nums))

outFile = open("outlarge.txt", "w")
outFile.write(str(nums))
outFile.close()
