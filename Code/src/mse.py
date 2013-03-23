from numpy import (linalg, column_stack, array, sqrt, sum, var, mean, std, arange, ones,
polyfit,log, vstack)
from matplotlib import pyplot as plt
import plot

def get_mse(tX,tY,X, Y, f):
    pred = (map(lambda x: x[0,0],(map(f,X))))
    act = Y
    x = array([i[0] for i in tX])
    y = array([i[1] for i in tX])
    M = column_stack((ones(len(x)),x**3,y))
    c, re, rk, sg = linalg.lstsq(M,tY)
    cl = [c[2]*i[1]+c[1]*i[0]+c[0] for i in X]
    bl = mean(Y)
    return mae(act,pred,bl,cl)

def mse(X, Y, f):
    pred = (map(lambda x: x[0,0],(map(f,X))))
    act = array(Y)
    return sum((act-pred)**2)/len(act)

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
    means =  array([mean(i) for i in errors])
    errorbars = ([z*std(er)/n for er in errors])
    print means
    print errorbars
    log_bars=vstack((log(means+errorbars)-log(means),log(means)-log(means-errorbars)))
    print log_bars
    #plt.errorbar(log(means),arange(1,4),xerr=log_bars,fmt='x')
    plt.errorbar(means,arange(1,4),xerr=errorbars,fmt='x')
    plt.title('Performance of SVM with a Non-Linear Score Function')
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
