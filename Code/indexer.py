from whoosh.fields import Schema, TEXT, ID, STORED
import os.path
from whoosh.index import create_in, open_dir
from whoosh.writing import BufferedWriter
from whoosh.query import *
from bs4 import BeautifulSoup
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher
from whoosh.filedb.filestore import FileStorage
import sys

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
    #Force BS to use lxml parser. It is the fastest.
    soup = BeautifulSoup(data,"lxml")
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


def index(dir,clean=False):
    if clean:
        clean_index(dir)
    else:
        incremental_index(dir)

def incremental_index(dir):
    store = FileStorage("index")
    ix = store.open_index()
    indexed_paths = set()
    to_index = set()

    with ix.searcher() as searcher:
        writer = ix.writer()
        for fields in searcher.all_stored_fields():
            indexed_path = fields['path']
            indexed_paths.add(indexed_path)
            if not os.path.exists(indexed_path):
                writer.delete_by_term('path',indexed_path)
            else:
                indexed_time = fields['time']
                mtime = os.path.getmtime(indexed_path)
                if mtime > indexed_time:
                    writer.delete_by_term('path',indexed_path)
                    to_index.add(indexed_path)

        for path in traverse(dir):
            if path in to_index or path not in indexed_paths:
                add_doc(writer,path)
        writer.commit()


def clean_index(dir):
    schema = getSchema()
    if not os.path.exists("index"):
        os.mkdir("index")
    store = FileStorage("index")
    ix = store.create_index(schema)
    wr = BufferedWriter(ix,period=1000,limit=1000)
    with wr as writer:
        for filename in traverse(dir):
            add_doc(writer,filename)


def search(query):
    store = FileStorage("index")
    ix = store.open_index()
    qp = QueryParser("content",schema=ix.schema)
    q = qp.parse(query)
    with ix.searcher() as s:
        results = s.search(q,limit=None)
        l = []
        for doc in results:
            l.append(doc['path'])
        return l

if __name__ == "__main__":
    folder = unicode(sys.argv[1])
    isClean = (sys.argv[2]=='True')
    print folder, isClean
    index(folder,isClean)
