# -*- coding: utf-8 -*-
"""
Created on Wed Apr 04 23:06:59 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./../../../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


#Get the original 48 slots data
slot = 30
day_counter = 1
lux_original = []
slot_true = 1
lux = []
tmp = []
with open("./../../../NREL_data/20160901.csv", 'r') as f:
    fifthlines = itertools.islice(f, 0, None, slot)
    for lines in fifthlines:
        tmp.append(lines.split(',')[2])
        if(day_counter == (1440/slot)):
            day_counter = 0
            tmp = [w.replace('\n', '') for w in tmp]
            lux_original.append([float(i) for i in tmp])
            tmp = []            
        day_counter += 1

days = len(lux_original)

#split into 2 arrays
lux_B1 = []
lux_B2 = []
for x in range(len(lux_original)):
    even = lux_original[x][0:][::2]
    lux_B1.append(even)
    odd = lux_original[x][0:][::2]
    lux_B2.append(odd)
    
    
node1 = QLSEP_node(0.001,0.1,3,60,days,50)
node2 = QLSEP_node(0.001,0.1,3,60,days,50)

param = 0.3

for x in range(0,days):
    for y in range(0,1440/60):        
        node1.EWMA(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1.Q_val_update(x,y)

        
        node2.EWMA(x,y,lux_B2[x-1][y])
        node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
        
        """Now node 2 sends node 1 (PER_previous and the updated Q-val)"""
        """now target node checks the PER"""
        """if node2's PER > target node's PER"""
        ratio = param*safe_div(node1.PER_previous,node2.PER_previous)
        if(ratio>0.8):
            ratio = 0.8
        elif(ratio<0):
            ratio=0
        node1.q_values[y]=(0.8-ratio)*node2.q_values[y]+(0.2+ratio)*node1.q_values[y]
        #node1.q_values[y]=0.5*node1.q_values[y] + 0.5*node2.q_values[y]
        node1.QLSEP_prediction(x,y)
        
[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2,node2.EWMA_val,days)


print "==================================="
print "METHOD 4 - Sharing Q-Values (NREL)"
print "===================================\n"

print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)

print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)
