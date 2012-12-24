from numpy import squeeze, asarray, argmax, mat, ones, eye
from fractions import Fraction
from os.path import abspath
import cPickle

def get_pr_dir(test):
    if (test):
        return '../Data/test_pr.p'
    else:
        return '../Data/pr.p'

class PageRank:

    new = {}

    def __init__(self,crawler):
        #E models the teleportation step. Here it is a uniform distribution: all pages are equiprobable.
        self.E = Fraction(1,crawler.dim)*ones((crawler.dim,1))
        #s is the probability of following a random link
        self.s = 0.85
        #t is the probability of teleportation
        self.t = 1-self.s
        self.I = mat(eye(crawler.dim))
        #M = sG+tE && M(PR) = PR => PR = t*(I-s*G)^(-1)*E
        self.PR = self.t*((self.I-self.s*crawler.adjm).I)*self.E
        self.by_name = {}
        c = crawler
        for i, pr in enumerate(self.PR):
            self.by_name[abspath(c.index.reverse[i])] = pr[0,0]
        self.max = argmax(self.PR)

    def __repr__(self):
        return str(squeeze(asarray(self.PR)))

    def save(self,test=False):
        pagerank = get_pr_dir(test)
        with open(pagerank,"wb") as f:
            cPickle.dump(self,f)

    @classmethod
    def load(cls,test=False):
        pagerank = get_pr_dir(test)
        if test:
            if 'test' in cls.new:
                return cls.new['test']
            else:
                with open(pagerank,"r") as f:
                    cls.new['test'] = cPickle.load(f)
                return cls.new['test']
        else:
            if 'train' in cls.new:
                return cls.new['train']
            else:
                with open(pagerank,"r") as f:
                    cls.new['train'] = cPickle.load(f)
                return cls.new['train']
