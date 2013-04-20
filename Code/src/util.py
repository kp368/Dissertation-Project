from bs4 import BeautifulSoup as BS
from nltk import PorterStemmer as PS

def strip_punct(s):
    """Take a string and return a unicode string 
    	with no punctuation symbols.

    >>> strip_punct(u'remove.the.dots')
    u'removethedots'

    >>> strip_punct(u'a very &confusing* line$')
    u'a very &confusing line$'

    >>> strip_punct('a (non)-unicode/ +string!!!')
    Traceback (most recent call last):
        ...
    TypeError: s must be unicode
    """

    if not isinstance(s,unicode):
       raise TypeError('s must be unicode')
    punctuation = u'!"#\'()*+,-./:;<=>?@[\]^_`{|}~'
    table = dict((ord(char),None) for char in punctuation)
    return s.translate(table)

def clean(path):
    """Take a page path and return the text on 
    	the page with no punctuation.     

    >>> clean('example_page.html')
    [u'Text', u'line', u'1', u'Text', u'line', u'2']

    >>> clean('example_no_text.html')
    []
    """
    f =open(path,'r') 
    data = f.read()
    soup = BS(data,"lxml")
    text = unicode(soup.get_text(u' '))
    clean = strip_punct(text).split()
    return clean

def has_image(path):
    """Take a page path and return image count.

    >>> has_image('example_page.html')
    1

    >>> has_image('example_no_text.html')
    0

    >>> has_image('3images.html')
    3
    """

    with open(path,'r') as f:
        data = f.read()
    soup = BS(data,"lxml")
    num = len(soup.findAll("img"))
    if num > 16:
        num = 16
    return num

if __name__ == "__main__":
    import doctest
    doctest.testmod()
