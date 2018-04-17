# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 23:03:52 2018

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


#split into 2 arrays  (Box 1)
lux_B1_even = []
lux_B2_odd = []
for x in range(len(lux_B1)):
    even = lux_B1[x][0:][::2]
    lux_B1_even.append(even)
    odd = lux_B2[x][1::][::2]
    lux_B2_odd.append(odd)
    
time = np.linspace(0,1440,num=1440/slot)

plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
for n in range(days):
    ax.plot(time,lux_B1[n])
plt.ylabel('Light Intensity (klux)')
plt.xlabel('time (min)')
plt.grid()
plt.savefig('LCD_dataset_B1.png', dpi = 200)



plt.figure(2)
fig, ax = plt.subplots(figsize=(7,4))
for n in range(days):
    ax.plot(time,lux_B2[n])
plt.ylabel('Light Intensity (klux)')
plt.xlabel('time (min)')
plt.grid()
plt.savefig('LCD_dataset_B2.png', dpi = 200)

