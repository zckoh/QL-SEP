# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 12:44:17 2018


EWMA using NREL Dataset (90days)


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


a=QLSEP_node(22,0.1,2,slot,days,2)

for x in range(0,days):
    for y in range(0,(1440/slot)):
        a.EWMA(x,y,lux_original[x-1][y])



"""Remove day 0"""
a.EWMA_val = a.EWMA_val[1:]
lux_original = lux_original[1:]
days = days-1


"""calculate MAPE"""
[mape,no] = MAPE_oneday(lux_original[8],a.EWMA_val[8])
print "MAPE = %s%% , N = %s (using EWMA)" % (mape,no)

#plot the prediction
time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 8

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time48 ,a.EWMA_val[index],'r',label = 'EWMA')
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


