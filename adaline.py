#!/usr/bin/python2

import math, sys, time

def drange(start, stop, step): #Generator for step <1, from http://stackoverflow.com/questions/477486/python-decimal-range-step-value
    r = start
    while r < stop:
            yield r
            r += step

class adaline:
    def __init__(self, w_vec):#, bias): #absorbed
        self.w_vec = w_vec
        #self.bias = bias #absorbed
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
        yin = 0
        #yin = self.bias #absorbed
        for xx,ww in zip(x_vec, self.w_vec):
            yin += xx*ww
        return yin

    def train(self, s_vec_list, t_vec, rate):
        if rate <= 0:
            raise Exception('Rate not positive: ' + str(rate))
        if len(s_vec_list) != len(t_vec):
            raise Exception('Training set problem: input count does not match result count.')
        insigFlag = False
        loopCount = 0
        while insigFlag == False and loopCount < numEpochs: #Loop till changes in the weights and bias are insignificant.
            for s_vec, tt in zip(s_vec_list, t_vec):
                yin = self.calc_yin(s_vec)
                yy = self.transfer(yin, isTraining = True) # yy = yin
                w_change = list()
                bias_change = -2*rate*(yin - tt)
                for i in range(len(self.w_vec)):
                    w_change.append(bias_change*s_vec[i])
                if verbose_flag:
                    print "yy: ", yy
                    #print "bias_change: ", bias_change #absorbed
                    print "w_change: ", w_change
                #self.bias = self.bias + bias_change #absorbed
                for ii,wc in enumerate(self.w_vec):
                    self.w_vec[ii] = wc + w_change[ii]
                    
                #if math.fabs(bias_change) < 0.1: #absorbed
                insigFlag = True #time to check if we need to exit
                for wc in w_change:
                    if math.fabs(wc) < 0.1:
                        insigFlag = True
                    else:
                        insigFlag = False
                        break
                #time.sleep(1)
            loopCount += 1
###
verbose_flag = False
if len(sys.argv) > 2:
    raise Exception('Too many arguments. Usage: adaline.py [-v|--verbose]')
elif len(sys.argv) == 1:
    pass
elif sys.argv[1] == '-v' or sys.argv[1] == '--verbose':
    verbose_flag = True
else:
    raise Exception('Bad argument. Usage: adaline.py [-v|--verbose]')

numEpochs = 100
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
    test_s_vec.insert(0,1) #absorbing the bias by placing an input shorted to 1 at the head of each training vector
for alpha in [0.1,0.5]:#drange(0.01,1,0.01):
    p = adaline([0 for x in test_s_vec_list[0]])#, 0) #absorbed
    #alpha = 0.1 #ACTUAL: 0.5
    p.train(test_s_vec_list, test_t_vec, rate=alpha)
    if verbose_flag:
        print "bias+weights: ", p.w_vec
    sol_vec = list()
    for test_s_vec in test_s_vec_list:
        sol_vec.append(p.transfer(p.calc_yin(test_s_vec), isTraining = False))
    if verbose_flag:
        print 'Solution: ', sol_vec, '\nExpected (t_vec): ', test_t_vec
    match_flag = True
    for i,j in zip(sol_vec, test_t_vec):
        if i != j:
            match_flag = False
            break
    if match_flag:
        print 't_vec matched with rate', alpha
