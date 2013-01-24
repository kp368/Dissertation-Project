from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
import sys
from features import LabeledFeatureSetCollection as LFSC, TestFeatureSetCollection as TFSC
from assessment import NB3Assessment as NB3A
from nltk import PorterStemmer as PS
import csv

def write_result(a,train_set):
    with open('results.csv','a') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerow(['NaiveBayes 5',a.val, a.value,
            a.correct, a.incor, a.total, train_set])

def predict(train_query):
    nb = NBC.train(LFSC(train_query).train_set)
    t = TFSC(train_query,nb)
    a = NB3A(t)
    write_result(a,train_query)

def plot(args):
    l = LFSC(args)
    l.plot(False)
    l.plot(True)
    #l.plot_3d(False)
    l.plot_3d(True)


if __name__ == "__main__":
    args = []
    for term in sys.argv[1:len(sys.argv)]:
        args.append(unicode(term))
#    predict(args)
    plot(args)
