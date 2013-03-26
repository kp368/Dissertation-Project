from collections import defaultdict
from os.path import join, abspath
from os import walk
from pagerank import PageRank
from sorter import sort
from util import clean, has_image
from nltk import PorterStemmer as PS
import matplotlib.pyplot as plt
from random import random, choice
from numpy import median, mean, arange, array_split, array, ones

QUANT = 7
MODE = 'score'
CLASS = False
max_pr = 10
max_cnt = 12
train_dir = abspath('../Train')
test_dir = abspath('../Test')


def get_page_rank(page,is_test):
    pr = PageRank.load(test=is_test)
    try:
        rank = 1000*pr.by_name[page]
    except KeyError:
        rank = choice(arange(5))
    return int(round(rank,0))

def get_count(term,page):
    t_count = page.count(term)+page.count(term.title())
    stem = PS().stem(term)
    s_count = page.count(stem)+page.count(stem.title())
    return t_count, s_count

def get_pages(test):
    pages = []
    if test:
        folder = test_dir
    else:
        folder = train_dir
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
        #self.stem_cnt = None
        self.term_cnt = None
        #self.img = None
        #self.wd_cnt = None
        #self.has_price = choice(arange(20))
        #self.has_contacts = choice(arange(30))
        #self.has_ads = choice(arange(4))
        #self.form = choice(arange(5))

        #Now concerned with regression, no need to compute category
        #self.cat = cat
        #ordinal represents the rank of the page
        self.ordinal = None
        self.cat = None

    @property
    def score(self):
        return sum(self.fv)

#Various score functions used in evaluation
    def get_sep(self):
        if self.img +self.term_cnt > 4.1:
            return 50.0
        else:
            return 1.0

    def get_insep(self):
        if self.pr > 1.3:
            if self.term_cnt > 0:
                return 50
            else:
                return 1
        elif self.term_cnt > 0:
            return 1.0
        else:
            return 50.0

    def get_score(self,g):
        #return sum(self.fv)
        if g:
            return g(self.term_cnt,self.pr)
        else:
            return self.score

    @property
    def fs(self):
        return dict(term_cnt=self.term_cnt,pr=self.pr)

    @property
    def dict(self):
        if CLASS:
            return dict(fs=self.fs,cat=self.cat)
        else:
            return dict(fs=self.fs,ord=self.ordinal)

    @property
    def fv(self):
        return self.fs.values()



class TestFeatureSet(LabeledFeatureSet):
    def __init__(self):
        super(TestFeatureSet,self).__init__()
        self.p_cat = None

