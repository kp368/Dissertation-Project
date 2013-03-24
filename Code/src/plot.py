from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
import csv
from matplotlib import mlab

def bayes():
   # plt.plot([0,1,1.6],[1.6,0.6,0],'r')
    plt.plot([0,1,2],[1,1,1],'r')
    plt.plot([1,1,1],[0,1,2],'r')
    plt.xticks([0,1,2], ('0','M',''))
    plt.yticks([0,1,2], ('0','M',''))
    plt.annotate('Class 2',xy=(1.5,1.5),xytext=(1.5,1.5))
    plt.annotate('Class 1',xy=(1.5,1.5),xytext=(0.5,1.5))
    plt.annotate('Class 1',xy=(1.5,1.5),xytext=(1.5,0.5))
    plt.annotate('Class 2',xy=(1.5,1.5),xytext=(0.5,0.5))
    plt.title('Classification of Linearly Inseparable Data')
    plt.ylabel('Feature 1')
    plt.xlabel('Feature 2')
    params = {'font.size': 16}
    plt.rcParams.update(params)
    plt.show()

from numpy import *

def points(x,y,y_fit):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x,y)
    ax.plot(x,y_fit,color='r')
    plt.show()

def plot_cats(cats):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cols = ['b','r']
    t = [5,41]
    x = arange(0,25,5)
    for i,c in enumerate(cols):
        ax.scatter(cats[i][0],cats[i][1],color=c)
        ax.plot(x,t[i]-x,color=c)
    plt.xlim(xmin=0,xmax=17)
    plt.ylim(ymin=-1,ymax=30)
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.title('Classification into Two Quantized Classes')
    plt.show()

def svm_feats():
    fs = [1,15,21,27]
    fig = plt.figure()
    plt.subplot(211)
    r = mlab.csv2rec('svm_fs.csv',delimiter=' ',names=['b_m','b_l','b_r','m','l','r'])
    p_es = r['m']
    p_yerr = array(zip(r['l'],r['r'])).T
    b_es = r['b_m']
    b_yerr = array(zip(r['b_l'],r['b_r'])).T
    ax1 = fig.add_subplot(211)
    ax1.errorbar(fs,p_es,p_yerr,color='b',label='Actual')
    ax1.errorbar(fs,b_es,b_yerr,color='g',fmt=':',label='Baseline')
    ax2 = fig.add_subplot(212)
    ax2.errorbar(fs,log(p_es),log(p_yerr),color='b',label='Actual')
    ax2.errorbar(fs,log(b_es),log(b_yerr),color='g',fmt=':',label='Baseline')
    #ax2.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    ax2.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15),ncol=2)
    #ax2.legend(bbox_to_anchor=(0., -0.42, 1.0, 0.1), loc=3, borderaxespad=0.,ncol=2,mode='expand')
    #plt.xlim(xmin=1.5,xmax = 16)
    ax2.set_ylim(ymax=35)
    #plt.xticks(arange(2,16))
    #plt.yticks(arange(0,225,25))
    plt.suptitle('SVM Performance with Varying Number of Features')
    ax1.set_ylabel('MSE')
    ax2.set_ylabel('MSE (Log Scale)')
    plt.xlabel('Number of Features')
    plt.show()


def feats():
    fs = [2,3,4,5,6,7,8,12,15]
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.6,0.75])
    c_es = [10,19.9,19.5,42.2,42.6,64.7,45.6,46.7,78.1]
    c_yerr = [2.8,4,3.9,11.5,11.5,14,11.1,10,17.6]
    ax.errorbar(fs,c_es,c_yerr,color='r',fmt='--',label='Ceiling')
    p_es = [18,39.5,41.6,71,64,130.7,124.5,281.2,458]
    p_yerr = [5,5.4,5.9,13.5,12.3,20.8,21.4,37.8,59.6]
    ax.errorbar(fs,p_es,p_yerr,color='b',label='Actual')
    b_es = [133,148,126,279,270,600,533,941,1282.9]
    b_yerr = [22,22,19.4,50,48,81,74,136.4,184.2]
    ax.errorbar(fs,b_es,b_yerr,color='g',fmt=':',label='Baseline')
    ax.plot(fs,exp(fs),'k-.',label='Exponential')
    ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    plt.xlim(xmin=1.5,xmax = 16)
    plt.ylim(ymin=0,ymax=1100)
    plt.xticks(arange(2,16))
    #plt.yticks(arange(0,225,25))
    plt.suptitle('Bayes Performance with Varying Number of Features')
    plt.ylabel('Mean Squared Error')
    plt.xlabel('Number of Features')
    plt.show()

