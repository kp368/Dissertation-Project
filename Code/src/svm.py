from cvxopt.solvers import coneqp as QP
from random import sample
from cvxopt import matrix as m
from numpy import tanh, exp, mean, vstack, hstack, ones, zeros, matrix, random, linalg, arange, eye
import numpy.linalg as linalg

def lin(x,y,args=None):
    return (x*y.T)[0,0]

def gauss(x,y,sigma=0.5):
    return exp(-sigma*linalg.norm(x-y)**2)

def poly(x,y,d):
    a = 1.0
    return (a*(x*y.T)[0,0])**d

def sigmoid(x,y,a):
    c =0
    return tanh(a*((x*y.T)[0,0])+c)

def comb_sum(x,y,sigma):
    return lin(x,y) + gauss(x,y,sigma)

def comb_wsum(x,y,a):
    return (a**2)*lin(x,y)+(1-a)**2*gauss(x,y)

def comb_prod(x,y,args):
    return lin(x,y)*gauss(x,y, args)

class SVM:

    def __init__(self,X,Y):
        self.X = X
        self.Y = Y

    def sample(self):
        X = self.X
        Y = self.Y
        XY = zip(X,Y)
        smpl = [XY[i] for i in sample(xrange(len(XY)),200)]
        return zip(*smpl)

    def solve(self, kern=lin, args=None):
        X = self.X
        Y = self.Y
       # OBX = matrix([[0.0008,3.0]
       #          ,[2,20.0]
       #          ,[0.0004,1]
       #          ,[5,0]])
       # Y = matrix([0.0,2.0,1.0,3.0]).T
       # X = matrix(data.XY[0],dtype='float')
       # Y = matrix(data.XY[1],dtype='float').T
        #trim the datapoints before passing to svm
        X = matrix(X, dtype='float')
        Y = matrix(Y, dtype='float').T
        e = 0.0
        C = 1
        N = len(X)
        E = ones((N,1))
        E2 = vstack((E, E))
        K = matrix([[kern(x,y) for x in X] for y in X])
        #K = X*X.T
        P = vstack((hstack(( K,-K))
                  , hstack((-K, K))))
        #a trick to increase the rank of P without perturbing data too much
        #P = P + np.eye(2*N)*1e-10
        q = vstack((e*E-Y, e*E+Y))

        A = vstack((E, -E))
        I = eye(2*N)
        G = vstack((A.T, -I, I))
        h = vstack(([[0]],0*E2,C*E2))
        #b = 0.0

        a = matrix(QP(m(P), m(q), G=m(G), h=m(h))['x'])

        def predict (x):
            b = mean(Y - e - a.T * hstack((K,-K)).T)
            k = matrix([[kern(x,y,args)] for y in X])
            return a.T * vstack((k,-k)) + b

        return predict


if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
    l = LFSC(args)
    solve(l)
