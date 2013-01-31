from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def scatter(ax):

    ax.set_xlabel('PageRank')
    ax.set_ylabel('Occurence')
    ax.set_zlabel('Ranking')

def plot(f,XY,XY2):
    pr_max =10
    occ_max =12
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
    scatter(ax)
    scatter(ax2)
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
