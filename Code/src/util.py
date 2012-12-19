
def strip_punct(s):
    punctuation = u'!"#\'()*+,-./:;<=>?@[\]^_`{|}~'
    table = dict((ord(char),None) for char in punctuation)
    return s.translate(table)
