# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 16:49:59 2018

Comparing EWMA, WCMA and QLSEP using the optimum parameters

- Plot MAPE of each day?


@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./QLSEP_class.py")
np.set_printoptions(threshold=np.nan)

def sum_list(d,D,y,myList = [], *args):
    sum = 0
    for x in range(1,D+1):
        sum += float(myList[d-x][y])
    return sum


#Get the original 48 slots data
slot = 30
day_counter = 1
lux_original = []
lux = []
tmp = []
with open("./NREL_data/20160901.csv", 'r') as f:
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




"""EWMA"""
a=QLSEP_node(22,0.1,2,slot,days,2)

for x in range(0,days):
    for y in range(0,(1440/slot)):
        a.EWMA(x,y,lux_original[x-1][y])


"""WCMA"""
D = 4 #past days
K = 3 #past samples
alpha_WCMA = 0.7
#obtain P
P = []
for i in range(K):
    P.append(float(i+1)/K)

M = np.array([[float(0)]*(1440/slot)]*days)
pre_WCMA = np.array([[float(0)]*(1440/slot)]*days)
GAP = np.array([[float(0)]*(1440/slot)]*days)
V = np.array([[[float(0)]*K]*(1440/slot)]*days)


for x in range(0,days):
    for y in range(0,(1440/slot)):
        M[x][y] = sum_list(x,D,y,lux_original)/D
        for k in range(0,K):
           V[x][y][k] = safe_div(float(lux_original[x][y-K+k]),M[x][y-K+k])
        GAP[x][y] = np.dot(V[x][y],P)/np.sum(P)
        pre_WCMA[x][y] = alpha_WCMA*float(lux_original[x][y-1]) + (1-alpha_WCMA)*GAP[x][y]*(M[x][y])


"""QL-SEP"""
node1 = QLSEP_node(0.001,0.1,3,slot,days,50)

for x in range(0,days):
    for y in range(0,1440/slot):
        node1.EWMA(x,y,lux_original[x-1][y])
        node1.Calculate_PER(x,y,lux_original[x][y-1],(np.amax(lux_original[x])*0.03))
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
            
"""Remove first day"""
pre_WCMA = pre_WCMA[1:]
lux_original = lux_original[1:]
a.EWMA_val = a.EWMA_val[1:]
node1.QLSEP_val = node1.QLSEP_val[1:]
days = days-1

"""calculate the MAPE"""
[mape_EWMA,no_EWMA] = MAPE_overall(lux_original,a.EWMA_val,days)
print "MAPE = %s%% , N = %s (using EWMA)" % (mape_EWMA,no_EWMA)

[mape_WCMA,no_WCMA] = MAPE_overall(lux_original,pre_WCMA,days)
print "MAPE = %s%% , N = %s (using WCMA)" % (mape_WCMA,no_WCMA)

[mape_QL,no_QL] = MAPE_overall(lux_original,node1.QLSEP_val,days)
print "MAPE = %s%% , N = %s (using QL-SEP)" % (mape_QL,no_QL)

EWMA_lst = []
WCMA_lst = []
QLSEP_lst = []

for d in range(days):
    EWMA_lst.append(MAPE_oneday(lux_original[d],a.EWMA_val[d]))
    WCMA_lst.append(MAPE_oneday(lux_original[d],pre_WCMA[d]))
    QLSEP_lst.append(MAPE_oneday(lux_original[d],node1.QLSEP_val[d]))
    
time_day = np.linspace(1,90, num = days)

print EWMA_lst[76]

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time_day,EWMA_lst,'g',label = 'EWMA')
ax.plot(time_day ,WCMA_lst,'r',label = 'WCMA')
ax.plot(time_day ,QLSEP_lst,'b',label = 'QLSEP')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Day')
plt.ylabel('MAPE (%)')
plt.title('90 days NREL data')
plt.grid()
plt.savefig('mape_vs_days.png', dpi = 600)
plt.show()


"""Huge Spike"""
plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[77],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,a.EWMA_val[77],'r',label = 'EWMA')
ax.plot(time48 ,node1.QLSEP_val[76],'b',label = 'QLSEP')
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

index = 78
print EWMA_lst[index-1]
print WCMA_lst[index-1]
print QLSEP_lst[index-1]


print EWMA_lst[index]
print WCMA_lst[index]
print QLSEP_lst[index]

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,a.EWMA_val[index],'r',label = 'EWMA')
ax.plot(time48 ,pre_WCMA[index],'orange',label = 'WCMA')
ax.plot(time48 ,node1.QLSEP_val[index],'b',label = 'QLSEP')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Day %s (NREL data)' % str(index+1))
plt.grid()
plt.show()


    
    
    
