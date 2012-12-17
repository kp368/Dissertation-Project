#Take a page and return a feature set!
from bs4 import BeautifulSoup as BS
from spider import PageRank
import sys

def strip_punct(s):
    punctuation = u'!"#\'()*+,-./:;<=>?@[\]^_`{|}~'
    table = dict((ord(char),None) for char in punctuation)
    return s.translate(table)

def get_feature_set(uword,path_to_page):
    #pr=pagerank, count=number of times @word occurs on the page
    data = open(path_to_page,'r').read()
    soup = BS(data,"lxml")
    text = unicode(soup.get_text(u' '))
    count = strip_punct(text).split().count(uword)
    pr = PageRank.load().by_name[path_to_page]
    featureset=dict(pr=pr,count=count)
    return featureset

if __name__ == "__main__":
    word = unicode(sys.argv[1])
    path = sys.argv[2]
    print get_feature_set(word,path)

