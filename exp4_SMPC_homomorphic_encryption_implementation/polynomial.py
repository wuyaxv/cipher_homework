#!/usr/bin/env python3

class Polynomial(object):
    """计算多项式向量系数矩阵"""

    def __init__(self, *Xs):

        self.coefficients   = []
        self.coeffi_len     = len(Xs)
        self.Xs = []

        for _ in Xs:
            self.Xs.append(-1 * _)
        
        self.CalcCoefficient()

    def CalcCoefficient(self):

        for _ in range(0, self.coeffi_len+1):
            tmp = self.recursive(N=self.coeffi_len, k=_, i=0)
            self.coefficients.append(tmp)
        self.coefficients.reverse()

    def getCoefficient(self):
        return tuple(self.coefficients)

    def recursive(self, N, k, i):

        if k > 0:
            produce = 0
            for _ in range(i, N-k+1):
                produce += self.Xs[_] * self.recursive(N, k-1, _+1)
            return produce
        else:
            return 1
    
    def __str__(self):
        s = "Coefficients: {"
        for i in self.coefficients:
            s += ' ' + str(i)
        s += ' }'

        return s
        
if __name__ == '__main__':
    p = Polynomial(1, 2)
    print(p.getCoefficient())
