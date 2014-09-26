#!/usr/bin/python2

class perceptron:
    def __init__(self, w_vec, threshold):
        self.w_vec = w_vec
        self.threshold = threshold
        self.bias = -1 * threshold
    def transfer(self, xx):
        if xx > self.threshold:
            return 1
        elif xx < -1 * self.threshold:
            return -1
        else:
            return 0
    def calc_yy(self, x_vec):
        if len(x_vec) != len(self.w_vec):
            raise Exception('Supplied input length does not match weight length.')
        yy = self.bias
        for xx,ww in zip(w_vec, self.w_vec):
            yy += xx*ww
        return yy
    def train(self, s_vec, t_vec):
        ;
