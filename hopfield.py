#!/usr/bin/python2

import numpy as np
import re
"""
def simple_transfer(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return x
"""

def rand_range(N):
    from random import shuffle
    x = [i for i in range(N)]
    shuffle(x)
    return x
    
def transfer(xin, x):
    return (xin/abs(xin)) if xin else x
    
class DiscreteHopfieldNet:
    def __init__(self, s_mat_list): #s_mat_list = list of np.matrix
        self.N = s_mat_list[0].shape[1]
        self.Q = len(s_mat_list)
        self.setweights(s_mat_list)
        self.y = np.matrix(np.zeros([self.N]))
        
    def setweights(self, s_mat_list):
        self.w_mat = np.matrix(np.zeros([self.N, self.N]))
        for i in xrange(self.N):
            for j in xrange(i+1, self.N):
                if i != j:
                    for s_mat_q in s_mat_list:
                        self.w_mat[i,j] += s_mat_q[0,i] * s_mat_q[0,j]
                    self.w_mat[j,i] = self.w_mat[i,j]
        #print "Weight: "; print self.w_mat
    def inp(self, x_mat):
        y_mat = x_mat
        yold_mat = np.matrix(np.zeros([self.N]))
        while np.count_nonzero(y_mat - yold_mat):
            yold_mat = y_mat
            i_list = rand_range(self.N)
            yin = np.matrix(np.zeros([self.N]))
            inp_other_neurons = 0
            for i in i_list:
                for j in xrange(self.N):
                    if j == i:
                        continue
                    inp_other_neurons += y_mat[0, j] * self.w_mat[j,i]
                yin[0,i] = x_mat[0,i] + inp_other_neurons
                y_mat[0,i] = transfer(yin[0,i], y_mat[0,i])
        return y_mat

def translate_input(inputtxt): #converts a string such as '.##\n#..\n#..\n#..\n.##' into the input matrix
    return np.matrix(re.sub('#', '1 ',
                        re.sub('\.', '-1 ',
                            re.sub('\n', '; ', inputtxt)))).flatten()

inp_c = translate_input(""".##
#..
#..
#..
.##""")
inp_d = translate_input("""##.
#.#
#.#
#.#
##.""")
inp_s = translate_input(""".##
#..
.#.
..#
##.""")
inp_x = translate_input("""#.#
#.#
.#.
#.#
#.#""")

s_mat_list = [inp_c, inp_d, inp_s, inp_x]
#s_mat_list = [np.matrix([1, 1, 1, -1]), np.matrix([1, -1, 1, 1])]
hopfield = DiscreteHopfieldNet(s_mat_list)
print hopfield.inp(inp_c)
