from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_feature_set
import os

test_dir = 'Test'
for root, dirs, files in os.walk(test_dir):
    for f in files:
        get_feature_set(f)

nb = NBC.train(get_train_set())



