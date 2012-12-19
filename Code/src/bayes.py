from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_feature_set
import os, sys
from os.path import join, abspath
from spider import PageRank
from sorter import sort


def train(train_set):
    nb = NBC.train(train_set)
    return nb


if __name__ == "__main__":
    args = []
    for i in sys.argv:
        term = unicode(i)
        args.append(term)
   # train(get_train_set(term))

