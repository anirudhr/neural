#!/usr/bin/python2

import numpy as np
import re
from random import shuffle

def rand_range(N):
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

s_mat_dict = {'C': inp_c, 'D': inp_d, 'S': inp_s, 'X': inp_x}
char_list = ['C', 'D', 'S', 'X']
NUM_ITER = 10
for i in xrange(NUM_ITER):
    s_mat_list = list()
    shuffle(char_list)
    for j in char_list:
        s_mat_list.append(s_mat_dict[j])
    hopfield = DiscreteHopfieldNet(s_mat_list)
    outs = dict()
    for j in rand_range(4):
        outs[char_list[j]] = hopfield.inp(s_mat_dict[char_list[j]])
    print "Iteration ", i
    for char, s_mat in s_mat_dict.iteritems():
        for j in char_list:
            match_flag = False
            if (outs[j] == s_mat).all():
                match_flag = match_flag or True
                print "\tOutput pattern", outs[j] , " for ", j, "matches character ", char,
                if j == char:
                    print "(stable)" 
                else:
                    print "(spurious)" 
            if not match_flag:
                print "\t No match in output pattern", outs[j] , "for ", j
#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:

"""
OUTPUT
$ python hopfield.py 
Iteration  0
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1  1  1 -1 -1 -1  1 -1 -1 -1 -1 -1  1  1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[ 1  1 -1  1 -1  1  1  1  1  1  1  1  1  1 -1]] for  D
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1  1  1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1  1  1 -1 -1 -1  1 -1 -1 -1 -1 -1  1  1 -1]] for  S
         No match in output pattern [[ 1  1 -1  1 -1  1  1  1  1  1  1  1  1  1 -1]] for  D
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1  1  1]] for  C
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1  1  1 -1 -1 -1  1 -1 -1 -1 -1 -1  1  1 -1]] for  S
         No match in output pattern [[ 1  1 -1  1 -1  1  1  1  1  1  1  1  1  1 -1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1  1  1]]  for  C matches character  C (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1  1  1 -1 -1 -1  1 -1 -1 -1 -1 -1  1  1 -1]] for  S
        Output pattern [[ 1  1 -1  1 -1  1  1  1  1  1  1  1  1  1 -1]]  for  D matches character  D (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1  1  1]] for  C
Iteration  1
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
Iteration  2
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
Iteration  3
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
Iteration  4
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
Iteration  5
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
Iteration  6
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
Iteration  7
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
Iteration  8
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
Iteration  9
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  S (spurious)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  S (stable)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  X (spurious)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  X (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  C matches character  C (stable)
        Output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]]  for  S matches character  C (spurious)
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  D
         No match in output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]] for  X
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  C
         No match in output pattern [[-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1]] for  S
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  D matches character  D (stable)
        Output pattern [[1 1 1 1 1 1 1 1 1 1 1 1 1 1 1]]  for  X matches character  D (spurious)

1: Yes, all 4 stored patterns are equilibrium states.
2: 

"""
