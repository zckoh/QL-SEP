# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 13:55:44 2018

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

"""calculate EWMA then combine"""
EWMA_val_noprob = np.array([[float(0)]*(1440/slot)]*days)

"""original (Bad model)"""
EWMA_valb1 = np.array([[float(0)]*(1440/slot/2)]*days)
EWMA_valb2 = np.array([[float(0)]*(1440/slot/2)]*days)

"""New model"""
#EWMA_val_shared = np.array([[float(0)]*(1440/slot)]*days)
EWMA_val_shared = []
index = 5
alpha = 0.4


for x in range(0,days):
    for y in range(0,1440/slot/2):
        EWMA_valb1[x][y] = alpha*(EWMA_valb1[x][y-1]) + (1-alpha)*(float(lux_B1[x-1][y]))
        EWMA_valb2[x][y] = alpha*(EWMA_valb2[x][y-1]) + (1-alpha)*(float(lux_B2[x-1][y]))
        
for x in range(0,days):
    for y in range(0,1440/slot):  
        EWMA_val_noprob[x][y] = alpha*(EWMA_val_noprob[x][y-1]) + (1-alpha)*(float(lux_original[x-1][y]))
        
for x in range(0,days):
    EWMA_val_shared.append([item for pair in zip(EWMA_valb1[x], EWMA_valb2[x]) for item in pair])

[mape_b1,no_b1] = MAPE_overall(lux_B1,EWMA_valb1,days)
[mape_b2,no_b2] = MAPE_overall(lux_B2,EWMA_valb2,days)
[mape_shared,no_shared] = MAPE_overall(lux_original,EWMA_val_shared,days)
[mape_original,no_original] = MAPE_overall(lux_original,EWMA_val_noprob,days)

print "24 slots"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1,no_b1)
print "MAPE = %s%% , N = %s (Box 2)" % (mape_b2,no_b2)
print "MAPE = %s%% , N = %s (Box 1 + 2)" % (mape_shared,no_shared)
print "\n48 slots"
print "MAPE = %s%% , N = %s (single node)\n" % (mape_original,no_original)
#plot the prediction
time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 54

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,EWMA_val_shared[index],'r',label = 'Undersample + sharing')
ax.plot(time24,EWMA_valb1[index],'b',label = 'Undersample (no sharing)')

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
