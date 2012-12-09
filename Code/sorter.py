from indexer import search
from spider import PageRank

res = search(u'Architecture')
print res
pr = PageRank.load()
print '\n'
def get_key(r):
    try:
        return pr.by_name[r]
    except KeyError:
        return 0
print sorted(res,key=get_key,reverse=True)

