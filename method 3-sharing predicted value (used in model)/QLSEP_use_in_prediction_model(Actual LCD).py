# -*- coding: utf-8 -*-
"""
Created on Tue Mar 06 15:12:18 2018

Method 3: Share predicton values (use it in prediction model)
(Actual Collected Data) - 20 days
Less correlated data



@author: zckoh
"""
    
#Get the original 48 slots data
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


#split into 2 arrays  (Box 1)
lux_B1_even = []
lux_B2_odd = []
for x in range(len(lux_B1)):
    even = lux_B1[x][0:][::2]
    lux_B1_even.append(even)
    odd = lux_B2[x][1::][::2]
    lux_B2_odd.append(odd)

"""New model"""
#EWMA_val_shared = np.array([[float(0)]*(1440/slot)]*days)
EWMA_val_shared = []
QLSEP_val_shared = []



node1 = QLSEP_node(0.003,0.4,3,60,days,50)
node2 = QLSEP_node(0.003,0.4,3,60,days,50)
for x in range(0,days):
    for y in range(0,1440/60):
        #Box 1 predicts
        #use y-1 of Box 2
        node1.EWMA_share(x,y,lux_B1_even[x-1][y],node2.EWMA_val[x][y-1])
        node1.Calculate_PER(x,y,lux_B1_even[x][y-1],(np.amax(lux_B1_even[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        
        #Box 2 predicts
        #use y of Box 1
        node2.EWMA_share(x,y,lux_B2_odd[x-1][y],node1.EWMA_val[x][y])
        node2.Calculate_PER(x,y,lux_B2_odd[x][y-1],(np.amax(lux_B2_odd[x])*0.03))
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)



for x in range(0,days):
    EWMA_val_shared.append([item for pair in zip(node1.EWMA_val[x], node2.EWMA_val[x]) for item in pair])
    QLSEP_val_shared.append([item for pair in zip(node1.QLSEP_val[x], node2.QLSEP_val[x]) for item in pair])

[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1_even,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1_even,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2_odd,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2_odd,node2.EWMA_val,days)


[mape_shared_QLSEP_b1, no_shared_QLSEP_b1] = MAPE_overall(lux_B1,QLSEP_val_shared,days)
[mape_shared_EWMA_b1, no_shared_EWMA_b1] = MAPE_overall(lux_B1,EWMA_val_shared,days)

[mape_shared_QLSEP_b2, no_shared_QLSEP_b2] = MAPE_overall(lux_B2,QLSEP_val_shared,days)
[mape_shared_EWMA_b2, no_shared_EWMA_b2] = MAPE_overall(lux_B2,EWMA_val_shared,days)



print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_EWMA,no_b2_EWMA)
print "MAPE = %s%% , N = %s (shared Box 1)" % (mape_shared_EWMA_b1,no_shared_EWMA_b1)
print "MAPE = %s%% , N = %s (shared Box 2)\n" % (mape_shared_EWMA_b2,no_shared_EWMA_b2)



print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2_QLSEP,no_b2_QLSEP)
print "MAPE = %s%% , N = %s (shared Box 1)" % (mape_shared_QLSEP_b1,no_shared_QLSEP_b1)
print "MAPE = %s%% , N = %s (shared Box 2)\n" % (mape_shared_QLSEP_b2,no_shared_QLSEP_b2)



#plot the proifles


time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 10  
plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_B2[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,QLSEP_val_shared[index],'r',label = 'shared')


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Box 1  (day) %s (Actual data)' % str(index+1))
plt.grid()
plt.show()
