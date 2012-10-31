from BeautifulSoup import BeautifulSoup
import sys

f = open(sys.argv[1],'r')
html = f.read()
soup = BeautifulSoup(html)
count = 0
for tag in soup.findAll('a'):
    if tag.has_key('href'):
        count += 1
        print tag['href']
print "Number of links to page %s is %d!" % (sys.argv[1],count)
