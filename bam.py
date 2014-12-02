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
def simple_transfer(xin, x):
    return (xin/abs(xin)) if xin else x
    
class BAM:
    def __init__(self, s_mat_list, t_mat_list): #s_mat_list, t_mat_list = list of np.matrix
        self.transfer = np.vectorize(simple_transfer) #transfer function
        self.setweight(s_mat_list, t_mat_list)
    def setweight(self, s_mat_list, t_mat_list):
        self.w_mat = np.matrix(np.zeros([s_mat_list[0].shape[1], t_mat_list[0].shape[1]]))
        for s_mat, t_mat in zip(s_mat_list, t_mat_list):
            self.w_mat += s_mat.getT() * t_mat
    def inp_left(self, x_mat):
        firstrun_flag = True
        convergence_flag = False
        while not convergence_flag:
            yin = x_mat * self.w_mat
            if firstrun_flag:
                y = np.matrix(np.zeros([yin.shape[1]]))
            yold = y
            y = self.transfer(yin, y)
            xin = y * self.w_mat.getT()
            if firstrun_flag:
                x = np.matrix(np.zeros([xin.shape[1]]))
                firstrun_flag = False
            xold = x
            x = self.transfer(xin, x)
            ydiff = list(np.array(y-yold).reshape(-1,))
            xdiff = list(np.array(x-xold).reshape(-1,))
            convergence_flag = True
            for i,j in zip(ydiff, xdiff):
                if i or j:
                    convergence_flag = False
                    #print 'Not converged'
        return y
    
    def inp_right(self, y_mat):
        firstrun_flag = True
        convergence_flag = False
        while not convergence_flag:
            xin = y_mat * self.w_mat.getT()
            if firstrun_flag:
                x = np.matrix(np.zeros([xin.shape[1]]))
            xold = x
            x = self.transfer(xin, x)
            yin = x * self.w_mat#.getT()
            if firstrun_flag:
                y = np.matrix(np.zeros([yin.shape[1]]))
                firstrun_flag = False
            yold = y
            y = self.transfer(yin, y)
            xdiff = list(np.array(y-yold).reshape(-1,))
            ydiff = list(np.array(x-xold).reshape(-1,))
            convergence_flag = True
            for i,j in zip(xdiff, ydiff):
                if i or j:
                    convergence_flag = False
                    #print 'Not converged'
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
#..
#..
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
$ ./bam.py 
Clean input from left:
[[-1.  1.  1.]]
Noisy input from left:
[[ 1. -1.  1.]]
Mistake-containing input from left:
[[-1.  1.  1.]]
Clean input from right:
[[-1.  1.  1.  1. -1. -1.  1. -1. -1.  1. -1. -1. -1.  1.  1.]]
Mistake-containing input from right:
[[-1.  1. -1. -1.  1. -1.  1. -1.  1. -1.  1. -1. -1.  1. -1.]]
Noisy input from right:
[[-1. -1.  1. -1.  1. -1. -1.  1. -1. -1.  1. -1. -1. -1.  1.]]
"""
