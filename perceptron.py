#!/usr/bin/python2

import time

class perceptron:
    def __init__(self, w_vec, threshold, bias):
        self.w_vec = w_vec
        self.threshold = threshold
        self.bias = bias#self.bias = -1 * threshold
    def transfer(self, yin):     #Calculates y = f-theta(yin)
        if yin > self.threshold:
            return 1
        elif yin < -1 * self.threshold:
            return -1
        else:
            return 0
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
        iter_count = 0
        w_change_count = 0
        max_w_change = len(s_vec_list)
        while w_change_count < max_w_change:   #Step
            for s_vec, tt in zip(s_vec_list, t_vec):
                yin = self.calc_yin(s_vec)
                yy = self.transfer(yin)
                w_change = list()
                for i in range(len(self.w_vec)):
                    w_change.append(0)
                bias_change = 0
                if yy != tt:
                    for ii, ww in enumerate(self.w_vec):
                        w_change[ii] = rate*tt*s_vec[ii]
                        self.w_vec[ii] = ww + w_change[ii]
                    bias_change = rate*tt
                    #print '***', bias_change, '***'
                    self.bias += bias_change
                    #self.threshold = -1 * self.bias
                    w_change_count = 0
                else:
                    w_change_count += 1
                #print '***', w_change_count, '***'
                iter_count += 1
                print iter_count, ': ', str(s_vec), '|', yin, '|', yy, '|', tt, '|', str(w_change), bias_change, str(self.w_vec), '|', self.bias #'***', w_change_count, '***', 
                #time.sleep(1)
                if w_change_count == max_w_change:
                    break
###

p = perceptron([0, 0, 0], 0.2, 0)
p.train([[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]], [1, -1, -1, -1], 1)
#p = perceptron([0, 0], 0.2, 0)
#p.train([[1, 1], [1, -1], [-1, 1], [-1, -1]], [1, -1, -1, -1], 1)

######################OUTPUT###############################
# 1. How many steps does it take for convergence?
#       21 (with learning rate = 1)
# 2. What is the final set of weights and bias?
#       w_vec = [2, 2, 2], bias = -4
#FORMAT
#step_number: s_vec(q) | yin | y | t(q) | delta-w_vec | delta-b | w_vec | b
# 1 :  [1, 1, 1] | 0 | 0 | 1 | [1, 1, 1] 1 [1, 1, 1] | 1
# 2 :  [1, 1, -1] | 2 | 1 | -1 | [-1, -1, 1] -1 [0, 0, 2] | 0
# 3 :  [1, -1, 1] | 2 | 1 | -1 | [-1, 1, -1] -1 [-1, 1, 1] | -1
# 4 :  [-1, 1, 1] | 2 | 1 | -1 | [1, -1, -1] -1 [0, 0, 0] | -2
# 5 :  [1, 1, 1] | -2 | -1 | 1 | [1, 1, 1] 1 [1, 1, 1] | -1
# 6 :  [1, 1, -1] | 0 | 0 | -1 | [-1, -1, 1] -1 [0, 0, 2] | -2
# 7 :  [1, -1, 1] | 0 | 0 | -1 | [-1, 1, -1] -1 [-1, 1, 1] | -3
# 8 :  [-1, 1, 1] | 0 | 0 | -1 | [1, -1, -1] -1 [0, 0, 0] | -4
# 9 :  [1, 1, 1] | -4 | -1 | 1 | [1, 1, 1] 1 [1, 1, 1] | -3
# 10 :  [1, 1, -1] | -2 | -1 | -1 | [0, 0, 0] 0 [1, 1, 1] | -3
# 11 :  [1, -1, 1] | -2 | -1 | -1 | [0, 0, 0] 0 [1, 1, 1] | -3
# 12 :  [-1, 1, 1] | -2 | -1 | -1 | [0, 0, 0] 0 [1, 1, 1] | -3
# 13 :  [1, 1, 1] | 0 | 0 | 1 | [1, 1, 1] 1 [2, 2, 2] | -2
# 14 :  [1, 1, -1] | 0 | 0 | -1 | [-1, -1, 1] -1 [1, 1, 3] | -3
# 15 :  [1, -1, 1] | 0 | 0 | -1 | [-1, 1, -1] -1 [0, 2, 2] | -4
# 16 :  [-1, 1, 1] | 0 | 0 | -1 | [1, -1, -1] -1 [1, 1, 1] | -5
# 17 :  [1, 1, 1] | -2 | -1 | 1 | [1, 1, 1] 1 [2, 2, 2] | -4
# 18 :  [1, 1, -1] | -2 | -1 | -1 | [0, 0, 0] 0 [2, 2, 2] | -4
# 19 :  [1, -1, 1] | -2 | -1 | -1 | [0, 0, 0] 0 [2, 2, 2] | -4
# 20 :  [-1, 1, 1] | -2 | -1 | -1 | [0, 0, 0] 0 [2, 2, 2] | -4
# 21 :  [1, 1, 1] | 2 | 1 | 1 | [0, 0, 0] 0 [2, 2, 2] | -4
