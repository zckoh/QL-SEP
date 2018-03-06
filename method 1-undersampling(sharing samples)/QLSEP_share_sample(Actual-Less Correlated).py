# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 10:32:50 2018

Method 1: Sharing actual sample between nodes
(Actual collected data)
less correlated data

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


#Get the original 48 slots data
tmp = []
lux_B1 = []
slot = 30
"""getting data"""
for i in range(1,21):
    with open("./../Less Correlated/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../Less Correlated/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

days = len(lux_B1)



#Split the samples into each sample for the box is 60min apart
lux_B1_even = []
lux_B2_odd = []
for x in range(len(lux_B1)):
    even = lux_B1[x][0:][::2]
    lux_B1_even.append(even)
    odd = lux_B2[x][1::][::2]
    lux_B2_odd.append(odd)



#Lux_shared = [box1,box2,box1,box2...]
lux_shared = []
for x in range(0,days):
    lux_shared.append([item for pair in zip(lux_B1_even[x], lux_B2_odd[x]) for item in pair])


#each node will have 48 slots as it combines 24 + 24 of sampled data
node1 = QLSEP_node(0.003,0.4,3,30,days,50)
node2 = QLSEP_node(0.003,0.4,3,30,days,50)
for x in range(0,days):
    for y in range(0,1440/30):
        node1.EWMA(x,y,lux_shared[x-1][y])
        node1.Calculate_PER(x,y,lux_shared[x][y-1],(np.amax(lux_shared[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        
        node2.EWMA(x,y,lux_shared[x-1][y])
        node2.Calculate_PER(x,y,lux_shared[x][y-1],(np.amax(lux_shared[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)


[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2,node2.EWMA_val,days)


print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)


print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)

