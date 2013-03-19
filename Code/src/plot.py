from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def bayes():
    plt.plot([0,1,1.6],[1.6,0.6,0],'r')
    plt.xticks(np.arange(3), ('0','M', ''))
    plt.yticks(np.arange(3), ('0','M', ''))
    plt.annotate('Class 1',xy=(1.5,1.5),xytext=(1.5,1.5))
    plt.annotate('Class 1',xy=(1.5,1.5),xytext=(0.5,1.5))
    plt.annotate('Class 1',xy=(1.5,1.5),xytext=(1.5,0.5))
    plt.annotate('Class 2',xy=(1.5,1.5),xytext=(0.5,0.5))
    plt.title('Classification with Interdependent Features')
    plt.ylabel('Feature 1')
    plt.xlabel('Feature 2')
    params = {'font.size': 16}
    plt.rcParams.update(params)
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
    pr_max =5
    occ_max =6
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
    #A, ind = zip(*[(XY[0][i],i) for i in np.arange(len(XY[0])) if (XY[0][i][0]<pr_max and XY[0][i][1]<occ_max)])
    #A = np.matrix(A)
    X = A[:,0]
    Y = A[:,1]
    Z_act = XY[1]
    #Z_act = [XY[1][i] for i in ind]
    ax.scatter(X,Y,Z_act,c='r')

    A2, ind2 = zip(*[(XY2[0][i],i) for i in np.arange(len(XY2[0])) if XY2[0][i][0]<pr_max and XY2[0][i][1]<occ_max])
    A2 = np.matrix(A2)
    X2 = A2[:,0]
    Y2 = A2[:,1]
    Z_tst = [XY2[1][i] for i in ind2]
    ax2.scatter(X2,Y2,Z_tst,c='r')
    train.show()
    test.show()