def quants():
    qs = [2,3,4,5,6,7,10,12,15]
    fig = plt.figure()
    ax = fig.add_axes([0.1,0.1,0.6,0.75])
    c_es = [72,24,23,14,11,10,6,2,0]
    c_yerr = [10.6,5.4,4.2,3.6,2.8,2.8,1,0.4,0]
    ax.errorbar(qs,c_es,c_yerr,color='r',fmt='--',label='Ceiling')
    p_es = [90.3,36.5,33.7,22.5,18.1,18.8,10,4,1.5]
    p_yerr = [13.1,7,6.7,4.5,3.8,3.9,2,1.1,0.18]
    ax.errorbar(qs,p_es,p_yerr,color='b',label='Actual')
    b_es = [195,72,94,95,143,154,160,180,170]
    b_yerr = [20.1,15,17.6,17.7,22.3,20.3,20,19,21]
    ax.errorbar(qs,b_es,b_yerr,color='g',fmt=':',label='Baseline')
    ax.legend(bbox_to_anchor=(1.02, 1), loc=2, borderaxespad=0.)
    #plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
    #   ncol=3, mode="expand", borderaxespad=0.)
    plt.suptitle('Bayes Performance with Varying Number of Classes')
    plt.xlim(xmin=1.5,xmax = 16)
    plt.ylim(ymin=0,ymax=225)
    plt.xticks(arange(2,16))
    plt.yticks(arange(0,225,25))
    plt.ylabel('Mean Squared Error')
    plt.xlabel('Number of Classes')
    plt.show()


def label(ax):

    ax.set_xlabel('PageRank')
    ax.set_ylabel('Occurence')
    ax.set_zlabel('Ranking')


def plot(f,train,test):

    fig1, fig2 = plt.figure(1), plt.figure(2)
    ax1, ax2 = fig1.add_subplot(111), fig2.add_subplot(111)
    t = 'Performance Prediction with a Linear Kernel'

    def p(ax,d,title,y_ax='Score'):

        x = np.arange(len(d[0]))
        y_act = d[1]
        y_pred = [f(i)[0,0] for i in d[0] ]
        ax.set_title(title)
        ax.set_xlabel('Page Number')
        ax.set_ylabel(y_ax)
        ax.scatter(x,y_act,s=10,c='b',marker='x',label='Actual Rank')
        ax.scatter(x,y_pred,s=10,c='r',marker='o',label='Predicted Rank')
        ax.legend(('Actual Rank','Predicted Rank'),'lower right')

    p(ax1,train,t+' (train)')
    p(ax2,test,t+' (test)')

    plt.show()


def plot_hyper(f,XY,XY2):
    pr_max =50
    occ_max =50
    train = plt.figure(1)
    test = plt.figure(2)
    ax = train.gca(projection='3d')
    ax.set_title("Training data")
    ax2 = test.gca(projection='3d')
    ax2.set_title("Test data")
    a = np.arange(-1,pr_max)
    b = np.arange(-1,occ_max)
    a,b = np.meshgrid(a,b)
    Z = np.zeros(a.shape)

    for i in np.arange(len(a)):
        for j in np.arange(len(a[0])):
            Z[i][j] = f(np.matrix([a[i][j],b[i][j]]))[0,0]

    ax.plot_wireframe(a, b, Z)
    ax2.plot_wireframe(a, b, Z)
    ax2.plot_surface(a, b, Z, rstride=8, cstride=8, alpha=0.3, cmap=cm.coolwarm)
    cset = ax2.contour(a, b, Z, zdir='z', offset = -0.1, cmap=cm.coolwarm)
    ax.plot_surface(a, b, Z, rstride=8, cstride=8, alpha=0.3, cmap=cm.coolwarm)
    cset = ax.contour(a, b, Z, zdir='z', offset = -0.1, cmap=cm.coolwarm)
    label(ax)
    label(ax2)
    A = np.matrix(XY[0])
    A, ind = zip(*[(XY[0][i],i) for i in np.arange(len(XY[0])) if (XY[0][i][0]<pr_max and XY[0][i][1]<occ_max)])
    A = np.matrix(A)
    X = A[:,0]
    Y = A[:,1]
    Z_act = XY[1]
    Z_act = [XY[1][i] for i in ind]
    ax.scatter(X,Y,Z_act,c='r')

    A2, ind2 = zip(*[(XY2[0][i],i) for i in np.arange(len(XY2[0])) if XY2[0][i][0]<pr_max and XY2[0][i][1]<occ_max])
    A2 = np.matrix(A2)
    X2 = A2[:,0]
    Y2 = A2[:,1]
    Z_tst = [XY2[1][i] for i in ind2]
    ax2.scatter(X2,Y2,Z_tst,c='r')
    plt.show()
   # test.show()



