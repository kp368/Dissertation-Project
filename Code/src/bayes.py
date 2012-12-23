from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
from parser import get_train_set, get_feature_set
from os.path import abspath
import sys
from features import LabeledFeatureSetCollection as LFSC,FeatureSetCollection as FSC
from assessment import Assessment as A
from nltk import PorterStemmer as PS
import csv

def write_csv(a,train_set,query):
    with open('results.csv','a') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(['NaiveBayes 3',train_set,query,
            a.value,a.correct,a.incor])

def predict(words):
    t_set = LFSC(words).train_set
    nb = NBC.train(t_set)
    t = TFSC(words,nb)
    a = A(t)
    write_result(a,t_set,query)

if __name__ == "__main__":
    args = [abspath(sys.argv[1])]
    for i in sys.argv[2:len(sys.argv)]:
        term = PS().stem(unicode(i))
        args.append(term)
    predict(args)
