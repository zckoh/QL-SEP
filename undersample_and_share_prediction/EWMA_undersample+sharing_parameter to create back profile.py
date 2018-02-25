# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:47:50 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)

def safe_div(x,y):
    if y == 0:
        return 0    
    return x / y


tmp = []
lux_B1 = []
slot = 30
"""getting data"""
for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

EWMA_val = np.array([[float(0)]*(1440/slot)]*days)

"""Set to have intertwine sampling """
tmp_int = []
lux_b1_int = []
lux_b2_int = []
min_btw_slot_intertwine = 60
for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]        
    lux_b1_int.append([float(a) for a in tmp_int])
    tmp_int = []
    
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]
    
    lux_b2_int.append([float(s) for s in tmp_int])    
    tmp_int = []
    
tmp_intt = []
lux_b1_intt = []
lux_b2_intt = []

for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
        
    lux_b1_intt.append([float(b) for b in tmp_intt])
    tmp_intt = []
    
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
    
    lux_b2_intt.append([float(i) for i in tmp_intt])
    tmp_intt = []


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
        EWMA_valb1[x][y] = alpha*(EWMA_valb1[x][y-1]) + (1-alpha)*(float(lux_b1_int[x-1][y]))
        EWMA_valb2[x][y] = alpha*(EWMA_valb2[x][y-1]) + (1-alpha)*(float(lux_b2_intt[x-1][y]))

for x in range(0,days):
    for y in range(0,1440/slot):
        EWMA_val_noprob[x][y] = alpha*(EWMA_val_noprob[x][y-1]) + (1-alpha)*(float(lux_B1[x-1][y]))


for x in range(0,days):
    EWMA_val_shared.append([item for pair in zip(EWMA_valb1[x], EWMA_valb2[x]) for item in pair])

EWMA_val_tmp = []
noprob_tmp = []
lux_tmp_b1 = []
shared = []
for i in range(0,len(lux_B1)):
    EWMA_10 = [float(j) for j in EWMA_valb1[i]]
    EWMA_shared = [float(j) for j in EWMA_val_shared[i]]
    nopros = [float(j) for j in EWMA_val_noprob[i]]
    #append all seen values into the same array to get the 10 days
    EWMA_val_tmp += EWMA_10
    noprob_tmp+=nopros
    shared += EWMA_shared
    lux_tmp_b1 +=lux_B1[i]

a = np.amax(lux_tmp_b1)
b = a*0.05

overall_before = 0
overall_coutner = 0
for i in range(len(noprob_tmp)):
    if(lux_tmp_b1[i]!=0):
        if(lux_tmp_b1[i]>b):
            overall_coutner += 1
            overall_before += abs((lux_tmp_b1[i]-noprob_tmp[i])/lux_tmp_b1[i])
            
overall_before = overall_before*100/overall_coutner
print "MAPE (EWMA) overall = %s%% (no undersampling no sharing)"% overall_before
print "N = %s" % overall_coutner
MAPE_EWMA_overall = 0
EWMA_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(EWMA_val_tmp)):
    if(lux_tmp_b1[i*2]!=0):
        if(lux_tmp_b1[i*2]>b):
            EWMA_MAPE_N_COUNTER += 1
            MAPE_EWMA_overall += abs((lux_tmp_b1[i*2]-EWMA_val_tmp[i])/lux_tmp_b1[i*2])
            
MAPE_EWMA_overall = MAPE_EWMA_overall*100/EWMA_MAPE_N_COUNTER
print "MAPE (EWMA) overall = %s%% (undersampling no sharing)"% MAPE_EWMA_overall
print "N = %s" % EWMA_MAPE_N_COUNTER
MAPE_EWMA_overall = 0
EWMA_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(shared)):
    if(lux_tmp_b1[i]!=0):
        if(lux_tmp_b1[i]>b):
            EWMA_MAPE_N_COUNTER += 1
            MAPE_EWMA_overall += abs((lux_tmp_b1[i]-shared[i])/lux_tmp_b1[i])
            
MAPE_EWMA_overall = MAPE_EWMA_overall*100/EWMA_MAPE_N_COUNTER
print "MAPE (EWMA) overall = %s%% (undersampling + sharing)"% MAPE_EWMA_overall
print "N = %s" % EWMA_MAPE_N_COUNTER

time = np.linspace(1,1440, num = 1440/slot)
timeb1 = []
timeb2 = []

for i in range(len(time)):
    if(i%2==0):
        timeb1.append(time[i])
    else:
        timeb2.append(time[i])



plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time,lux_B1[index],'g',label = 'Actual Box 1')
#ax.plot(time,lux_B2[index],'y',label = 'Actual Box 2')
#ax.plot(time,EWMA_val_noprob[index],'yx',label = 'No sharing & undersampling')
#ax.plot(timeb1,lux_b1_int[index],'b',label = 'Box 1')
ax.plot(timeb1,EWMA_valb1[index],'b',label = 'Undersample (no sharing)')

#ax.plot(timeb2,lux_b2_intt[index],'rx',label = 'Box 2')
ax.plot(time,EWMA_val_shared[index],'r',label = 'Undersample + sharing')

#ax.plot(time2,EWMA_valb1[index],'rx',label='EWMA')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Box 1 day %s' % str(index+1))
plt.grid()
plt.ylim([0,15])
plt.savefig('cloudy_day_plot.png', bbox_inches='tight')
