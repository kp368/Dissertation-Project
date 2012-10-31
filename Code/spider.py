#Spider at the moment takes a seed webpage and outputs a matrix representing link structure.

from numpy import *
import sys
from BeautifulSoup import *


class Page:

    def __init__(self,name):
        self.name = name
        self.links = []

    def __repr__(self):
        return self.name + repr(self.links)


class Crawler:
    
    def __init__(self, prefix, seed):
        self.index = {seed: 0}
        self.seed = seed
        self.prefix = prefix
        self.pages = [Page(seed)]
    
    def parse(self, name):
        data = open(self.prefix + name,'r').read()
        return BeautifulSoup(data)

    def crawl(self,page=None):

        if not page:
            page = self.pages[0]

        soup = self.parse(page.name)
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


if __name__ == "__main__":

    #seed webpage must be supplied as an argument
    prefix = sys.argv[1]
    page_name = sys.argv[2]
    c = Crawler(prefix,page_name)
    c.crawl()
    dim = len(c.pages)
    matrix = zeros((dim,dim))
    for i in range(dim*dim):
        if i%dim in c.pages[i/dim].links:
            matrix.put([i],[1])
    print matrix
    print c.pages
