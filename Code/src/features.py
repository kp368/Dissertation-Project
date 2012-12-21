from collections import defaultdict
from os.path import join, abspath
from os import walk
from pagerank import PageRank
from sorter import sort
from util import clean
from nltk import PorterStemmer as PS

class LabeledFeatureSet:

    def __init__(self,term_cnt=None,stem_cnt=None,pr=None,cat=None):
       self.pr = pr
       self.stem_cnt = stem_cnt
       self.term_cnt = term_cnt
       self.cat = cat

    @property
    def fs(self):
        return dict(pr=self.pr,stem_cnt=self.stem_cnt,term_cnt=self.term_cnt)

    @property
    def tuple(self):
        return self.fs,self.cat

class LabeledFeatureSetCollection(defaultdict):

    def __init__(self,terms):
        super(LabeledFeatureSetCollection,self).__init__(lambda:defaultdict(LabeledFeatureSet))
        self.terms = terms
        self.pages = get_pages(test_dir)

    def compute_cat(self):
        for term in self.terms:
            res = sort(term,test=True)
            l = len(res)
            for page in self.pages:
                if (page in res[0:l/2]):
                    self[page][term].cat =1
                elif (page in res[l/2:l]):
                    self[page][term].cat =2
                else:
                    self[page][term].cat =0

    def compute_fs(self):
        for page in self.pages:
            pr = get_page_rank(page)
            clean_page = clean(page)
            for term in self.terms:
                self[page][term].pr = pr
                self[page][term].term_cnt = get_count(term,clean_page)
                stem = PS().stem(term)
                self[page][term].stem_cnt = get_count(stem,clean_page)

test_dir = abspath('../Test')

def get_page_rank(page):
    pr = PageRank.load(test=True)
    try:
        rank = pr.by_name[page]
    except KeyError:
        rank = 0
    return rank

def get_count(term,page):
    count = page.count(term)+page.count(term.title())
    return count

def get_pages(folder):
    pages = []
    for root, dirs, files in walk(folder):
        for f in files:
            page = join(root,f)
            pages.append(page)
    return pages

