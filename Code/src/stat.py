from numpy import array, sqrt, sum, var, mean, std
from matplotlib import pyplot as plt

def get_mse(X, Y, f):
    pred = (map(lambda x: x[0,0],(map(f,X))))
    act = Y
    return mse(act,pred)

def mse(act, pred):
    a = array(act)
    p = array(pred)
    sq_er = (a-p)**2
    boxplot(sq_er)
    show()
    s_mean = mean(sq_er)
    s_var = std(sq_er)
    n = sqrt(len(act))
    z = 2.0
    conf_int = [sqrt(s_mean-z*s_var/n), sqrt(s_mean+z*s_var/n)]
    return sqrt(s_mean), conf_int


def mae(act, pred, bl, cl):
    a = array(act)
    p = array(pred)
    b = bl
    c = cl
    plt.figure()
    plt.hold = True
    er_p = abs(a-p)
    er_b = abs(a-b)
    er_c = abs(a-c)
    means = [mean(er_b),mean(er_p),mean(er_c)]
    z =2.0
    plt.boxplot([er_p,er_b,er_c],vert=0,bootstrap=10000)#,usermedians=means)
    plt.show()

