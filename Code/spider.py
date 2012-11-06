#Spider at the moment takes a seed webpage (index.asp or index.html), constructs a stochastic matrix G which represents the link structure of
#the web and then computes and outputs pagerank vector. The web is only the pages discovered from the seed page (which 
#is all the pages as wget crawls the web in the same fashion.

from fractions import Fraction
from numpy import *
import sys
from BeautifulSoup import BeautifulSoup
from sets import Set

#force full arrays to be printed
set_printoptions(threshold=nan)

class BiMap(dict):
    
    def __init__(self):
        super(BiMap,self).__init__()
        self.reverse = dict()

    def __setitem__(self,key,value):
        super(BiMap,self).__setitem__(key,value)
        self.reverse.__setitem__(value,key)


class Page:

    def __init__(self,name):
        self.name = name
        #use a set to avoid duplicate elements
        self.links = Set()

    def __repr__(self):
        return self.name #+ repr(self.links)


class Crawler:
    
    def __init__(self, prefix, seed):
        #index maps pages to indices
        self.index = BiMap()
        self.index[seed] = 0
        #seed is the page whose children are being explored. Page name without path.
        self.seed = seed
        #prefix is the path to the page
        self.prefix = prefix
        #pages keeps a list of pages in the order of discovery (depth first)
        self.pages = [Page(seed)]
        #discovers all the pages and links between them
        self.crawl()
        #number of pages in the web (also dimension for all the future matrices)
        self.dim = len(self.pages)
        #creates a probability matrix from the data discovered by crawl()
        self.adjm = self.matrify()
    
    def parse(self, name):
        data = open(self.prefix + name,'r').read()
        return BeautifulSoup(data)

    def crawl(self,page=None):

        if not page:
            page = self.pages[0]

        try:
            soup = self.parse(page.name)
        except IOError:    
            #if page is unfriendly assume it has no links!
            return

        for tag in soup.findAll('a'):
            if tag.has_key('href'):
                
                link = tag['href']
                if 'http' in link or 'mailto' in link:
                    continue

                if not link in self.index:
                    #the page is encountered for the first time    
                    next_index = len(self.pages)
                    new_page = Page(link)
                    self.index[link] = next_index
                    self.pages.append(new_page)
                    page.links.add(next_index)
                    self.crawl(new_page)
                else: 
                    #if the link has already been encountered
                    index_to_add = self.index[link]
                    page.links.add(index_to_add)

    def matrify(self):
        G = zeros((self.dim,self.dim))#,dtype='object')
        for (i, page) in enumerate(self.pages):
            #treat dangling pages as if they had links to every page in the web
            if(len(page.links)==0 or((len(page.links)==1)and i in page.links)):
                p = Fraction(1,self.dim)
                for n in xrange(0,self.dim):
                    G[n,i] = p
            else:
                #non-dangling pages share their 'importance' with all outgoing links equally
                for link in page.links:
                    G[link,i] = Fraction(1,len(page.links))
        return G


class PageRank:

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
        self.max = argmax(self.PR)
        
    def __repr__(self):
        return str(squeeze(asarray(self.PR)))

def near(a,b):
    return abs(a-b)<0.001

if __name__ == "__main__":
    #seed webpage must be supplied as an argument
    prefix = sys.argv[1]
    page_name = sys.argv[2]
    filename = prefix+'.txt'
    #f = open('filename.txt','w')
    c = Crawler(prefix,page_name)
    pr = PageRank(c)
    #f.write(pr.__repr__())
    #f.close()
    print c.index.reverse[pr.max]
