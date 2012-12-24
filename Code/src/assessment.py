from fractions import Fraction

class Assessment:

    def __init__(self,t):
        self.t = t
        self.total = float(len(self.t)*len(self.t.terms))
        self.correct = [0,0,0]
        self.incor = [0,0,0]
        self.tot_correct = float(sum(self.correct))
        self.assess(self.t)
        self.value = 100*round(self.tot_correct/self.total,4)

    def assess(self):
        for p in self.t:
            for i in self.t[p]:
                if self.t[p][i].cat == self.t[p][i].p_cat:
                    self.tot_correct += 1
                    if self.t[p][i].cat == 2:
                        self.correct[2] += 1
                    elif self.t[p][i].cat == 1:
                        self.correct[1] += 1
                    else:
                        self.correct[0] += 1
                elif self.t[p][i].cat == 2:
                    self.incor[2] +=1
                elif self.t[p][i].cat == 1:
                    self.incor[1] +=1
                else:
                    self.incor[0] +=1



