#!/usr/bin/python2
# Using the delta rule, find the weights required to perform the following classifications:
# Vectors (1, 1, 1, 1) and (−1, 1, −1, −1) are members of one class and have target value of 1;
# vectors (1, 1, 1, −1) and (1, −1, −1, 1) are members of another class and have target value of −1.
# Use a learning rate of 0.5 and starting weights of 0.
# Using each of the training vector as input, test the response of the net.

class perceptron:
    def __init__(self, w_vec, threshold):
        self.w_vec = w_vec
        self.threshold = threshold
        self.bias = -1 * threshold
    def transfer(self, yin):     #Calculates y = fθ(yin)
        if yin > self.threshold:
            return 1
        elif yin < -1 * self.threshold:
            return -1
        else:
            return 0
    def calc_yy(self, x_vec):   #Calculates yin = x.w + b
        if len(x_vec) != len(self.w_vec):
            raise Exception('Supplied input length does not match weight length.')
        yy = self.bias
        for xx,ww in zip(x_vec, self.w_vec):
            yy += xx*ww
        return yy
    def train(self, s_vec, t_vec, rate):
        if rate <= 0:
            raise Exception('Rate not positive.')
        if len(s_vec) != len(t_vec):
            raise Exception('Training set problem: input count does not match result count.')
        doLoop = True
        while doLoop == True:
            #
