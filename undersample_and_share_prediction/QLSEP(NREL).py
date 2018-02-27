# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 14:27:00 2018
(USING QLSEP)
2 24 slots profile predicting individually, 
and sharing its prediction to build up a higher resolution profile.


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
    
"""New model"""
#EWMA_val_shared = np.array([[float(0)]*(1440/slot)]*days)
EWMA_val_shared = []
QLSEP_val_shared = []


"""
node1 = QLSEP_node(0.003,0.4,3,60,days,50)
node2 = QLSEP_node(0.003,0.4,3,60,days,50)
for x in range(0,days):
    for y in range(0,1440/60):
        node1.EWMA(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        
        node2.EWMA(x,y,lux_B2[x-1][y])
        node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)
"""
    
node1 = QLSEP_node(0.003,0.4,3,30,days,50)
node2 = QLSEP_node(0.003,0.4,3,30,days,50)
for x in range(0,days):
    for y in range(0,1440/30):
        if(y%2==0):
            print "n1"
            #every 0 2 4 6 8
            #Node 1 sameples + predicts
            #Sends Node 2 its prediction to be used
            #receives Node 2 EWMA_value for the previous slot to use in EWMA calculation
            node1.EWMA_share(x,y,lux_B1[x-1][y],node2.EWMA_val[x][y-1])
            node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
            node1.Q_val_update(x,y)
            node1.QLSEP_prediction(x,y)
            
        else:
            print "n2"
            #Every 1 3 5 7 9 
            #Nodoe 2 predicts
            #sends node 1 its prediction to be used
            #recevies node 1 EWMA-value for the previous slot to use in EWMA calculation
            node2.EWMA_share(x,y,lux_B2[x-1][y],node1.EWMA_val[x][y-1])
            node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
            node2.Q_val_update(x,y)
            node2.QLSEP_prediction(x,y)
            
node_original = QLSEP_node(0.001,0.4,3,30,days,50)
for x in range(0,days):
    for y in range(0,1440/30):
        node_original.EWMA(x,y,lux_original[x-1][y])
        node_original.Calculate_PER(x,y,lux_original[x][y-1],(np.amax(lux_original[x])*0.03))
        node_original.Q_val_update(x,y)
        node_original.QLSEP_prediction(x,y)

for x in range(0,days):
    EWMA_val_shared.append([item for pair in zip(node1.EWMA_val[x], node2.EWMA_val[x]) for item in pair])
    QLSEP_val_shared.append([item for pair in zip(node1.QLSEP_val[x], node2.QLSEP_val[x]) for item in pair])

[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2,node2.EWMA_val,days)


[mape_shared_QLSEP, no_shared_QLSEP] = MAPE_overall(lux_original,QLSEP_val_shared,days)
[mape_shared_EWMA, no_shared_EWMA] = MAPE_overall(lux_original,EWMA_val_shared,days)

[mape_original_QLSEP, no_original_QLSEP] = MAPE_overall(lux_original, node_original.QLSEP_val,days)
[mape_original_EWMA, no_original_EWMA] = MAPE_overall(lux_original, node_original.EWMA_val,days)


print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)
print "MAPE = %s%% , N = %s (shared)" % (mape_shared_EWMA,no_shared_EWMA)
print "MAPE = %s%% , N = %s (original)\n" % (mape_original_EWMA,no_shared_EWMA)

print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)
print "MAPE = %s%% , N = %s (shared)" % (mape_shared_QLSEP,no_shared_QLSEP)
print "MAPE = %s%% , N = %s (original)\n" % (mape_original_QLSEP,no_original_QLSEP)



#plot the proifles


time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 79  
plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,QLSEP_val_shared[index],'r',label = 'shared')
ax.plot(time48,node_original.QLSEP_val[index],'b',label = 'original')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Box day %s (NREL data)' % str(index+1))
plt.grid()
plt.show()
