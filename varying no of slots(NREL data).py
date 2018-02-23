# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 13:00:30 2018

Using data from NREL

Vary the no of slots per day and calculating its MAPE

No sharing of parameters, use actual collected data

@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools

from QLSEP_class import QLSEP_node

np.set_printoptions(threshold=np.nan)

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

"""Import data"""
slot = 30
day_counter = 1
lux_B1 = []
slot_true = 1
lux = []
tmp = []
with open("./NREL_data/20160901.csv", 'r') as f:
    fifthlines = itertools.islice(f, 0, None, slot)
    for lines in fifthlines:
        tmp.append(lines.split(',')[2])
        if(day_counter == (1440/slot)):
            day_counter = 0
            tmp = [w.replace('\n', '') for w in tmp]
            lux_B1.append([float(i) for i in tmp])
            tmp = []            
        day_counter += 1

days = len(lux_B1)

print len(lux_B1[20])

"""Different sampling frequency"""
lux_60min = []
lux_90min = []
lux_120min = []

tmp_60 = []
tmp_90 = []
tmp_120 = []

#save for each 2,3,4 times
for x in range(len(lux_B1)):
    for i in range(len(lux_B1[x])):
        if(i%2==0):
            tmp_60.append(lux_B1[x][i])
        if(i%3==0):
            tmp_90.append(lux_B1[x][i])
        if(i%4==0):
            tmp_120.append(lux_B1[x][i])
    lux_60min.append(tmp_60)
    tmp_60 = []
    lux_90min.append(tmp_90)
    tmp_90 = []
    lux_120min.append(tmp_120)
    tmp_120 = []




"""calculate EWMA + QLSEP for each total slot"""
index = 18

"""48 slots"""
node48 = QLSEP_node(0.001,0.4,3,slot,days,50)

for x in range(0,days):
    for y in range(0,1440/slot):
        node48.EWMA(x,y,lux_B1[x-1][y])
        node48.Calculate_PER(x,y,lux_B1[x][y-1])
        node48.Q_val_update(x,y)
        node48.QLSEP_prediction(x,y)


"""Find MAPE(EWMA)"""
lux_B1_combined = []
node48_EWMA_combined = []
for i in range(0,len(lux_B1)):
    EWMA_tmp = [float(j) for j in node48.EWMA_val[i]]
    lux_tmp = [float(j) for j in lux_B1[i]]
    lux_B1_combined += lux_tmp
    node48_EWMA_combined += EWMA_tmp

a = np.amax(lux_B1_combined)
b = a*0.05

EWMA_MAPE_COUNTER_48 = 0
EWMA_overall_48 = 0
for i in range(len(lux_B1_combined)):
    if(lux_B1_combined[i]!=0):
        if(lux_B1_combined[i]>b):
            EWMA_MAPE_COUNTER_48 += 1
            EWMA_overall_48 += abs((lux_B1_combined[i]-node48_EWMA_combined[i])/lux_B1_combined[i])

MAPE_EWMA_overall_48 = EWMA_overall_48*100/EWMA_MAPE_COUNTER_48
print "MAPE (EWMA) overall = %s%% (48 slots)"% MAPE_EWMA_overall_48
print "N = %s" % EWMA_MAPE_COUNTER_48




time = np.linspace(1,1440, num = 1440/slot)
plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))

ax.plot(time,lux_B1[index],'g',label = 'Actual')
ax.plot(time,node48.QLSEP_val[index],'r',label = 'QLSEP')
ax.plot(time,node48.EWMA_val[index],'b',label = 'EWMA')


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')

plt.grid()
plt.title('Day %s (48 slots)' % str(index+1))





"""24 slots"""
node24 = QLSEP_node(0.001,0.4,3,60,days,50)
for x in range(0,days):
    for y in range(0,1440/60):
        node24.EWMA(x,y,lux_60min[x-1][y])
        node24.Calculate_PER(x,y,lux_60min[x][y-1])
        node24.Q_val_update(x,y)
        node24.QLSEP_prediction(x,y)

"""Find MAPE(EWMA)"""
lux_60min_combined = []
node24_EWMA_combined = []
for i in range(0,len(lux_B1)):
    EWMA_tmp = [float(j) for j in node24.EWMA_val[i]]
    lux_tmp = [float(j) for j in lux_60min[i]]
    lux_60min_combined += lux_tmp
    node24_EWMA_combined += EWMA_tmp

a = np.amax(lux_60min_combined)
b = a*0.05

EWMA_MAPE_COUNTER_24 = 0
EWMA_overall_24 = 0
for i in range(len(lux_60min_combined)):
    if(lux_60min_combined[i]!=0):
        if(lux_60min_combined[i]>b):
            EWMA_MAPE_COUNTER_24 += 1
            EWMA_overall_24 += abs((lux_60min_combined[i]-node24_EWMA_combined[i])/lux_60min_combined[i])

