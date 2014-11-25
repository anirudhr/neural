#!/usr/bin/python2
#:indentSize=4:tabSize=4:noTabs=true:wrap=soft:

import numpy as np

def simple_transfer(x):
        if x > 0:
            return 1
        elif x < 0:
            return -1
        else:
            return 0

class BAM:
    def __init__(self, s_mat_list, t_mat_list): #s_mat_list, t_mat_list = list of np.matrix
        self.transfer = np.vectorize(simple_transfer) #transfer function
        self.setweight(s_mat_list, t_mat_list)
    def setweight(s_mat_list, t_mat_list):
        self.w_mat = np.empty([s_mat_list[0].shape[1], t_mat_list[0].shape[1]]) #will be filled with garbage values, will be same as using np.zeros() but marginally faster
        for s_mat, t_mat in zip(s_mat_list, t_mat_list):
            self.w_mat += s_mat.getT() * t_mat
    def inp_left(x_mat):
        return self.transfer(x_mat * self.w_mat)
    
    def inp_left(y_mat):
        return self.transfer(y_mat * self.w_mat.getT())
    
def translate_input(inputtxt): #converts a string such as '.##\n#..\n#..\n#..\n.##' into the input matrix
    return np.matrix(re.sub('#', '1 ',
                        re.sub('\.', '-1 ',
                            re.sub('\n', '; ', inputtxt)))).flatten()
                                
inp_c = """.##
#..
#..
#..
.##"""
t_c = np.matrix('-1 1 1')
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
t_x = np.matrix('1 -1 1')

inp_list = [translate_input(inp_c), translate_input(inp_d), translate_input(inp_x)]
out_list = [t_c, t_d, t_x]
