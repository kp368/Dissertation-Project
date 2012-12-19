#Spider at the moment takes a seed webpage (index.asp or index.html), constructs a stochastic matrix G which represents the link structure of
#the web and then computes and outputs pagerank vector. The web is only the pages discovered from the seed page (which 
#is all the pages as wget crawls the web in the same fashion.

from pagerank import PageRank
import sys
from os.path import dirname, abspath, normpath, join
from page import Page
from numpy import zeros, set_printoptions, nan
from fractions import Fraction

#force full arrays to be printed
set_printoptions(threshold=nan)


class BiMap(dict):

    def __init__(self):
        super(BiMap,self).__init__()
        self.reverse = dict()

    def __setitem__(self,key,value):
        super(BiMap,self).__setitem__(key,value)
        self.reverse.__setitem__(value,key)


class Crawler:

    def __init__(self, seed):
        #index maps pages to indices
        self.index = BiMap()
        self.index[seed] = 0
        #seed is the page whose children are being explored. Page name without path.
        self.seed = seed
        #pages keeps a list of pages in the order of discovery (depth first)
        self.pages = [Page(seed)]
        #discovers all the pages and links between them
        self.crawl()
        #number of pages in the web (also dimension for all the future matrices)
        self.dim = len(self.pages)
        #creates a probability matrix from the data discovered by crawl()
        self.adjm = self.matrify()

    def crawl(self,page=None):

        if not page:
            page = self.pages[0]

        try:
            soup = page.soupify()
        except IOError:
            #if page is unfriendly assume it has no links!
            print 'IGNORED PAGE: '+ page.path#TODO:add logging
            return

        for tag in soup.findAll('a'):
            if tag.has_key('href'):
                link = tag['href']
                if 'http' in link or 'mailto' in link:
                    continue

                new_page = page.relative(link)

                if not new_page.path in self.index:
                    #the page is encountered for the first time    
                    next_index = len(self.pages)
                    self.index[new_page.path] = next_index
                    self.pages.append(new_page)
                    page.links.add(next_index)
                    self.crawl(new_page)
                else: 
                    #if the link has already been encountered
                    index_to_add = self.index[new_page.path]
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


if __name__ == "__main__":
    #seed webpage must be supplied as an argument
    page_name = abspath(sys.argv[1])
    isTest = (sys.argv[2]=='True')
    c = Crawler(page_name)
    pr = PageRank(c)
    print pr.by_name
    pr.save(isTest)
