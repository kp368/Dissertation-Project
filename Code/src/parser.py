#Take a page and return a feature set!
from bs4 import BeautifulSoup as BS
from spider import PageRank
import sys
from page import Page
from util import strip_punct

#FeatureSet is a collection of predefined page qualities. Curently of form [(rank,count),cat]
class FeatureSet:
    def __init__(self,prank=None,count=None,cat=None):
        self.pr = prank
        self.cnt = count
        self.cat = cat

    



def get_feature_set(uwords,path_to_page):
    #pr=pagerank, count=number of times @word occurs on the page
    count = clean.count(uword)
    pr = PageRank.load(test=True)
    try:
        rank = pr.by_name[path_to_page]
    except KeyError:
        rank = 0
    if count>0:
        print path_to_page, rank, count
    featureset=dict(pr=rank,count=count)
    return featureset


def get_train_set(terms):

    test_dir = abspath('../Test')
    training_set = []

    def get_cat(path):
        if (path in sort(term,test=True)):
            return 1

    for root, dirs, files in os.walk(test_dir):
        for f in files:
            training_set.append((get_feature_set(terms,join(root,f)),get_cat(join(root,f))))
    return training_set


if __name__ == "__main__":
    word = unicode(sys.argv[1])
    path = sys.argv[2]
    print get_feature_set(word,path)

