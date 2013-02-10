from bs4 import BeautifulSoup as BS
from nltk import PorterStemmer as PS

def strip_punct(s):
    punctuation = u'!"#\'()*+,-./:;<=>?@[\]^_`{|}~'
    table = dict((ord(char),None) for char in punctuation)
    return s.translate(table)

def clean(path):
    f =open(path,'r') 
    data = f.read()
    soup = BS(data,"lxml")
    text = unicode(soup.get_text(u' '))
    clean = strip_punct(text).split()
    return clean

def has_image(path):
    with open(path,'r') as f:
        data = f.read()
    soup = BS(data,"lxml")
    return len(soup.findAll("img"))
