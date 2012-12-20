from bs4 import BeautifulSoup as BS
from nltk import PorterStemmer as PS

def strip_punct(s):
    punctuation = u'!"#\'()*+,-./:;<=>?@[\]^_`{|}~'
    table = dict((ord(char),None) for char in punctuation)
    return s.translate(table)

def clean(path):
    data = open(path,'r').read()
    soup = BS(data,"lxml")
    text = unicode(soup.get_text(u' '))
    clean = strip_punct(text)
    stems = PS().stem(clean).split()
    return stems
