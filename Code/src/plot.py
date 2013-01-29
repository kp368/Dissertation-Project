from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np

def plot(f,XY,XY2):
    train = plt.figure(1)
    test = plt.figure(2)
    ax = train.gca(projection='3d')
    ax.set_title("Training data")
    ax2 = test.gca(projection='3d')
    ax2.set_title("Test data")
    a = np.arange(0,80)
    b = np.arange(0,80)
    #a , b = np.arange(0,4), np.arange(0,4)
    a,b = np.meshgrid(a,b)

    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_zlim(0, 500)
    ax2.set_xlim(0, 20)
    ax2.set_ylim(0, 20)
    ax2.set_zlim(0, 500)
    Z = np.zeros(a.shape)

    for i in np.arange(len(a)):
        for j in np.arange(len(a[0])):
            Z[i][j] = f(np.matrix([a[i][j],b[i][j]]))[0,0]

    #surf = ax.plot_surface(a, b, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
    #        linewidth=0, antialiased=False)
    ax.plot_wireframe(a, b, Z)
    ax2.plot_wireframe(a, b, Z)
    ax.set_xlabel('PageRank')
    ax.set_ylabel('Occurence')
    ax.set_zlabel('Ranking')

    ax2.set_xlabel('PageRank')
    ax2.set_ylabel('Occurence')
    ax2.set_zlabel('Ranking')
    Z_act = XY[1]
    A = np.matrix(XY[0])
    X = A[:,0]
    Y = A[:,1]
    ax.scatter(X,Y,Z_act,c='r')

    Z_tst = XY2[1]
    A2 = np.matrix(XY2[0])
    X2 = A2[:,0]
    Y2 = A2[:,1]
    ax2.scatter(X2,Y2,Z_tst,c='r')
    #x,y,z = [0.0008,2,0.0004,5],[3,20,1,0],[0,2,1,3]
    #ax.scatter(x,y,z)
    train.show()
    test.show()
