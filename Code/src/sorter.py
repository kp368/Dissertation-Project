from indexer import search
from pagerank import PageRank
import sys
from random import random

def sort(uquery,test=False):
    res = search(uquery,test)
    pr = PageRank.load(test)
    def get_key(r):
        try:
            return pr.by_name[r]
        except KeyError:
            return random()/1000
    #print res
    # print '\n'
    return sorted(res,key=get_key,reverse=True)
    

if __name__ == "__main__":
    query = unicode(sys.argv[1])
    test = (sys.argv[2]=='True')
    print sort(query,test)

