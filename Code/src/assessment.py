class Assessment:

    def __init__(self,t):
        self.total = len(t)
        self.correct = [0,0,0]
        self.incor = [0,0,0]
        self.tot_correct = sum(self.correct)
        self.assess(t)
        self.value = self.tot_correct/self.total

    def assess(self,t):
        for p in t:
            for i in t[p]:
                if t[p][i].cat == t[p][i].p_cat:
                    self.tot_correct += 1
                    if t[p][i].cat == 2:
                        self.correct[2] += 1
                    elif t[p][i].cat == 1:
                        self.correct[1] += 1
                    else:
                        self.correct[0] += 1
                elif t[p][i].cat == 2:
                    self.incor[2] +=1
                elif t[p][i].cat == 1:
                    self.incor[1] +=1
                else:
                    self.incor[0] +=1



