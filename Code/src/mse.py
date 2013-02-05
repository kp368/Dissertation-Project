import numpy as np
import svm

class MSE:

    def __init__(self,data,f):
        self.act = np.array(data[1])
        self.pred = (map(lambda x: x[0,0],(map(f,data[0]))))

    @property
    def MSE(self):
        return np.sqrt(np.sum((self.act-self.pred)**2)/len(self.act))
