# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 12:13:08 2018

WCMA on NREL dataset (90 days)


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


"""make it 90 days"""
pre_WCMA = pre_WCMA[1:]
lux_original = lux_original[1:]

"""calculate the MAPE"""
[mape,no] = MAPE_overall(lux_original,pre_WCMA,days-1)
print "MAPE = %s%% , N = %s (using WCMA)" % (mape,no)

#plot the prediction
time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 0

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,pre_WCMA[index],'r',label = 'WCMA')
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

