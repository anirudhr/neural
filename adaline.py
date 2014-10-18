#!/usr/bin/python2

import math, time

class adaline:
    def __init__(self, w_vec, bias):
        self.w_vec = w_vec
        self.bias = bias
    def transfer(self, yin, isTraining = False):
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
        yin = 0#self.bias #absorbed bias
        for xx,ww in zip(x_vec, self.w_vec):
            yin += xx*ww
        return yin

    def train(self, s_vec_list, t_vec, rate):
        if rate <= 0:
            raise Exception('Rate not positive.')
        if len(s_vec_list) != len(t_vec):
            raise Exception('Training set problem: input count does not match result count.')
        insigFlag = False
        loopCount = 0
        while insigFlag == False and loopCount < 1000: #Loop till changes in the weights and bias are insignificant.
            for s_vec, tt in zip(s_vec_list, t_vec):
                yin = self.calc_yin(s_vec)
                yy = self.transfer(yin, isTraining = True) # yy = yin
                w_change = list()
                bias_change = -2*rate*(yin - tt)
                for i in range(len(self.w_vec)):
                    w_change.append(bias_change*s_vec[i])
                print "yy: ", yy
                print "bias_change: ", bias_change
                print "w_change: ", w_change
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
                #time.sleep(1)
            loopCount += 1
###

#ACTUAL
test_s_vec_list = [[1, 1, 1, 1], [-1, 1, -1, -1], [1, 1, 1, -1], [1, -1, -1, 1]]
test_t_vec = [1, 1, -1, -1]
#AND for 2
#test_s_vec_list = [[1, 1], [1, -1], [-1, 1], [-1, -1]]
#test_t_vec = [1, -1, -1, -1]
#AND for 4
#test_s_vec_list = [[1, 1, 1, 1], [1, -1, 1, -1], [-1, 1, -1, 1], [-1, -1, -1, -1]]
#test_t_vec = [1, -1, -1, -1]
for test_s_vec in test_s_vec_list:
    test_s_vec.insert(0,1)
p = adaline([0 for x in test_s_vec_list[0]], 0)
p.train(test_s_vec_list, test_t_vec, rate=0.05) #ACTUAL: 0.5
#print "bias: ", p.bias
print "bias+weights: ", p.w_vec
sol_vec = list()
for test_s_vec in test_s_vec_list:
    sol_vec.append(p.transfer(p.calc_yin(test_s_vec), isTraining = False))
print 'Solution: ', sol_vec, '\nExpected (t_vec): ', test_t_vec
for i,j in zip(sol_vec, test_t_vec):
    if i != j:
        print 't_vec not matched'
        break
