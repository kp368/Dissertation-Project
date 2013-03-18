from numpy import array, sqrt, sum, var, mean, std

def get_mse(X, Y, f):
    pred = (map(lambda x: x[0,0],(map(f,X))))
    act = Y
    return mse(act,pred)

def mse(act, pred):
    a = array(act)
    p = array(pred)
    sq_er = (a-p)**2
    s_mean = mean(sq_er)
    s_var = std(sq_er)
    n = sqrt(len(act))
    z = 2.0
    conf_int = [sqrt(s_mean-z*s_var/n), sqrt(s_mean+z*s_var/n)]
    return sqrt(s_mean), conf_int
