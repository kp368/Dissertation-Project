from collections import defaultdict
from os.path import join, abspath
from os import walk
from pagerank import PageRank
from sorter import sort
from util import clean
from nltk import PorterStemmer as PS
import matplotlib.pyplot as plt

train_dir = abspath('../Train')
test_dir = abspath('../Test')

def get_page_rank(page,is_test):
    pr = PageRank.load(test=is_test)
    try:
        rank = pr.by_name[page]
    except KeyError:
        rank = 0
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

class LabeledFeatureSet(object):

    def __init__(self,term_cnt=None,stem_cnt=None,pr=None,cat=None,ordinal=None):
       self.pr = pr
       self.stem_cnt = stem_cnt
       self.term_cnt = term_cnt
       self.cat = cat
       self.ordinal = ordinal

    @property
    def fs(self):
        return dict(pr=self.pr,stem_cnt=self.stem_cnt,term_cnt=self.term_cnt)

    @property
    def tuple(self):
        return self.fs,self.cat

    @property
    def fv(self):
        return self.pr, self.term_cnt

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

    def compute_cat(self, is_test):
        for term in self.terms:
            res = sort(term,is_test)
            l = len(res)
            for page in self.pages:
                if (page in res[0:l/2]):
                    self[page][term].cat =0
                else:
                    self[page][term].cat =1

    def compute_ord(self, is_test):
        for term in self.terms:
            res = sort(term, is_test)
            for i, page in enumerate(res):
                self[page][term].ordinal = i


class TestFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms,nb):
        super(TestFeatureSetCollection,self).__init__(terms,TestFeatureSet)
        self.pages = get_pages(test_dir)
        self.compute_cat(True)
        self.terms = terms
        self.predict_cat(nb)

    def predict_cat(self,nb):
        for page in self.pages:
            pr = get_page_rank(page,True)
            clean_page = clean(page)
            for term in self.terms:
                self[page][term].pr = pr
                self[page][term].term_cnt, self[page][term].stem_cnt = get_count(term,clean_page)
                self[page][term].p_cat = nb.classify(self[page][term].fs)

class LabeledFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms):
        super(LabeledFeatureSetCollection,self).__init__(terms)
        self.pages = get_pages(train_dir)
        self.compute_cat(False)
        self.compute_fs(False)
        self.compute_ord(False)

    @property
    def train_set(self):
        train_set = []
        for p in self.pages:
            for t in self.terms:
                train_set.append(self[p][t].tuple)
        return train_set

    #return only relevant pages, e.g. those that have been actually ranked
    @property
    def XY(self):
        X, Y = [], []
        for p in self.pages:
            for t in self.terms:
                if self[p][t].ordinal != None:
                    X.append(self[p][t].fv)
                    Y.append(self[p][t].ordinal)
        return X, Y

    @property
    def X(self):
        X = []
        for p in self.pages:
            for t in self.terms:
                X.append(self[p][t].fv)
        return X

    @property
    def Y(self):
        Y = []
        for p in self.pages:
            for t in self.terms:
                Y.append(self[p][t].ordinal)
        return Y


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

