from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_feature_set
import os
from os.path import join, abspath
from spider import PageRank

def get_train_set():
    training_set = []
    test_dir = abspath('../Test')
    for root, dirs, files in os.walk(test_dir):
        for f in files:
            training_set.append((get_feature_set(u'architect',join(root,f)),1))
    return training_set

def train():
    nb = NBC.train(get_train_set())
    return nb


if __name__ == "__main__":
    print get_train_set()
