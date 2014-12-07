#!/usr/bin/python2
#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:

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
    
class DiscreteHopfieldNet:
    def __init__(self, s_mat_list): #s_mat_list = list of np.matrix
        self.N = s_mat_list[0].shape[1]
        self.Q = len(s_mat_list)
        self.setweights(s_mat_list)
        self.y = np.matrix(np.zeros([self.N]))
    def transfer(xin, x):
        return (xin/abs(xin)) if xin else x
    def setweights(self, s_mat_list):
        self.w_mat = np.matrix(np.zeros([self.N, self.N]))
        for i in xrange(self.N):
            for j in xrange(self.N):
                if i != j:
                    for s_mat_q in s_mat_list:
                        self.w_mat[i,j] += s_mat_q[0,i] * s_mat_q[0,j]
        print "Weight: "
        print self.w_mat

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
