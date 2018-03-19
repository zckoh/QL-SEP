# -*- coding: utf-8 -*-
"""
Created on Sun Mar 18 23:38:58 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


#Get the original 48 slots data
slot = 30
day_counter = 1
lux_original = []
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
            lux_original.append([float(i) for i in tmp])
            tmp = []            
        day_counter += 1

days = len(lux_original)

EWMA_val = np.array([[float(0)]*(1440/slot)]*days)

"""New model"""

index = 5
alpha_lst = np.linspace(0,1,num=11)
MAPE_lst = []

for k in range(0,len(alpha_lst)):
    print alpha_lst[k]    
    for x in range(0,days):
        for y in range(0,1440/slot):
            EWMA_val[x][y] = alpha_lst[k]*(EWMA_val[x][y-1]) + (1-alpha_lst[k])*(float(lux_original[x-1][y]))
    #now already complete, calculate the MAPE
    [mape_EWMA, no_b1_EWMA] = MAPE_overall(lux_original,EWMA_val,days)
    MAPE_lst.append(mape_EWMA)
    #reset the EWMA_val
    EWMA_val = np.array([[float(0)]*(1440/slot)]*days)
        
print MAPE_lst



plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(alpha_lst,MAPE_lst,'b')
plt.xlabel(r'$\alpha$')
plt.ylabel('MAPE (%)')
plt.grid()
plt.savefig('alpha_vs_mape.png', dpi = 600)
plt.show()


        
        
        
        
        
        
        
        