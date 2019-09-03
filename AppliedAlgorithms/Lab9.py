def lcs(a, b):
    n = len(a)
    m = len(b)
    opt = [[0 for i in range(m + 1)] for i in range(n + 1)] #Columns = b, rows = a
    
    #Fill the Matrix
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i-1] == b[j-1]:
                match = opt[i-1][j-1] + 1
            else:
                match = opt[i-1][j - 1]
            i_miss = opt[i-1][j]
            j_miss = opt[i][j-1]
            opt[i][j] = max([match, i_miss, j_miss])
            
    s = ''
    i = n
    j = m 
    while (i > 0 and j > 0):
        if (opt[i][j] == (opt[i-1][j-1] + 1)) and a[i-1] == b[j-1]:
            i-=1
            j-=1
            s += a[i]
        elif opt[i][j] == opt[i-1][j]:
            i-=1
        else:
            j-=1   
            
    return (opt[n][m], s[::-1])

f = open("lab9_test_lcs.txt")
txt = f.readlines()
(l, res) = lcs(txt[0],txt[1])
print("Length: " + str(l) + ", Result: " + res)