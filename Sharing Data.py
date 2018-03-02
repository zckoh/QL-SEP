# -*- coding: utf-8 -*-
"""
Created on Sun Jan 07 14:41:41 2018

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



#Importing True values collected from both boxes(Samples per Min)
lux_b1_true = []
lux_b2_true = []
slot_true = 1
tmp = []
for i in range(22,32):
    with open("./highly correlated data/Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot_true)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b1_true.append([float(k) for k in tmp])
    tmp = []
    with open("./highly correlated data/Box 2/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot_true)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b2_true.append([float(i) for i in tmp])
    tmp = []



#Importing sampled values from both boxes (samples per 30 min)
#store into 2 different lux_b1 & lux_b2
tmp = []
lux_b1 = []
lux_b2 = []
slot = 30
for i in range(22,32):
    with open("./highly correlated data/Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b1.append([float(k) for k in tmp])
    tmp = []
    with open("./highly correlated data/Box 2/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b2.append([float(i) for i in tmp])
    tmp = []
    

#combine & average (share all data samples both ways)
lux_average = np.array([[float(0)]*(1440/slot)]*len(lux_b1))
for x in range(0,len(lux_b1)):
    for y in range(0,1440/slot):
        lux_average[x][y] = (lux_b1[x][y]+lux_b2[x][y])/2

#intertwine the collected data ,Box 1(lux_b1_int) then Box 2(lux_b2_intt) ...
tmp_int = []
lux_b1_int = []
lux_b2_int = []
min_btw_slot_intertwine = 60
for i in range(22,32):
    with open("./highly correlated data/Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]        
    lux_b1_int.append([float(a) for a in tmp_int])
    tmp_int = []
    
    with open("./highly correlated data/Box 2/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]
    
    lux_b2_int.append([float(s) for s in tmp_int])    
    tmp_int = []


tmp_intt = []
lux_b1_intt = []
lux_b2_intt = []

for i in range(22,32):
    with open("./highly correlated data/Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
        
    lux_b1_intt.append([float(b) for b in tmp_intt])
    tmp_intt = []
    
    with open("./highly correlated data/Box 2/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
    
    lux_b2_intt.append([float(i) for i in tmp_intt])
    tmp_intt = []

#combine (Box1,Box2,Box1,Box2)
temp = []
lux_added_together = []
for x in range(0,10):
    for y in range(len(lux_b2_intt[0])):
        temp.append(lux_b1_int[x][y])
        temp.append(lux_b2_intt[x][y])
    lux_added_together.append(temp)
    temp = []

        
#Combine half_day + half day
def split_list(a_list):
    half = len(a_list)/2
    return a_list[:half], a_list[half:]

lux_b1_part1 = []
lux_b1_part2 = []

lux_b2_part1 = []
lux_b2_part2 = []

for i in range(0,10):
    lux_b1_part1_day, lux_b1_part2_day = split_list(lux_b1[i])
    lux_b1_part1.append(lux_b1_part1_day)
    lux_b1_part2.append(lux_b1_part2_day)
    lux_b2_part1_day, lux_b2_part2_day = split_list(lux_b2[i])
    lux_b2_part1.append(lux_b2_part1_day)
    lux_b2_part2.append(lux_b2_part2_day)
    
#box 1 first half, Box 2 next half
lux_half2_combined = []
for i in range(0,10):
    a = np.append(lux_b1_part1[i],lux_b2_part2[i])
    lux_half2_combined.append(a)

time = np.linspace(1,1440, num = 1440/slot_true)    
time1 = np.linspace(1,1440, num = 1440/(slot))    
time_avg = np.linspace(1,1440,num = 1440/slot)
time_int = np.linspace(1,1440,num = 1440/(min_btw_slot_intertwine/2))
time_half = np.linspace(1,1440,num = 1440/slot)

time2 = np.linspace(1,14400, num = 14400/(slot/2))


lux_last10_b1 = np.array([])
lux_last10_b2 = np.array([])
lux_last10_avg = np.array([])
for i in range(len(lux_b1)-10,len(lux_b1)):
    lux_last10_b1 = np.append(lux_last10_b1,lux_b1[i])
    lux_last10_b2 = np.append(lux_last10_b2,lux_b2[i])
    lux_last10_avg = np.append(lux_last10_avg,lux_average[i])
    
index = 9




plt.figure(1)
fig, ax = plt.subplots(figsize=(20,4))

ax.plot(time,lux_b1_true[index],'r',label='Box 1(30 Actual)')
ax.plot(time,lux_b2_true[index],'r',label='Box 1(30 Actual)')

ax.plot(time_avg,lux_average[index],'g',label='Averaged')

ax.plot(time_half,lux_half2_combined[index],'r',label = 'Half')
ax.plot(time_int,lux_added_together[index],'b',label='Intertwine')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlim([400,1100])
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Light intensity sampled every 30 mins %s/11/2017' % str(20+index+1))

'''
plt.figure(2)
fig, ax = plt.subplots(figsize=(15,4))
ax.plot(time2,lux_last10_b1,'r',label='Box 1')
ax.plot(time2,lux_last10_b2,'b',label='Box 2')
ax.plot(time2,lux_last10_avg,'g',label='Box 3')
plt.ylim([0,25])

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.grid()
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Light intensity sampled every 30 mins %s/11/2017' % str(20+index+1))
'''