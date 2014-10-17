#!/usr/bin/python2

import math

class adaline:
    def __init__(self, w_vec, bias):
        self.w_vec = w_vec
        self.bias = bias
    def transfer(self, yin, isTraining = False):     #Calculates y = fθ(yin)
        if isTraining: #training, f(yin) = yin
            return yin
        else:   #not training, f(yin) = bipolar Heaviside step function
            if yin >= 0:
                return 1
            else:
                return -1
    def calc_yin(self, x_vec):   #Calculates yin = x.w + b
        if len(x_vec) != len(self.w_vec):
            raise Exception('Supplied input length does not match weight length.')
        yin = self.bias
        for xx,ww in zip(x_vec, self.w_vec):
            yin += xx*ww
        return yin

    def train(self, s_vec_list, t_vec, rate):
        if rate <= 0:
            raise Exception('Rate not positive.')
        if len(s_vec_list) != len(t_vec):
            raise Exception('Training set problem: input count does not match result count.')
        insigFlag = False
        while insigFlag == False: #Loop till changes in the weights and bias are insignificant.
            for s_vec, tt in zip(s_vec_list, t_vec):
                yin = self.calc_yin(s_vec)
                yy = self.transfer(yin, isTraining = True) # yy = yin
                w_change = list()
                bias_change = -2*rate*(yin - tt)
                for i in range(len(self.w_vec)):
                    w_change.append(bias_change*x_vec[i])
                self.bias = self.bias + bias_change
                for ii,wc in enumerate(self.w_vec):
                    self.w_vec[ii] = wc + w_change[ii]
                    
                if math.fabs(bias_change) < 0.1: #time to check if we need to exit
                    insigFlag = True
                    for wc in w_change:
                        if math.fabs(wc) < 0.1:
                            insigFlag = True
                        else:
                            insigFlag = False
                            break
###

p = adaline([0, 0, 0], 0.1, 0)
p.train([[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]], [1, -1, -1, -1], 1)
#p = adaline([0, 0], 0.2, 0)
#p.train([[1, 1], [1, -1], [-1, 1], [-1, -1]], [1, -1, -1, -1], 1)
