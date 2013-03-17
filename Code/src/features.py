from collections import defaultdict
from os.path import join, abspath
from os import walk
from pagerank import PageRank
from sorter import sort
from util import clean, has_image
from nltk import PorterStemmer as PS
import matplotlib.pyplot as plt
from random import random
from numpy import median

MODE = 'score'
CLASS = True
max_pr = 10
max_cnt = 12
train_dir = abspath('../Train')
test_dir = abspath('../Test')

def get_page_rank(page,is_test):
    pr = PageRank.load(test=is_test)
    try:
        rank = 1000*pr.by_name[page]
    except KeyError:
        rank = random()
    return rank

def get_count(term,page):
    t_count = page.count(term)+page.count(term.title())
    stem = PS().stem(term)
    s_count = page.count(stem)+page.count(stem.title())
    return t_count, s_count

def get_pages(folder):
    pages = []
    for root, dirs, files in walk(folder):
        for f in files:
            page = join(root,f)
            pages.append(page)
    return pages

def get_rpages(terms,test):
    pages = []
    for t in terms:
        res = sort(t,test)
        for page in res:
            pages.append(page)
    return pages


class LabeledFeatureSet(object):

    def __init__(self):

        #these are features of the page
        self.pr = None
        self.stem_cnt = None
        self.term_cnt = None
        self.pic = None

        #Now concerned with regression, no need to compute category
        #self.cat = cat
        #ordinal represents the rank of the page
        self.ordinal = None
        self.cat = None


    @property
    def score(self):
        return sum(self.fv)

    def get_score(self,g):
        #return sum(self.fv)
        if g:
            return g(self.pr, self.term_cnt, self.stem_cnt)
        else:
            return self.score

    @property
    def fs(self):
        return dict(pr=self.pr,stem_cnt=self.stem_cnt,term_cnt=self.term_cnt)

    @property
    def dict(self):
        if CLASS:
            return dict(fs=self.fs,cat=self.cat)
        else:
            return dict(fs=self.fs,ord=self.ordinal)

    @property
    def fv(self):
        return self.pr, self.term_cnt, self.stem_cnt, self.pic



class TestFeatureSet(LabeledFeatureSet):
    def __init__(self):
        super(TestFeatureSet,self).__init__()
        self.p_cat = None

class FeatureSetCollection(defaultdict):

    def __init__(self,terms,l=LabeledFeatureSet):
        super(FeatureSetCollection,self).__init__(lambda:defaultdict(l))
        self.terms = terms

    def compute_fs(self,is_test):
        for page in self.pages:
            pr = get_page_rank(page,is_test)
            clean_page = clean(page)
            for term in self.terms:
                self[page][term].pr = pr
                self[page][term].term_cnt, self[page][term].stem_cnt = get_count(term,clean_page)
                self[page][term].pic = has_image(page)

    def compute_cat(self,is_test):
        nums = []
        for page in self.pages:
            for term in self.terms:
                nums.append(self[page][term].score)
        mn = min(nums)
        mx = max(nums)
        t = int(round(median(nums),0))
        #t = int(round((mn+mx)/2,0))
        zero = 0
        one = 0
        for page in self.pages:
            for term in self.terms:
                if (int(round(self[page][term].score,0)))>t:
                    self[page][term].cat = 1
                    one += 1
                else:
                    self[page][term].cat = 0
                    zero += 1
                print self[page][term].score, '-->', self[page][term].cat

    def compute_ord(self, is_test):
        for term in self.terms:
            res = sort(term, is_test)
            for i, page in enumerate(res):
                self[page][term].ordinal = i


    @property
    def XY(self):
        return self.get_XY()

    def get_XY(self,g=None):
        X, Y = [], []
        for p in self.pages:
            for t in self.terms:
                s = self[p][t]
                if s.term_cnt>0:#s.ordinal != None and s.pr<max_pr and s.term_cnt<max_cnt:
                    X.append(self[p][t].fs)
                    if CLASS:
                        Y.append(self[p][t].cat)
                    elif MODE=='rank':
                        Y.append(self[p][t].ordinal)
                    elif MODE=='score':
                        Y.append(self[p][t].get_score(g))

        return X, Y

class TestFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms,nb=None):
        super(TestFeatureSetCollection,self).__init__(terms,TestFeatureSet)
        self.pages = get_rpages(terms,True)
        self.terms = terms
        self.compute_fs(True)
        if MODE=='rank':
            self.compute_ord(True)
        if nb:
            self.compute_cat(True)
            self.predict_cat(nb)

    def predict_cat(self,nb):
        for page in self.pages:
            pr = get_page_rank(page,True)
            clean_page = clean(page)
            for term in self.terms:
                self[page][term].pr = pr
                self[page][term].term_cnt, self[page][term].stem_cnt = get_count(term,clean_page)
                self[page][term].p_cat = nb.predict(self[page][term].fs)

    def get_results(self,g=None):
        act, pred = [], []
        for p in self.pages:
            for t in self.terms:
                s = self[p][t]
                if s.term_cnt>0:#s.ordinal != None and s.pr<max_pr and s.term_cnt<max_cnt:
                    act.append(s.cat)
                    pred.append(s.p_cat)

        return act, pred

class LabeledFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms):
        super(LabeledFeatureSetCollection,self).__init__(terms)
        self.pages = get_rpages(terms,False)
        self.compute_fs(False)
        if CLASS:
            self.compute_cat(False)
        if MODE=='rank':
            self.compute_ord(False)

    @property
    def train_set(self):
        train_set = []
        for p in self.pages:
            for t in self.terms:
                train_set.append(self[p][t].tuple)
        return train_set


    def plot(self,test):
        if test:
            self.pages = get_pages(test_dir)
            self.compute_fs(test)
        xs = []
        ys = []
        for term in self.terms:
            res = sort(term,test)
            for i, page in enumerate(res):
                pr = get_page_rank(page,test)
                xs.append(i)
                ys.append(pr)
        plt.scatter(xs,ys,s=3)
        plt.xlabel('PageRank')
        plt.ylabel('Returns order')
        if test:
            plt.title('PageRank and Rank correlation plot(Test data)')
        else:
            plt.title('PageRank and Rank correlation plot(Train data)')
        plt.show()


    def plot_3d(self,test):
        if test:
            self.pages = get_pages(test_dir)
            self.compute_fs(test)
        xs = []
        ys = []
        zs = []
        for term in self.terms:
            res = sort(term,test)
            for i, page in enumerate(res):
                pr = get_page_rank(page,test)
                xs.append(i)
                ys.append(pr)
                zs.append(self[page][term].term_cnt)
        print zs
        #plt.scatter(xs,ys,s=2)
        #plt.axis([0,250,0,0.03])
        from mpl_toolkits.mplot3d import Axes3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(xs,ys,zs)
        plt.ylabel('PageRank')
        plt.xlabel('Returns order')
        if test:
            plt.title('PageRank and Rank correlation plot(Test data)')
        else:
            plt.title('PageRank and Rank correlation plot(Train data)')
        plt.show()

