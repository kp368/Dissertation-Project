from svm import SVM, lin, gauss, sigmoid, poly, comb_prod, comb_sum, comb_wsum
from mse import mse
import csv

def hyper_tune(train, test):
    X_tr = train.XY[0]
    X_ts = test.XY[0]
    params = [-0.5,-0.25,-0.15,-0.05,0]
    errors = [0.001,0.005]
    Y_tr = train.get_XY()[1]
    Y_ts = test.get_XY()[1]
    kernel = comb_prod

    with open('htun.csv','a') as f:
        writer = csv.writer(f)

        for e in errors:
            #compute a predict function with svm
            S = SVM(X_tr,Y_tr,e)
            S.sample()

            for p in params:
                    if S.solve(kernel,p)=='optimal':

                        fun = S.predict
                        #compute error for both train and test data
                        train_mse =  mse(X_tr,Y_tr,fun)
                        test_mse =  mse(X_ts,Y_ts,fun)

                        #write to memory
                        writer.writerow([e,p,train_mse,test_mse])
                    else:
                        writer.writerow([e,p,'Singular matrix'])


def evaluate(train,test):
    k_names = ['Lin ', 'Gaus', 'Prod', 'Poly']
    k_funs = {'Lin ':lin, 'Gaus':gauss, 'Poly':poly, 'Prod':comb_prod}
    h_names = ['Sum ','Sqrd']
    h_funs = {'Sum ':lambda x, y: x+y, 'Sqrd':lambda x, y: x**2+y}
    args = {'Lin ':[None], 'Gaus':[0.05,0.50,5.00,50.0], 'Poly':[2,3,4,5], 'Prod':[0.05,0.50,5.00,50.0]}

    X_tr = train.XY[0]
    X_ts = test.XY[0]
    error = 0.5

    with open('eval.csv','a') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(['-------------------------'])
        for h in h_names:
            for k in k_names:

                arg = args[k]

                heuristic = h_funs[h]
                Y_tr = train.get_XY(heuristic)[1]
                Y_ts = test.get_XY(heuristic)[1]

                #compute a predict function with svm
                S = SVM(X_tr,Y_tr,error)
                S.sample()
                kernel = k_funs[k] 

                for a in arg:
                    if S.solve(kernel,a)=='optimal':

                        fun = S.predict
                        #compute error for both train and test data
                        train_mse =  mse(X_tr,Y_tr,fun)
                        test_mse =  mse(X_ts,Y_ts,fun)

                        #write to memory
                        writer.writerow([h,k,a,train_mse,test_mse,error])