MAPE_EWMA_overall_24 = EWMA_overall_24*100/EWMA_MAPE_COUNTER_24
print "MAPE (EWMA) overall = %s%% (24 slots)"% MAPE_EWMA_overall_24
print "N = %s" % EWMA_MAPE_COUNTER_24


time = np.linspace(1,1440, num = 1440/60)
plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))

ax.plot(time,lux_60min[index],'g',label = 'Actual')
ax.plot(time,node24.QLSEP_val[index],'r',label = 'QLSEP')
ax.plot(time,node24.EWMA_val[index],'b',label = 'EWMA')


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')

plt.grid()
plt.title('Day %s (24 slots)' % str(index+1))


"""16 slots"""
node16 = QLSEP_node(0.001,0.4,3,90,days,50)
for x in range(0,days):
    for y in range(0,1440/90):
        node16.EWMA(x,y,lux_90min[x-1][y])
        node16.Calculate_PER(x,y,lux_90min[x][y-1])
        node16.Q_val_update(x,y)
        node16.QLSEP_prediction(x,y)

"""Find MAPE(EWMA)"""
lux_90min_combined = []
node16_EWMA_combined = []
for i in range(0,len(lux_B1)):
    EWMA_tmp = [float(j) for j in node16.EWMA_val[i]]
    lux_tmp = [float(j) for j in lux_90min[i]]
    lux_90min_combined += lux_tmp
    node16_EWMA_combined += EWMA_tmp

a = np.amax(lux_90min_combined)
b = a*0.05

EWMA_MAPE_COUNTER_16 = 0
EWMA_overall_16 = 0
for i in range(len(lux_90min_combined)):
    if(lux_90min_combined[i]!=0):
        if(lux_90min_combined[i]>b):
            EWMA_MAPE_COUNTER_16 += 1
            EWMA_overall_16 += abs((lux_90min_combined[i]-node16_EWMA_combined[i])/lux_90min_combined[i])

MAPE_EWMA_overall_16 = EWMA_overall_16*100/EWMA_MAPE_COUNTER_16
print "MAPE (EWMA) overall = %s%% (16 slots)"% MAPE_EWMA_overall_16
print "N = %s" % EWMA_MAPE_COUNTER_16



time = np.linspace(1,1440, num = 1440/90)
plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))

ax.plot(time,lux_90min[index],'g',label = 'Actual')
ax.plot(time,node16.QLSEP_val[index],'r',label = 'QLSEP')
ax.plot(time,node16.EWMA_val[index],'b',label = 'EWMA')


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')

plt.grid()
plt.title('Day %s (16 slots)' % str(index+1))




"""12 slots"""
node12 = QLSEP_node(0.001,0.4,3,120,days,50)
for x in range(0,days):
    for y in range(0,1440/120):
        node12.EWMA(x,y,lux_120min[x-1][y])
        node12.Calculate_PER(x,y,lux_120min[x][y-1])
        node12.Q_val_update(x,y)
        node12.QLSEP_prediction(x,y)

"""Find MAPE(EWMA)"""
lux_120min_combined = []
node12_EWMA_combined = []
for i in range(0,len(lux_B1)):
    EWMA_tmp = [float(j) for j in node12.EWMA_val[i]]
    lux_tmp = [float(j) for j in lux_120min[i]]
    lux_120min_combined += lux_tmp
    node12_EWMA_combined += EWMA_tmp

a = np.amax(lux_120min_combined)
b = a*0.05

EWMA_MAPE_COUNTER_12 = 0
EWMA_overall_12 = 0
for i in range(len(lux_120min_combined)):
    if(lux_120min_combined[i]!=0):
        if(lux_120min_combined[i]>b):
            EWMA_MAPE_COUNTER_12 += 1
            EWMA_overall_12 += abs((lux_120min_combined[i]-node12_EWMA_combined[i])/lux_120min_combined[i])

MAPE_EWMA_overall_12 = EWMA_overall_12*100/EWMA_MAPE_COUNTER_12
print "MAPE (EWMA) overall = %s%% (12 slots)"% MAPE_EWMA_overall_12
print "N = %s" % EWMA_MAPE_COUNTER_12


time = np.linspace(1,1440, num = 1440/120)
plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))

ax.plot(time,lux_120min[index],'g',label = 'Actual')
ax.plot(time,node12.QLSEP_val[index],'r',label = 'QLSEP')
ax.plot(time,node12.EWMA_val[index],'b',label = 'EWMA')


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')

plt.grid()
plt.title('Day %s (12 slots)' % str(index+1))


