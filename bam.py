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
    def __init__(self, s_vec_list, t_vec_list): #s_vec_list, t_vec_list = list of np.matrix
        self.w_mat = np.empty([s_vec_list[0].shape[1], t_vec_list[0].shape[1]]) #will be filled with garbage values, will be same as using np.zeros() but marginally faster
        for s_vec, t_vec in zip(s_vec_list, t_vec_list):
            self.w_mat += s_vec.getT() * t_vec
        self.transfer = np.vectorize(simple_transfer)
    def inp_left(x_vec):
        pass
    def inp_left(y_vec):
        pass
