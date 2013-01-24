from cvxopt.solvers import qp as QP
from cvxopt import matrix as m
import numpy as np
import numpy.linalg as linalg

def K_lin(x1,x2):
    return np.dot(x1,x2)

def get_kernel(data,tok='linear'):

    X = data.X

    #N = number of training samples
    N = len(X)

    # init an NxN matrix to hold the kernel matrix
    Q = np.zeros([N,N])

    if tok == 'linear':
        for i in np.arange(N):
            for j in np.arange(N):
                Q[i,j] = K_lin(X[i],X[j])

    return Q

def solve(data):

    N = len(data.X)
    Y = data.Y
    I = np.matrix(np.identity(N))
    E_min = (np.transpose(np.reshape(np.tensordot(np.array([1,-1]),I,0),[2*N,N])))
    E_pl = (np.transpose(np.reshape(np.tensordot(np.array([1,1]),I,0),[2*N,N])))
    P = (np.dot(np.dot(np.transpose(E_min),get_kernel(data,'linear')),E_min))
    A = (np.dot(np.ones((1,N)),E_min))
    G = (np.dot(np.ones((1,N)),E_pl))
    q = (np.transpose(np.dot(Y,E_min)))
    h = (0.5)
    b = 0.0
    print linalg.inv(P)
    return QP(m(P), m(q), m(G), m(h), m(A), m(b))


if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
    l = LFSC(args)
    solve(l)
