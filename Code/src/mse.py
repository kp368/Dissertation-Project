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
    #er_p = abs(a-p)
    #er_b = abs(a-b)
    #er_c = abs(a-c)
    er_p = (a-p)**2
    er_b = (a-b)**2
    er_c = (a-c)**2
    #means = [sqrt(mean(er_b)),sqrt(mean(er_p)),sqrt(mean(er_c))]
    means = [mean(er_b),mean(er_p),mean(er_c)]
    int_p = (means[1]-z*std(er_p)/n, means[1]+z*std(er_p)/n)
    int_b = (means[0]-z*std(er_b)/n, means[0]+z*std(er_b)/n)
    int_c = (means[2]-z*std(er_c)/n, means[2]+z*std(er_c)/n)
    intervals=[int_b,int_p,int_c]
    #errors = [sqrt(z*std(er_b)/n),sqrt(z*std(er_p)/n),sqrt(z*std(er_c)/n)]
    errors = [z*std(er_b)/n,z*std(er_p)/n,z*std(er_c)/n]
    print means
    print errors
    plt.errorbar(means,arange(1,4),xerr=errors,fmt='x')
    plt.title('Performance of Naive Bayes on Linearly Separable Data')
    #plt.title('Performance of Naive Bayes on Linearly Inseparable Data')
    plt.xlabel('Squared Error in Score')
    #plt.errorbar([er_b,er_p,er_c],[1,2,3],xerr=0.2)
    #plt.boxplot([er_b,er_p,er_c],sym='',vert=0,whis=0,bootstrap=None,usermedians=means,conf_intervals=[int_b,int_p,int_c],widths=0.3)
    plt.yticks([0,1,2,3,4], ('','Baseline','Actual', 'Ceiling',''))
    plt.xticks(arange(100,1000,100))
    params = {'font.size': 16}
    plt.rcParams.update(params)
    plt.show()


