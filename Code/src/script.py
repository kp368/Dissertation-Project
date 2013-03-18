import features
import svm
import plot
import nbayes

def bayes():
    l = features.LabeledFeatureSetCollection([u'arcitecture',u'building'])
    nb = nbayes.Bayes(l.XY[0],l.XY[1],2)
    t = features.TestFeatureSetCollection([u'arcitecture',u'building'],nb)
    return t

def data():
    l = features.LabeledFeatureSetCollection([u'arcitecture',u'building'])
    t = features.TestFeatureSetCollection([u'arcitecture',u'building'])
    return l, t

def plt(l,t):
    f = svm.solve(l,svm.comb_prod)
    plot.plot(f,l.XY,t.XY)
