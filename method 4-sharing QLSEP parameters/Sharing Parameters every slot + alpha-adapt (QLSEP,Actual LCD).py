# -*- coding: utf-8 -*-
"""
Created on Mon Mar 12 12:18:21 2018

QLSEP model (With 1 node sharing to the other every slot)
(Actual LCD Data)
+
Alpha - adapt

@author: zckoh
"""



import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)
execfile("./../QLSEP_class.py")

index = 18

#Importing True values collected from both boxes(Samples per Min)
tmp = []
lux_B1 = []
slot = 60

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

"""(learning_rate, alpha, N, Min per slot, days, checking_slot)"""
node1 = QLSEP_node(0.003,0.4,3,slot,days,50)
node2 = QLSEP_node(0.003,0.4,3,slot,days,50)

n1_q_val = []
n2_q_val = []

for x in range(0,days):
    for y in range(0,1440/slot):
        """Node 1 predicting"""
        node1.alpha_adapt(x,y,(np.amax(lux_B1[x])*0.03),lux_B1[x][y-1])
        node1.a2 = 0.3*node2.a2 + 0.7*node1.a2
        node1.EWMA_dynamic(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
       
        
        """Node 2 predicting"""
        node2.alpha_adapt(x,y,(np.amax(lux_B2[x])*0.03),lux_B2[x][y-1])
        node2.EWMA_dynamic(x,y,lux_B2[x-1][y])
        node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
        
        #Node 2 share to node 1
        #node1.q_values[y] = 0.3*node1.q_values[y] + 0.7*node2.q_values[y]
        if(y==12):
            n1_q_val.append(node1.q_values[y])
            n2_q_val.append(node2.q_values[y])


[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2,node2.EWMA_val,days)



print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_EWMA,no_b2_EWMA)


print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_QLSEP,no_b2_QLSEP)

time = np.linspace(1,len(n1_q_val), num = len(n1_q_val))


plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,n1_q_val,'r',label='Box 1')
ax.plot(time,n2_q_val,'b',label= 'Box 2')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel(r'Q')
plt.grid()
plt.title(r'How Q-value varies w.r.t time (slot 12)')
