# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 15:48:25 2018

Dynamic update for local EWMA prediction model + QLSEP
Alpha adapt


@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


#Get the original 48 slots data
slot = 30
day_counter = 1
lux_original = []
slot_true = 1
lux = []
tmp = []
with open("./../NREL_data/20160901.csv", 'r') as f:
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
    odd = lux_original[x][1::][::2]
    lux_B2.append(odd)


node1 = QLSEP_node(0.003,0.4,3,60,days,50)
node2 = QLSEP_node(0.003,0.4,3,60,days,50)

for x in range(0,days):
    for y in range(0,1440/slot/2):
        
        #Node 1 uses static parameter
        node1.alpha_adapt(x,y,(np.amax(lux_B1[x])*0.03),lux_B1[x][y-1])
        node1.EWMA_dynamic(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        #Node 2 uses alpha-adapt algorithm
        #Calculate the PER of the last slot
        node2.alpha_adapt(x,y,(np.amax(lux_B2[x])*0.03),lux_B2[x][y-1])
        node2.EWMA_dynamic(x,y,lux_B2[x-1][y])
        PER = node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
        

[mape_static,no_static] = MAPE_overall(lux_B1,node1.EWMA_val,days)
[mape_dynamic,no_dynamic] = MAPE_overall(lux_B2,node2.EWMA_val,days)



print "24 slots"
print "===================EWMA=====================\n"
print "MAPE = %s%% , N = %s (box1)" % (mape_static,no_static)
print "MAPE = %s%% , N = %s (box2)\n" % (mape_dynamic,no_dynamic)



[mape_static,no_static] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_dynamic,no_dynamic] = MAPE_overall(lux_B2,node2.QLSEP_val,days)

print "===================QLSEP=====================\n"
print "MAPE = %s%% , N = %s (box1)" % (mape_static,no_static)
print "MAPE = %s%% , N = %s (box2)" % (mape_dynamic,no_dynamic)


