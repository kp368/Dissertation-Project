import features
import svm
import plot

def data():
    l = features.LabeledFeatureSetCollection([u'arcitecture',u'building'])
    t = features.TestFeatureSetCollection([u'arcitecture',u'building'])
    return l, t

def plt(l,t):
    f = svm.solve(l,svm.comb_prod)
    plot.plot(f,l.XY,t.XY)
