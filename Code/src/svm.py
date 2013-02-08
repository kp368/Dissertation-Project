from cvxopt.solvers import coneqp as QP
from random import sample
from cvxopt import matrix as m
from numpy import tanh, exp, mean, vstack, hstack, ones, zeros, matrix, random, linalg, arange, eye
import numpy.linalg as linalg

def lin(x,y):
    return (x*y.T)[0,0]

def gauss(x,y):
    sigma = 5
    return exp(-sigma*linalg.norm(x-y)**2)

def poly(x,y):
    a = 4.0
    d = 3
    return (a*(x*y.T)[0,0])**d

def sigmoid(x,y):
    a =1.0/300
    c =0
    return tanh(a*((x*y.T)[0,0])+c)

def comb_sum(x,y):
    return lin(x,y) + gauss(x,y)

def comb_wsum(x,y):
    a = 0.2
    return (a**2)*lin(x,y)+(1-a)**2*gauss(x,y)

def comb_prod(x,y):
    return lin(x,y)*gauss(x,y)

def solve(data, kern=lin):
   # OBX = matrix([[0.0008,3.0]
   #          ,[2,20.0]
   #          ,[0.0004,1]
   #          ,[5,0]])
   # Y = matrix([0.0,2.0,1.0,3.0]).T
   # X = matrix(data.XY[0],dtype='float')
   # Y = matrix(data.XY[1],dtype='float').T
    XY = zip(data.XY[0],data.XY[1])
    #trim the datapoints before passing to svm
    smpl = [XY[i] for i in sample(xrange(len(XY)),200)]
    X, Y = zip(*smpl)
    X = matrix(X, dtype='float')
    Y = matrix(Y, dtype='float').T
    e = 0.0
    C = 1
    a = svm(X, Y, e, C, kern)
    return a

def svm (X, Y, e, C, kern):
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
        k = matrix([[kern(x,y)] for y in X])
        return a.T * vstack((k,-k)) + b

    return predict

if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
    l = LFSC(args)
    solve(l)
