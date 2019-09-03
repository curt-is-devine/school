from math import sqrt

#Reading of the file
text = open("Auto.txt", "r")
delta = []
titles = text.readline().split()
for line in text:
    splitline = line.split()
    nums = splitline[1:9]
    delta += [nums + [" ".join(splitline[9:])]]
m = len(delta)

#Set up X and Y matrices
Y = [[float(entry[0])] for entry in delta]
X = [entry[1:len(entry)-1] for entry in delta]
for x in range(len(X)):
    for item in range(len(X[0])):
        X[x][item] = float(X[x][item])

#Helper functions
def h(sigma, x, means, var):
    return sigma[0] + (sigma[1] * (x[0] - means[0])/var[0]) + (sigma[2] * (x[1] - means[1])/var[1]) + (sigma[3] * (x[2] - means[2])/var[2]) + (sigma[4] * (x[3] - means[3])/var[3]) + (sigma[5] * (x[4] - means[4])/var[4]) + (sigma[6] * (x[5] - means[5])/var[5]) + (sigma[7] * (x[6] - means[6])/var[6])

def transpose(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]

def matrixMultiply(m1, m2):
    result = [[0 for i in range(len(m2[0]))] for i in range(len(m1))]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    return result



#means of x
xs = [0 for i in range(0, 7)]
for i in range(len(X)):
    for j in range(len(X[0])):
        xs[j] += X[i][j]
for i in range(len(xs)):
    xs[i] = xs[i]/m

#variations and standard deviations of x
var = [0 for i in range(0, 7)]
for x in X:
    for i in range(len(X[0])):
        var[i] += (x[i] - xs[i]) * (x[i] - xs[i])        
sd = [0 for i in range(0, 7)]
for i in range(len(var)):
    sd[i] = sqrt(1/m * var[i])

#initiailizaiton of sigma, alpha, and iteration limit
sigmas = [0 for i in range(0, 8)]

#Change this for alpha values
alpha = 0.1

#Change this for iterations
it = 1000

#Linear regression
while it > 0:
    sigmas[0] = sigmas[0] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * 1 for i in range(len(X))])
    sigmas[1] = sigmas[1] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][0] - xs[0])/sd[0] for i in range(len(X))])
    sigmas[2] = sigmas[2] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][1] - xs[1])/sd[1] for i in range(len(X))])
    sigmas[3] = sigmas[3] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][2] - xs[2])/sd[2] for i in range(len(X))])
    sigmas[4] = sigmas[4] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][3] - xs[3])/sd[3] for i in range(len(X))])
    sigmas[5] = sigmas[5] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][4] - xs[4])/sd[4] for i in range(len(X))])
    sigmas[6] = sigmas[6] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][5] - xs[5])/sd[5] for i in range(len(X))])
    sigmas[7] = sigmas[7] - alpha * 1 / m * sum([(h(sigmas, X[i], xs, sd) - Y[i][0]) * (X[i][6] - xs[6])/sd[6] for i in range(len(X))])
    it -= 1
    #print(1/(2 * m) * sum([(h(sigmas, X[i], xs, sd) - Y[i]) * (h(sigmas, X[i], xs, sd) - Y[i]) for i in range(len(X))]))
print(sigmas)
#1.1    
#sigma0 = 23.444906177804324
#sigma1 = -0.5122038537837849
#sigma2 = -0.2301090012233633    
#sigma3 = -1.1449353633061334
#sigma4 = -3.3956345217693724
#sigma5 = -0.2961819264998824
#sigma6 = 2.6253695465418954
#sigma7 = 1.0486809842880997
#The "year" coefficient (sigma6) indicates that miles per gallon increases with
#respect to the manufacturing date of a car

#1.2
#print(h(sigmas, [4, 300, 200, 3500, 11, 70, 2], xs, sd))
#y = 15.491747535998638 mpg

#1.3
#alpha = 3: The plot of J with each iteration increases linearly,
#never converging or settling on a value
#alpha = 0.3: The plot of J exponentially decays to a value near 5.45
#By the 100th iteration, the function is only changing in value by about
#0.001 every time
#alpha = 0.03: The plot of J seems to be exponentially decreasing, and
#would still continue decreasing if more iterations were kept, only
#reaching a value of ~6.5 when the final value should be near 5.45 as
#stated above
#alpha = 0.00003: The plot of J with each iteration dfecreases linearly and
#clearly does not approach convergence, only reaching a value of
#about 302.98, when the final value should be about 5.45

#1.4
#the coefficients should be roughly those above, but they come out too be:
#sigma0 = -17.124859315932905
#sigma1 = -0.4929052764876453
#sigma2 = 0.019840347573539408    
#sigma3 = -0.017196705194711746
#sigma4 = -0.006464086502996192
#sigma5 = 0.07773300470896846
#sigma6 = 0.7501885228877201
#sigma7 = 1.4256544690306252

X = [[1] + x for x in X]
XT = transpose(X)
firstHalf = matrixMultiply(XT, X)
#used an online calculator to calculate the inverse of this matrix since
#I cannot get numpy to work (http://matrix.reshish.com/inverCalculation.php)
inverse = [[1.9356249872578186, -0.02407892959814684, 0.00023109625297927544, -0.0025249965796906577, 0.00004869637509124875, -0.01775151834707004, -0.018833270857235542, -0.013091097906105821], \
           [-0.024078929598144012, 0.009441496016177756, -0.00014569213168822765, 0.0000494160299852028, -0.0000024222328650031606, 0.0001461120448216095, 0.00002345757061624168, -0.0008013192873514051], \
           [0.00023109625297921643, -0.00014569213168822502, 0.0000051016882203761544, -0.000002754051932853482, -0.0000001705492342293565, 0.000006796788751535896, 0.000002235780433997082, 0.000059838236703856153], \
           [-0.002524996579690565, 0.00004941602998520117, -0.0000027540519328535285, 0.000017100861638066308, -0.00000036700414325947746, 0.00007540331770112513, 0.000013851852496362254, -0.00008119457322232253], \
           [0.00004869637509124445, -0.000002422232865003321, -0.00000017054923422935116, -0.000000367004143259481, 0.00000003834426644499308, -0.000002783366365653566, -0.0000004914723983660506, 0.000001572825676775834], \
           [-0.0177515183470703, 0.0001461120448216103, 0.000006796788751535593, 0.00007540331770112591, -0.0000027833663656535716, 0.0008767712981603785, 0.000032279777823486643, -0.000023686941565099993], \
           [-0.018833270857235455, 0.000023457570616279443, 0.0000022357804339964223, 0.00001385185249636315, -0.0000004914723983661063, 0.00003227977782348291, 0.0002343487313034542, -0.000013203907103164643], \
           [-0.01309109790610784, -0.0008013192873513584, 0.00005983823670385597, -0.00008119457322231932, 0.0000015728256767757017, -0.000023686941565078882, -0.000013203907103144594, 0.006985682318296632]]
firstThreeQuarters = matrixMultiply(inverse, XT)
solution = matrixMultiply(firstThreeQuarters, Y)
print(solution)
