from numpy import array, sqrt, sum, var, mean, std, arange, ones
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
    z = 2.0
    n = sqrt(len(act))
    a = array(act)
    p = array(pred)
    b = array(bl)
    c = array(cl)
    plt.figure()
    plt.hold = True
    errors = [(a-b)**2,(a-p)**2,(a-c)**2]
    means = [mean(i) for i in errors]
    errorbars = [z*std(er)/n for er in errors]
    print means
    print errorbars
    plt.errorbar(means,arange(1,4),xerr=errorbars,fmt='x')
    plt.title('Performance of Naive Bayes on Linearly Separable Data')
    #plt.title('Performance of Naive Bayes on Linearly Inseparable Data')
    plt.xlabel('Squared Error in Score')
    #plt.errorbar([er_b,er_p,er_c],[1,2,3],xerr=0.2)
    #plt.boxplot([er_b,er_p,er_c],sym='',vert=0,whis=0,bootstrap=None,usermedians=means,conf_intervals=[int_b,int_p,int_c],widths=0.3)
    plt.yticks([0,1,2,3,4], ('','Baseline','Actual', 'Ceiling',''))
    #plt.xticks(arange(100,1000,100))
    params = {'font.size': 16}
    plt.rcParams.update(params)
    plt.show()


def plot_quant():
    x = arange(2,6)
    
    y = [mean(er) for er in errors]
    ints = [z*std(i)/n for i in errors]
    plt.figure()

    plt.errorbar(x, y, yerr=errors,fmt='o')
