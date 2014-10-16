#!/usr/bin/python2
# Using the delta rule, find the weights required to perform the following classifications:
# Vectors (1, 1, 1, 1) and (−1, 1, −1, −1) are members of one class and have target value of 1;
# vectors (1, 1, 1, −1) and (1, −1, −1, 1) are members of another class and have target value of −1.
# Use a learning rate of 0.5 and starting weights of 0.
# Using each of the training vector as input, test the response of the net.

class perceptron:
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

p = perceptron([0, 0, 0], 0.1, 0)
p.train([[1, 1, 1], [1, 1, -1], [1, -1, 1], [-1, 1, 1]], [1, -1, -1, -1], 1)
#p = perceptron([0, 0], 0.2, 0)
#p.train([[1, 1], [1, -1], [-1, 1], [-1, -1]], [1, -1, -1, -1], 1)
