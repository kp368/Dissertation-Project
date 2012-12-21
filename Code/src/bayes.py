from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_train_set, get_feature_set
from os.path import abspath
import sys
from features import LabeledFeatureSetCollection as LFSC,FeatureSetCollection as FSC

def train(train_set):
    nb = NBC.train(train_set)
    return nb

def predict(page,words):
    nb = train(LFSC(words).train_set)
    fsets = FSC(words).train_set
    for fs in fsets:
        print nb.classify(fs)

if __name__ == "__main__":
    args = [abspath(sys.argv[1])]
    for i in sys.argv[2:len(sys.argv)]:
        term = PS().stem(unicode(i))
        args.append(term)
    predict(args[0],args[1])
