#!/usr/bin/python2

import sys

#16 different binary logic functions: http://en.wikipedia.org/wiki/Boolean_algebras_canonically_defined#Truth_tables
#x0	x1	2f0	2f1	2f2	2f3	2f4	2f5	2f6	2f7	2f8	2f9	2f10	2f11	2f12	2f13	2f14	2f15
#-1	-1	-1	+1	-1	+1	-1	+1	-1	+1	-1	+1	-1	+1	-1	+1	-1	+1
#+1	-1	-1	-1	+1	+1	-1	-1	+1	+1	-1	-1	+1	+1	-1	-1	+1	+1
#-1	+1	-1	-1	-1	-1	+1	+1	+1	+1	-1	-1	-1	-1	+1	+1	+1	+1
#+1	+1	-1	-1	-1	-1	-1	-1	-1	-1	+1	+1	+1	+1	+1	+1	+1	+1

# To check if problem is linearly separable, check if b + x.w = 0. But can this be programmed?

# Algorithm to generate w, b (n = number of input components = 2 for this):
# 0. wi = 0 for i = 1 to n
# 1. for v_s, v_t in zip(vlist_s, vlist_t):
# 2.	xi = v_s[i] for i = 1 to n
# 3.	y = t
# 4.	wi = wi + xi*y for i = 1 to n
# 5.	b = b + y

# To check Hebb rule -generated weight and bias validity, t == x.w + b for each training set

x0 = [-1, 1, -1, 1]
x1 = [-1, -1, 1, 1]
f0 = [-1, -1, -1, -1]
f1 = [1, -1, -1, -1]
f2 = [-1, 1, -1, -1]
f3 = [1, 1, -1, -1]
f4 = [-1, -1, 1, -1]
f5 = [1, -1, 1, -1]
f6 = [-1, 1, 1, -1]
f7 = [1, 1, 1, -1]
f8 = [-1, -1, -1, 1]
f9 = [1, -1, -1, 1]
f10 = [-1, 1, -1, 1]
f11 = [1, 1, -1, 1]
f12 = [-1, -1, 1, 1]
f13 = [1, -1, 1, 1]
f14 = [-1, 1, 1, 1]
f15 = [1, 1, 1, 1]

f_list = [f0,f1,f2,f3,f4,f5,f7,f8,f10,f11,f12,f13,f14,f15] #not including f6 and f9 because they are not linearly separable.

if len(sys.argv) != 2:
    print 'Usage: hebb.py plot|calc'
    exit()

if str(sys.argv[1]) == 'calc':
    def calcWeightsBiasByHebb(x0, x1, t_list):
        w0_list = list()
        w1_list = list()
        b_list = list()
        for which_fun, t_val in enumerate(t_list):
            w0_val = 0
            w1_val = 0
            b_val = 0
            for ii, tt in enumerate(t_val):
                w0_val += x0[ii] * tt
                w1_val += x1[ii] * tt
                b_val += tt
            print 'For 2f%s' % which_fun
            print '          w0 = ', w0_val, ', w1 = ', w1_val, ', b = ', b_val
            w0_list.append(w0_val)
            w1_list.append(w1_val)
            b_list.append(b_val)
        return w0_list, w1_list, b_list
    
    w0, w1, b = calcWeightsBiasByHebb(x0, x1, f_list)
    
    ####verification code

elif str(sys.argv[1]) == 'plot':
    import matplotlib.pyplot as plt
    
    def plotToPng(t_list):
        for ii, t_val in enumerate(t_list):
            plt.clf()
            plt.axis([-3, 3, -3, 3])
            plt.grid()
            for jj in xrange(0, 4):
                x = x0[jj]
                y = x1[jj]
                if t_val[jj] == -1:
                    plt.plot(x, y, 'ro')
                    #print str((x, y)), ' is a neg'
                else:
                    plt.plot(x, y, 'bo')
                    #print str((x, y)), ' is a pos'
            plt.savefig('res_2f' + str(ii) + '.png', bbox_inches='tight')
    plotToPng(f_list)
else:
    print 'Usage: hebb.py plot|calc'
