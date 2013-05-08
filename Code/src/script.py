import features
import svm
import plot
import nbayes

def bayes():
    l = features.LabeledFeatureSetCollection([u'arcitecture',u'building'])
    nb = nbayes.Bayes(l.XY[0],l.XY[1],2)
    t = features.TestFeatureSetCollection([u'arcitecture',u'building'],l.t,nb)
    return l, t

def data():
    l = features.LabeledFeatureSetCollection([u'arcitecture',u'building'])
    t = features.TestFeatureSetCollection([u'arcitecture',u'building'])
    return l, t

def plt(l,t):
    f = svm.solve(l,svm.comb_prod)
    plot.plot(f,l.XY,t.XY)

def fit(h):
    l,t = data()
    if h=='step':
	S = svm.SVM(l.XY[0],l.get_XY(lambda x,y:x>=4)[1],0)
	S.sample()
	S.solve(svm.gauss,0.25)
	f = S.predict
        plot.plot_hyper(f,l.get_XY(lambda x,y: x>=4),t.get_XY(lambda x,y:x>=4))

    elif h=='step_bad':
	S = svm.SVM(l.XY[0],l.get_XY(lambda x,y:x>=4)[1],0)
	S.sample()
	S.solve(svm.gauss,0.15)
	f = S.predict
        plot.plot_hyper(f,l.get_XY(lambda x,y: x>=4),t.get_XY(lambda x,y:x>=4))
    elif h=='poly':
        S = svm.SVM(l.XY[0],l.get_XY(lambda x,y:x**2+y**2)[1],0);S.sample();S.solve(svm.poly,2); f = S.predict
        plot.plot_hyper(f,l.get_XY(lambda x,y:x**2+y**2),t.get_XY(lambda x,y:x**2+y**2))

    elif h =='lin':
	S = svm.SVM(l.XY[0],l.get_XY(lambda x,y:x+y)[1],0);S.sample();S.solve(svm.lin); f = S.predict
        plot.plot_hyper(f,l.get_XY(lambda x,y:x+y),t.get_XY(lambda x,y:x+y))

