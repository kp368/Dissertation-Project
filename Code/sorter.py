from indexer import search
from spider import PageRank
import sys

def sort(uquery):
    res = search(uquery)
    pr = PageRank.load()
    def get_key(r):
        try:
            return pr.by_name[r]
        except KeyError:
            return 0
    print sorted(res,key=get_key,reverse=True)

if __name__ == "__main__":
    query = unicode(sys.argv[1])
    sort(query)

