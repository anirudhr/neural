#!/usr/bin/python2

class classifier:
    def __init__(self, weights, threshold):
        self.weights = weights
        self.threshold = threshold
    def transfer(self, x):
        if x > self.threshold:
            return 1
        elif x < -1 * self.threshold:
            return -1
        else:
            return 0

