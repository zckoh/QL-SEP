# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 22:54:10 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
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
    
index = 29

time = np.linspace(0,1440,num=1440/slot)

plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
for n in range(days):
    ax.plot(time,lux_original[n])
plt.ylabel('Light Intensity (klux)')
plt.xlabel('time (min)')
plt.grid()
plt.savefig('NREL_dataset.png', dpi = 200)

