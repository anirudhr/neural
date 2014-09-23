#!/usr/bin/python2

import sys

#16 different binary logic functions: http://en.wikipedia.org/wiki/Boolean_algebras_canonically_defined#Truth_tables
#x0_v	x1_v	2f0	2f1	2f2	2f3	2f4	2f5	2f6	2f7	2f8	2f9	2f10	2f11	2f12	2f13	2f14	2f15
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

# To check Hebb rule -generated weight and bias validity, t = 1 ? x.w + b > 0 : 0 for each training set

x0_v = [-1, 1, -1, 1]
x1_v = [-1, -1, 1, 1]
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
    def calcWeightsBiasByHebb(x0_v, x1_v, t_list):
        w0_list = list()
        w1_list = list()
        b_list = list()
        for which_fun, t_val in enumerate(t_list):
            w0_val = 0
            w1_val = 0
            b_val = 0
            for ii, tt in enumerate(t_val):
                w0_val += x0_v[ii] * tt
                w1_val += x1_v[ii] * tt
                b_val += tt
            #START CODE SKIPPING 2f6 and 2f9
            if which_fun >= 6:
                which_fun += 1
            if which_fun >= 9:
                which_fun += 1
            #END CODE SKIPPING 2f6 and 2f9
            print 'For 2f%s' % which_fun
            print '          w0 = ', w0_val, ', w1 = ', w1_val, ', b = ', b_val
            w0_list.append(w0_val)
            w1_list.append(w1_val)
            b_list.append(b_val)
        return w0_list, w1_list, b_list
    
    ####verification code
    def verifyHebb(w0_vl, w1_vl, b_vl, x0_v, x1_v, t_list):
        for ii, t_l, w0, w1, b in zip(range(len(t_list)), t_list, w0_vl, w1_vl, b_vl):
            y = 0
            y_l = list()
            f = True
            for jj, x0, x1 in zip(range(len(x0_v)), x0_v, x1_v):
                y = x0*w0 + x1*w1 + b
                y_l.append(y)
                if (y <= 0 and t_l[jj] == 1) or (y > 0 and t_l[jj] == 0):
                    f = False
            #START CODE SKIPPING 2f6 and 2f9
            if ii >= 6:
                ii += 1
            if ii >= 9:
                ii += 1
            #END CODE SKIPPING 2f6 and 2f9
            if f:
                print 'correct, 2f%s' % ii,
                print '\t||| y vals: %s' % str(y_l),
                print '\t||| t vals: %s' % str(t_l)
            else:
                print 'incorrect, 2f%s' % ii,
                print '\t||| y vals: %s' % str(y_l),
                print '\t||| t vals: %s' % str(t_l)

    w0_vl, w1_vl, b_vl = calcWeightsBiasByHebb(x0_v, x1_v, f_list)
    verifyHebb(w0_vl, w1_vl, b_vl, x0_v, x1_v, f_list)

elif str(sys.argv[1]) == 'plot':
    import matplotlib.pyplot as plt
    
    def plotToPng(t_list):
        for ii, t_val in enumerate(t_list):
            plt.clf()
            plt.axis([-3, 3, -3, 3])
            plt.grid()
            for jj in xrange(0, 4):
                x = x0_v[jj]
                y = x1_v[jj]
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
    
####################CODE OUTPUT####################
# For 2f0
          # w0 =  0 , w1 =  0 , b =  -4
# For 2f1
          # w0 =  -2 , w1 =  -2 , b =  -2
# For 2f2
          # w0 =  2 , w1 =  -2 , b =  -2
# For 2f3
          # w0 =  0 , w1 =  -4 , b =  0
# For 2f4
          # w0 =  -2 , w1 =  2 , b =  -2
# For 2f5
          # w0 =  -4 , w1 =  0 , b =  0
# For 2f7
          # w0 =  -2 , w1 =  -2 , b =  2
# For 2f8
          # w0 =  2 , w1 =  2 , b =  -2
# For 2f10
          # w0 =  4 , w1 =  0 , b =  0
# For 2f11
          # w0 =  2 , w1 =  -2 , b =  2
# For 2f12
          # w0 =  0 , w1 =  4 , b =  0
# For 2f13
          # w0 =  -2 , w1 =  2 , b =  2
# For 2f14
          # w0 =  2 , w1 =  2 , b =  2
# For 2f15
          # w0 =  0 , w1 =  0 , b =  4
# correct, 2f0 		||| y vals: [-4, -4, -4, -4] 	||| t vals: [-1, -1, -1, -1]
# correct, 2f1 		||| y vals: [2, -2, -2, -6] 	||| t vals: [1, -1, -1, -1]
# correct, 2f2 		||| y vals: [-2, 2, -6, -2] 	||| t vals: [-1, 1, -1, -1]
# correct, 2f3 		||| y vals: [4, 4, -4, -4] 	||| t vals: [1, 1, -1, -1]
# correct, 2f4 		||| y vals: [-2, -6, 2, -2] 	||| t vals: [-1, -1, 1, -1]
# correct, 2f5 		||| y vals: [4, -4, 4, -4] 	||| t vals: [1, -1, 1, -1]
# correct, 2f7 		||| y vals: [6, 2, 2, -2] 	||| t vals: [1, 1, 1, -1]
# correct, 2f8	 	||| y vals: [-6, -2, -2, 2] 	||| t vals: [-1, -1, -1, 1]
# correct, 2f10 	||| y vals: [-4, 4, -4, 4] 	||| t vals: [-1, 1, -1, 1]
# correct, 2f11 	||| y vals: [2, 6, -2, 2] 	||| t vals: [1, 1, -1, 1]
# correct, 2f12 	||| y vals: [-4, -4, 4, 4] 	||| t vals: [-1, -1, 1, 1]
# correct, 2f13 	||| y vals: [2, -2, 6, 2] 	||| t vals: [1, -1, 1, 1]
# correct, 2f14 	||| y vals: [-2, 2, 2, 6] 	||| t vals: [-1, 1, 1, 1]
# correct, 2f15 	||| y vals: [4, 4, 4, 4] 	||| t vals: [1, 1, 1, 1]
