#Spider at the moment takes a seed webpage (index.asp or index.html), constructs a stochastic matrix G which represents the link structure of
#the web and then computes and outputs pagerank vector. The web is only the pages discovered from the seed page (which 
#is all the pages as wget crawls the web in the same fashion.

from fractions import Fraction
from numpy import *
import sys
from BeautifulSoup import BeautifulSoup


class Page:

    def __init__(self,name):
        self.name = name
        self.links = []

    def __repr__(self):
        return self.name #+ repr(self.links)


class Crawler:
    
    def __init__(self, prefix, seed):
        self.index = {seed: 0}
        self.seed = seed
        self.prefix = prefix
        self.pages = [Page(seed)]
        self.crawl()
        self.dim = len(self.pages)
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
                    page.links.append(next_index)
                    self.crawl(new_page)
                else: 
                    #if the link has already been encountered
                    index_to_add = self.index[link]
                    page.links.append(index_to_add)

    def matrify(self):
        G = zeros((self.dim,self.dim))
        for (i, page) in enumerate(self.pages):
            if((len(page.links)==0) or((len(page.links)==1)and page.links[0]==i)):
                p = Fraction(1,self.dim)
                for n in xrange(0,self.dim):
                    G[n,i] = p
            else:
                for link in page.links:
                    G[link,i] = Fraction(1,len(page.links))
        return G



class PageRank:

    def __init__(self,crawler):
        self.E = Fraction(1,crawler.dim)*ones((crawler.dim,1))
        self.s = 0.85
        self.t = 1-self.s
        self.I = mat(eye(crawler.dim))
        self.PR = self.t*((self.I-self.s*crawler.adjm).I)*self.E
        self.one= sum(self.PR)
        
    def __repr__(self):
        return str(squeeze(asarray(self.PR)))



if __name__ == "__main__":
    #seed webpage must be supplied as an argument
    prefix = sys.argv[1]
    page_name = sys.argv[2]
    c = Crawler(prefix,page_name)
    pr = PageRank(c)
    print pr
    print pr.one
    print c.dim
