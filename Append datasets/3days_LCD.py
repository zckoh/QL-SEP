# -*- coding: utf-8 -*-
"""
Created on Mon Apr 23 23:06:45 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
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

index = 12
"""Combine 3 days"""
B1_3day = []
B2_3day = []

for x in range(3):
    for slt in range(1440/slot):
        B1_3day.append(lux_B1[index+x][slt])
        B2_3day.append(lux_B2[index+x][slt])

time = np.linspace(0,1440*3,num=1440*3/slot)
plt.figure(1)
fig, ax = plt.subplots(figsize=(15,4))
ax.plot(time,B1_3day,'g',label = 'Box 1')
ax.plot(time,B2_3day,'r',label = 'Box 2')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width

plt.ylabel('Light Intensity (klux)')
plt.xlabel('time (min)')
plt.ylim([0,24])
plt.grid()
plt.savefig('LCD_3day.png', dpi = 200)