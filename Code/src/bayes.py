from nltk.classify.naivebayes import NaiveBayesClassifier as NBC
import sys
from features import LabeledFeatureSetCollection as LFSC, TestFeatureSetCollection as TFSC
from assessment import Assessment as A
from nltk import PorterStemmer as PS
import csv

def write_result(a,train_set,query):
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
    for term in sys.argv:
        args.append(unicode(term))
    predict(args)
