def minNumber(A, begin, end, n):
    m = float("inf")
    for i in range(begin, end + 1):
        if float(A[i]) < float(m):
            m = A[i]
    return m

inFile = open("lab1_minNumber_test.txt")
a = inFile.read().split("\n")[1:]
inFile.close()

outFile = open("out.txt", "w")
outNums = [minNumber(a, 0, 99, 0), minNumber(a, 100, 399, 0), minNumber(a, 400, 999, 0)]
for num in outNums:
    outFile.write(str(num) + "\n")
outFile.close()