class PreciseFraction:

    def __init__(self,num,denom=1):
        self.num = num
        self.denom = denom

    def __radd__(self,other):
        if (not self.denom==other.denom):
            print "Denominators don't match!"
        else:
            if (self.num+other.num==self.denom):
                return PreciseFraction(1)
            else:
                return PreciseFraction(self.num+other.num,self.denom)

    def __repr__(self):
        if (self.denom==1):
            return str(self.num)
        else:
            return str(self.num)  + '/' + str(self.denom)
