from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_feature_set
import os, sys
from os.path import join, abspath
from spider import PageRank
from sorter import sort

def get_train_set(term):

    def get_cat(path):
        if (path in sort(term,test=True)):
            return 1

    training_set = []
    test_dir = abspath('../Test')
    for root, dirs, files in os.walk(test_dir):
        for f in files:
            training_set.append((get_feature_set(term,join(root,f)),get_cat(join(root,f))))
            if get_cat(join(root,f))==1:
                print join(root,f)
    return training_set

def train(train_set):
    nb = NBC.train(train_set)
    return nb


if __name__ == "__main__":
    term = unicode(sys.argv[1])
    train(get_train_set(term))

