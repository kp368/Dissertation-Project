from sets import Set
from os.path import dirname, abspath, normpath, join
from util import strip_punct
from bs4 import BeautifulSoup as BS

class Page:

    def __init__(self,path):
        self.path = path
        #use a set to avoid duplicate elements
        self.links = Set()

    #traverse a relative link to return a new page object 
    def relative(self,link):
        new_page = Page(normpath(join(self.root,link)))
        return new_page

    @property
    def root(self):
        return dirname(self.path)

    def soupify(self):
        data = open(self.path,'r').read()
        soup = BS(data,"lxml")
        return soup

    #parse a page into a clean unicode 
    def parse(self):
        soup = soupify()
        text = unicode(soup.get_text(u' '))
        clean = strip_punct(text).split()
        return clean

    def __repr__(self):
        return self.name #+ repr(self.links)

