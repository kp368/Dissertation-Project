from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_train_set, get_feature_set
from os.path import abspath
import sys
from features import LabeledFeatureSetCollection as LFSC,FeatureSetCollection as FSC

def predict(page,words):
    nb = NBC.train(LFSC(words).train_set)
    t = TFSC(words,nb)
    return t

if __name__ == "__main__":
    args = [abspath(sys.argv[1])]
    for i in sys.argv[2:len(sys.argv)]:
        term = PS().stem(unicode(i))
        args.append(term)
    predict(args[0],args[1])
