from whoosh.fields import Schema, TEXT, ID, STORED
import os.path
from whoosh.index import create_in, open_dir
from whoosh.query import *
from BeautifulSoup import BeautifulSoup
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.filedb.filestore import FileStorage


#if __name__ == "__main__":

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    elif re.match('[.,\s]', str(element)): 
        return False
    #elif re.match('', str(element)): 
     #   return False
    return True


def getSchema():
    return Schema(title=TEXT(stored=True),content=TEXT,path=ID(unique=True,stored=True),time=STORED)

def add_doc(writer,path):
    file = open(path,'r')
    data = file.read()
    file.close()
    soup = BeautifulSoup(data)
    if (soup.title):
        title = unicode(soup.title.string)
    else:
        components = path.split(u'/')
        last = len(components)-1
        title = components[last]
    content = unicode(soup.getText(u' '))
    #texts = filter(visible,soup.body.findAll(text=True))
    mtime = os.path.getmtime(path)
    writer.add_document(title=title,content=content,path=path,time=mtime)

def traverse(dir):
    for root, dirs, files in os.walk(dir):
        for f in files:
            yield root+u'/'+f


def index(dir):
    schema = getSchema()
    if not os.path.exists("index"):
        os.mkdir("index")
    store = FileStorage("index")
    ix = store.create_index(schema)
    writer = ix.writer() #TODO:use with
    for filename in traverse(dir):
        add_doc(writer,filename)
    writer.commit()


def search(query):
    store = FileStorage("index")
    ix = store.open_index()
    qp = QueryParser("content",schema=ix.schema)
    q = qp.parse(query)
    with ix.searcher() as s:
        results = s.search(q)
        for doc in results:
            print doc


