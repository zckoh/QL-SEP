# -*- coding: utf-8 -*-
"""
Created on Thu Apr 05 20:57:50 2018

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
    with open("./../../../Less Correlated/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../../../Less Correlated/Box 2/day%s.txt" %i , 'r') as f:
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
    
    
    

C = 0.2
W = 1.0

node1 = QLSEP_node(0.001,0.1,3,60,days,50)
node2 = QLSEP_node(0.001,0.1,3,60,days,50)

for x in range(0,days):
    for y in range(0,1440/60):        
        node1.EWMA(x,y,lux_B1_even[x-1][y])
        node1.Calculate_PER(x,y,lux_B1_even[x][y-1],(np.amax(lux_B1_even[x])*0.03))
        node1.Q_val_update(x,y)

        
        node2.EWMA(x,y,lux_B2_odd[x-1][y])
        node2.Calculate_PER(x,y,lux_B2_odd[x][y-1],(np.amax(lux_B2_odd[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
        
        """Now node 2 sends node 1 (PER_previous and the updated Q-val)"""
        """now target node calculates the ratio between the PERs"""
        ratio = C*safe_div(node1.PER_previous,node2.PER_previous)
        if(ratio>W):
            ratio = W
        elif(ratio<0):
            ratio=0
        node1.q_values[y]=(W-ratio)*node2.q_values[y]+((1-W)+ratio)*node1.q_values[y]
        #node1.q_values[y]=0.5*node1.q_values[y] + 0.5*node2.q_values[y]
        node1.QLSEP_prediction(x,y)
        
[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1_even,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1_even,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2_odd,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2_odd,node2.EWMA_val,days)


print "==================================="
print "METHOD 4 - Sharing Q-values (LCD)"
print "===================================\n"
print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)

print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)


print "Index = 14"
print node1.QLSEP_val[14]
# =============================================================================
# 
# index = 14
# 
# time24 = np.linspace(0,1440,num=1440/slot/2)
# 
# plt.figure(1)
# fig, ax = plt.subplots(figsize=(7,4))
# ax.plot(time24,lux_B1_even[index],'g',label= 'Actual')
# ax.plot(time24,node1.QLSEP_val[index],'b',label= 'QLSEP')
# 
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# plt.ylabel('Light Intensity (klux)')
# plt.xlabel('time (min)')
# plt.grid()
# 
# =============================================================================

