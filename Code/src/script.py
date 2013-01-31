from features import LabeledFeatureSetCollection as L, TestFeatureSetCollection as T
import svm
import plot

def data():
    l = L([u'arcitecture',u'building'])
    t = T([u'arcitecture',u'building'])
    return l, t

def plt(l,t):
    f = svm.solve(l,svm.comb_prod)
    plot.plot(f,l.XY,t.XY)
