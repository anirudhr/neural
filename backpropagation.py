#!/usr/bin/python2

#Find the new weights when the net illustrated in Figure 6.12 is presented the input pattern (0, l) and the target output is l. Use a learning rate of a = 0.25, and the binary sigmoid activation function.

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
