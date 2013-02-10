from numpy import array, sqrt, sum

def mse(X, Y, f):
    pred = (map(lambda x: x[0,0],(map(f,X))))
    act = array(Y)
    return sqrt(sum((act-pred)**2)/len(act))
