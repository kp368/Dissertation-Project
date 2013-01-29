from features import LabeledFeatureSetCollection as L, TestFeatureSetCollection as T
import svm
import plot

l = L([u'building',u'arcitecture',u'construction',u'materials'])
t = T([u'building',u'arcitecture',u'construction',u'materials'])

f = svm.solve(l)
plot.plot(f,l.XY,t.XY)
