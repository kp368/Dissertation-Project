from whoosh.fields import Schema, TEXT, ID
import os.path
from whoosh.index import create_in, open_dir
from whoosh.query import *
from BeautifulSoup import BeautifulSoup
from whoosh.qparser import QueryParser
from whoosh.searching import Searcher


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

def index(folder,query):
    schema = Schema(title=TEXT(stored=True), content=TEXT, path=ID(stored=True))
    if not os.path.exists("index"):
        os.mkdir("index")

    ix = create_in("index",schema)
    writer = ix.writer()
    
    for filename in os.listdir(folder):
       # if os.path.isdir(folder+'/'+filename):
        #    print filename +"is a directory" 
        data = open(folder+filename,'r').read()
        soup = BeautifulSoup(data)
        if (soup.title):
            myTitle = soup.title.string
        #texts = filter(visible,soup.getText(' '))
        myContent = soup.getText(u' ')
        myPath = folder+filename

        writer.add_document(title=myTitle,content=myContent,
                path=myPath)
    writer.commit()


def search(query):
    ix = open_dir("index")
    qp = QueryParser("content",schema=ix.schema)
    q = qp.parse(query)
    with ix.searcher() as s:
        results = s.search(q)
        for doc in results:
            print doc


        #print str(title) + str(path)#  + str(content)