class FeatureSetCollection(defaultdict):

    def __init__(self,terms,l=LabeledFeatureSet):
        super(FeatureSetCollection,self).__init__(lambda:defaultdict(l))
        self.terms = terms
        self.t = None

    def get_mean(self,cat):
        if QUANT==2:
            if cat==0:
                return 3
            else:
                return 16
            #return abs(self.t-cat*self.mx)/2.0+self.t*cat
        if QUANT==7:
            m = [mean(arange(self.t[i],self.t[i+1])) for i in arange(7)]
            return m[cat]


    def compute_fs(self,is_test):
        for page in self.pages:
            pr = get_page_rank(page,is_test)
            clean_page = clean(page)
            for term in self.terms:
                s = self[page][term]
                self[page][term].pr = pr
                self[page][term].term_cnt, self[page][term].stem_cnt = get_count(term,clean_page)
                #s.wd_cnt = s.term_cnt%len(clean(page))
                #s.has_price = choice(arange(15))# sum(list(get_count(u'price',clean_page)))
                #self[page][term].img = has_image(page)

    def compute_stat(self):
        nums = []
        for page in self.pages:
            for term in self.terms:
                nums.append(self[page][term].score)
        self.mn = min(nums)
        self.mx = max(nums)
        nums.sort()
        a = array_split(nums,7)
        self.t = [(a[i][len(a[i])-1]+a[i+1][0])/2.0 for i in xrange(6)]
        self.t.append(self.mn); self.t.append(self.mx); self.t.sort()

    def compute_cat(self,is_test):
        for page in self.pages:
            for term in self.terms:
                s = self[page][term]
                #if s.score <= self.t:
                #    s.cat = 0
                #else:
                #    s.cat =1
                if s.score <= self.t[1]:
                    s.cat = 0
                elif s.score <= self.t[2]:
                    s.cat = 1
                elif s.score <= self.t[3]:
                    s.cat = 2
                elif s.score <= self.t[4]:
                    s.cat = 3
                elif s.score <= self.t[5]:
                    s.cat = 4
                elif s.score <= self.t[6]:
                    s.cat = 5
                else:
                    s.cat = 6
                #print self[page][term].score,'-->',self[page][term].cat

    def compute_ord(self, is_test):
        for term in self.terms:
            res = sort(term, is_test)
            for i, page in enumerate(res):
                self[page][term].ordinal = 1.0/(i+1.0)


    @property
    def XY(self):
        return self.get_XY()

    def get_XY(self,g=None):
        X, Y = [], []
        for p in self.pages:
            for t in self.terms:
                s = self[p][t]
                #if s.term_cnt>0:#s.ordinal != None and s.pr<max_pr and s.term_cnt<max_cnt:
                X.append(self[p][t].fv)
                if CLASS:
                    Y.append(self[p][t].cat)
                elif MODE=='rank':
                    Y.append(self[p][t].ordinal)
                elif MODE=='score':
                    Y.append(self[p][t].get_score(g))

        return X, Y

    def get_points(self):
        tuples = [([],[]) for x in xrange(7)]
        for p in self.pages:
            for t in self.terms:
                s = self[p][t]
                tuples[s.cat][0].append(s.img)
                tuples[s.cat][1].append(s.term_cnt)
        return tuples

class TestFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms,nb=None):
        super(TestFeatureSetCollection,self).__init__(terms,TestFeatureSet)
        self.pages = get_rpages(terms,True)
        self.terms = terms
        #self.t = t
        self.compute_fs(True)
        if MODE=='rank':
            self.compute_ord(True)
        if nb:
            self.compute_cat(True)
            self.predict_cat(nb)

    def predict_cat(self,nb):
        for page in self.pages:
            #pr = get_page_rank(page,True)
            #clean_page = clean(page)
            for term in self.terms:
               # s = self[page][term]
               # self[page][term].pr = pr
               # self[page][term].term_cnt, self[page][term].stem_cnt = get_count(term,clean_page)
               # s.wd_cnt = len(clean_page)
               # self[page][term].img = has_image(page)
                self[page][term].p_cat = nb.predict(self[page][term].fs)

    def get_results(self,g=None):
        act, pred, ceil, bl = [], [], [], []
        for p in self.pages:
            for term in self.terms:
                s = self[p][term]
                #if s.term_cnt>0:#s.ordinal != None and s.pr<max_pr and s.term_cnt<max_cnt:
                act.append(s.score)
                pred.append(self.get_mean(s.p_cat))
                ceil.append(self.get_mean(s.cat))
                #print s.p_cat, s.cat, '-->', self.get_mean(s.p_cat), self.get_mean(s.cat)

        for i in act:
            bl.append(self.get_mean(choice(arange(QUANT))))

        return act, pred, bl, ceil

class LabeledFeatureSetCollection(FeatureSetCollection):

    def __init__(self,terms):
        super(LabeledFeatureSetCollection,self).__init__(terms)
        self.pages = get_rpages(terms,False)
        self.compute_fs(False)
        #self.compute_stat()
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


    def plot_d(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        cats = self.get_points()
        cols = ['b','g','r','c','m','y','k']
        t = [1,2,4,9,81,256]
        x = arange(0,20,2)
        for i,c in enumerate(cols):
            ax.scatter(cats[i][0],cats[i][1],color=c)
        for th in t:
            ax.plot(x,th-x**2)
        plt.show()

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

