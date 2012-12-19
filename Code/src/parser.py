#Take a page and return a feature set!
from bs4 import BeautifulSoup as BS
from os.path import abspath, join
from os import walk
from pagerank import PageRank
import sys
from page import Page
from sorter import sort
from util import clean

def get_feature_set(uword,path_to_page):
    #pr=pagerank, count=number of times @word occurs on the page
    clean_page = clean(path_to_page)
    count = clean_page.count(uword)
    pr = PageRank.load(test=True)
    try:
        rank = pr.by_name[path_to_page]
    except KeyError:
        rank = 0
    featureset=dict(pr=rank,count=count)
    return featureset


def get_train_set(term):

    test_dir = abspath('../Test')
    training_set = []

    def get_cat(path):
        res = sort(term,test=True)
        l = len(res)
        if (path in res[0:l/2]):
            return 1
        elif (path in res[l/2:l]):
            return 2
        else:
            return 0

    for root, dirs, files in walk(test_dir):
        for f in files:
            path = join(root,f)
            fs = get_feature_set(term,path)
            cat = get_cat(path)
            training_set.append((fs,cat))
            if cat != 0:
                print (path,fs,cat)
    return training_set


if __name__ == "__main__":
    word = unicode(sys.argv[1])
    path = sys.argv[2]
    print get_train_set(word)

