#!/usr/bin/python2
#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:

import numpy as np
import re

def simple_transfer(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return x

class BAM: #need to test for convergence.
#biases for Y-layer (input left) are b_j^Y = sum_q=1toQ(t_j^q)
#biases for X-layer (input right) are b_i^X = sum_q=1toQ(s_i^q)
    def __init__(self, s_mat_list, t_mat_list): #s_mat_list, t_mat_list = list of np.matrix
        self.transfer = np.vectorize(simple_transfer) #transfer function
        self.setweight(s_mat_list, t_mat_list)
        self.biasY = np.matrix(np.zeros([t_mat_list[0].shape[1]]))
        for t_mat in t_mat_list:
            self.biasY = self.biasY + t_mat
        self.biasX = np.matrix(np.zeros([s_mat_list[0].shape[1]]))
        for s_mat in s_mat_list:
            self.biasX = self.biasX + s_mat
            
    def setweight(self, s_mat_list, t_mat_list):
        self.w_mat = np.matrix(np.zeros([s_mat_list[0].shape[1], t_mat_list[0].shape[1]]))
        for s_mat, t_mat in zip(s_mat_list, t_mat_list):
            self.w_mat += s_mat.getT() * t_mat
            
    def inp_left(self, x_mat):
        yin = x_mat * self.w_mat + biasY
        y = self.transfer(yin)
        #test for convergence, else repeat this.
        return y
    
    def inp_right(self, y_mat):
        xin = y_mat * self.w_mat.getT() + biasX
        x = self.transfer(xin)
        #test for convergence, else repeat this.
        return x
    
def translate_input(inputtxt): #converts a string such as '.##\n#..\n#..\n#..\n.##' into the input matrix
    return np.matrix(re.sub('#', '1 ',
                        re.sub('\.', '-1 ',
                            re.sub('\n', '; ', inputtxt)))).flatten()
                                
inp_c = """.##
#..
#..
#..
.##"""
inp_c_mistake = """.##
.#.
.#.
.#.
.##"""
t_c = np.matrix('-1 1 1')
t_c_mistake = np.matrix('-1 -1 1')
inp_d = """##.
#.#
#.#
#.#
##."""
t_d = np.matrix('1 -1 1')
inp_x = """#.#
#.#
.#.
#.#
#.#"""
t_x = np.matrix('1 1 -1')

inp_list = [translate_input(inp_c), translate_input(inp_d), translate_input(inp_x)]
out_list = [t_c, t_d, t_x]

bam_cdx = BAM(inp_list, out_list)
#print bam_cdx.w_mat
print "Clean input from left:"
print bam_cdx.inp_left(translate_input(inp_c))
print "Noisy input from left:"
print bam_cdx.inp_left(np.matrix('0 1 0 1 0 1 0 1 0 1 0 1 0 1 0'))
print "Mistake-containing input from left:"
print bam_cdx.inp_left(translate_input(inp_c_mistake))

print "Clean input from right:"
print bam_cdx.inp_right(t_c)
print "Mistake-containing input from right:"
print bam_cdx.inp_right(t_c_mistake)
print "Noisy input from right:"
print bam_cdx.inp_right(np.matrix('-1 1 -1'))

"""
Output:
$ python bam.py 
Clean input from left:
[[-1  1  1]]
Noisy input from left:
[[ 1 -1  1]]
Mistake-containing input from left:
[[-1  1 -1]]
Clean input from right:
[[-1  1  1  1 -1 -1  1 -1 -1  1 -1 -1 -1  1  1]]
Mistake-containing input from right:
[[-1  1 -1 -1  1 -1  1 -1  1 -1  1 -1 -1  1 -1]]
Noisy input from right:
[[-1 -1  1 -1  1 -1 -1  1 -1 -1  1 -1 -1 -1  1]]
"""