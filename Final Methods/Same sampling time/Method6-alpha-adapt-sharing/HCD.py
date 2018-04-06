# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 23:15:32 2018

@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./../../../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


#Get the original 48 slots data
tmp = []
lux_B1 = []
slot = 30
"""getting data"""
for i in range(1,21):
    with open("./../../../highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../../../highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

days = len(lux_B1)


#split into 2 arrays  (Box 1)
lux_B1_even = []
lux_B2_odd = []
for x in range(len(lux_B1)):
    even = lux_B1[x][0:][::2]
    lux_B1_even.append(even)
    odd = lux_B2[x][0:][::2]
    lux_B2_odd.append(odd)


node1 = QLSEP_node(0.001,0.1,3,60,days,50)
node2 = QLSEP_node(0.001,0.1,3,60,days,50)


n1_alpha = []
n2_alpha = []

param = 0.3

for x in range(0,days):
    for y in range(0,1440/60):
        #Node1 updates its alpha & predicts for next slot
        node1.alpha_adapt(x,y,(np.amax(lux_B1_even[x])*0.03),lux_B1_even[x][y-1])
        node1.Calculate_PER(x,y,lux_B1_even[x][y-1],(np.amax(lux_B1_even[x])*0.03))
        #now share to node 1 and find the change in prediction
        #node1.a2 = 0.5*node2.a2 + 0.5*node1.a2
        
        ratio = param*safe_div(node1.PER_previous,node2.PER_previous)
        if(ratio>0.8):
            ratio = 0.8
        elif(ratio<0):
            ratio=0
        node1.a2=(0.8-ratio)*node2.a2+(0.2+ratio)*node1.a2

        node1.EWMA_dynamic(x,y,lux_B1_even[x-1][y])
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        
        
        n1_alpha.append(node1.a2)
        n2_alpha.append(node2.a2)
        #Node2 updates its alpha & predicts for next slot
        node2.alpha_adapt(x,y,(np.amax(lux_B2_odd[x])*0.03),lux_B2_odd[x][y-1])
        
        #now share to node 2 and find the change in prediction
        #node2.a2 = 0.5*node2.a2 + 0.5*node1.a2
        node2.EWMA_dynamic(x,y,lux_B2_odd[x-1][y])
        node2.Calculate_PER(x,y,lux_B2_odd[x][y-1],(np.amax(lux_B2_odd[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
        

[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1_even,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1_even,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2_odd,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2_odd,node2.EWMA_val,days)


print "==================================="
print "METHOD 6 - Alpha-adapt Sharing (HCD)"
print "===================================\n"

print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)

print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)