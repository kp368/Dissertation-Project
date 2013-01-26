from cvxopt.solvers import coneqp as QP
from cvxopt import matrix as m
from numpy import mean, vstack, hstack, ones, zeros, matrix, random, linalg, arange, eye
import numpy.linalg as linalg

#def K_lin(x1,x2):
#    return (np.dot(x1,x2)+1)**2
#
#def get_kernel(data,tok='linear'):
#
#    X = data.X
#    
#    #N = number of training samples
#    N = len(X)
#
#    # init an NxN matrix to hold the kernel matrix
#    Q = np.zeros([N,N])
#
#    if tok == 'linear':
#        for i in np.arange(N):
#            for j in np.arange(N):
#                Q[i,j] = K_lin(X[i],X[j])+1
#
#    R = np.random.rand(N,N)
#    return R

def solve(data):
    #X = matrix([[1.0,3.0]
    #         ,[2.0,2.0]
    #         ,[3.0,1.0]])
    #Y = matrix([2.0,4.0,6.0]).T
    X = matrix(data.XY[0],dtype='float')
    Y = matrix(data.XY[1],dtype='float').T
    e = 2
    C = 1
    a = svm(X, Y, e, C)
    return a

def svm (X, Y, e, C):
    N = len(X)
    #N = len(data.X)
    E = ones((N,1))
    E2 = vstack((E, E))
    #K = get_kernel(data,'linear')
    K = X*X.T
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

    #x is a matrix of form
    def predict (x):
        b = mean(Y - e - a.T * hstack((X*X.T,-X*X.T)).T)
        return a.T * hstack((x*X.T,-x*X.T)).T + b

    return predict

if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
    l = LFSC(args)
    solve(l)
