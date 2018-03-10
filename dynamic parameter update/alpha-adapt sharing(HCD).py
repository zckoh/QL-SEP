# -*- coding: utf-8 -*-
"""
Created on Sat Mar 10 10:15:14 2018

alpha-adapt EWMA (Sharing)
sharing occurs every slot
Node 2 share to node 1 (target)

Weighted average of all nearby nodes
Only have 1 target node instead of all trying to help each other

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
slot = 60
"""getting data"""
for i in range(1,21):
    with open("./../highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

days = len(lux_B1)

node1 = QLSEP_node(0.003,0.4,3,slot,days,50)
node2 = QLSEP_node(0.003,0.4,3,slot,days,50)

n1_alpha = []
n2_alpha = []


for x in range(0,days):
    for y in range(0,1440/slot):
        #Node1 updates its alpha & predicts for next slot
        node1.alpha_adapt(x,y,(np.amax(lux_B1[x])*0.03),lux_B1[x][y-1])
        
        #now share to node 1 and find the change in prediction
        node1.a2 = 0.5*node2.a2 + 0.5*node1.a2
        node1.EWMA_dynamic(x,y,lux_B1[x-1][y])
        n1_alpha.append(node1.a2)
        n2_alpha.append(node2.a2)
        #Node2 updates its alpha & predicts for next slot
        node2.alpha_adapt(x,y,(np.amax(lux_B2[x])*0.03),lux_B2[x][y-1])
        
        #now share to node 2 and find the change in prediction
        #node2.a2 = 0.5*node2.a2 + 0.5*node1.a2
        node2.EWMA_dynamic(x,y,lux_B2[x-1][y])
        

        
[mape_b1,no_b1] = MAPE_overall(lux_B1,node1.EWMA_val,days)
[mape_b2,no_b2] = MAPE_overall(lux_B2,node2.EWMA_val,days)



print "24 slots"
print "===================EWMA (sharing)=====================\n"
print "MAPE = %s%% , N = %s (box1)" % (mape_b1,no_b1)
print "MAPE = %s%% , N = %s (box2)\n" % (mape_b2,no_b2)


# =============================================================================
# no = 0
# for no in range(len(n1_alpha)):
#     print "%s %s " %(n1_alpha[no],n2_alpha[no])
# 
# =============================================================================
time = np.linspace(1,1440*days, num = 1440*days/slot)


plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,n1_alpha,'r',label='Box 1')
ax.plot(time,n2_alpha,'b',label= 'Box 2')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel(r'$\alpha$')
plt.grid()
plt.title(r'How $\alpha$ varies w.r.t time')


