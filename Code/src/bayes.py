from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
import sys
from features import LabeledFeatureSetCollection as LFSC, TestFeatureSetCollection as TFSC
from assessment import Assessment as A
from nltk import PorterStemmer as PS
import csv

def write_result(a,train_set):
    with open('results.csv','a') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(['NaiveBayes 3', train_set,
            train_set, a.value, a.total, a.correct, a.incor])

def predict(train_query):
    nb = NBC.train(LFSC(train_query).train_set)
    t = TFSC(train_query,nb)
    a = A(t)
    write_result(a,train_query)

if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
    predict(args)
