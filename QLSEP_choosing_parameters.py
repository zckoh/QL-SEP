# -*- coding: utf-8 -*-
"""
Created on Tue Apr 03 15:48:34 2018

QLSEP -Varying parameters to get optimum value
NREL data (90 days)


@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./QLSEP_class.py")
np.set_printoptions(threshold=np.nan)

index = 20

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
lux_original_backup = lux_original
days_backup = days

learning_rate_lst = np.linspace(0,0.01,num=11)
MAPE_lst = []

for k in range(0,len(learning_rate_lst)):
    lux_original = lux_original_backup
    days = days_backup
    node1 = QLSEP_node(learning_rate_lst[k],0.1,3,slot,days,50)

    for x in range(0,days):
        for y in range(0,1440/slot):
            node1.EWMA(x,y,lux_original[x-1][y])
            node1.Calculate_PER(x,y,lux_original[x][y-1],(np.amax(lux_original[x])*0.03))
            node1.Q_val_update(x,y)
            node1.QLSEP_prediction(x,y)
        
        
#==============================================================================
#     node1.QLSEP_val = node1.QLSEP_val[1:]
#     lux_original = lux_original[1:]
#     days = days-1
#==============================================================================

    """calculate MAPE"""
    [mape,no] = MAPE_overall(lux_original,node1.QLSEP_val,days)
    MAPE_lst.append(mape)
    print "MAPE = %s%% , N = %s (using QL-SEP) Learning rate = %s" % (mape,no,learning_rate_lst[k])

#plot the prediction
time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 9

# =============================================================================
# plt.figure(1)
# fig, ax = plt.subplots(figsize=(7.5,4))
# ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
# ax.plot(time48 ,node1.QLSEP_val[index],'r',label = 'QL-SEP')
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# plt.xlabel('Time(Min)')
# plt.ylabel('Light Intensity (klux)')
# plt.title('Day %s (NREL data)' % str(index+1))
# plt.grid()
# plt.show()
# 
# =============================================================================
plt.figure(1)
fig, ax = plt.subplots(figsize=(6,4))
ax.plot(learning_rate_lst,MAPE_lst,'b')
plt.xlabel(r'$\gamma$')
plt.ylabel('MAPE (%)')
plt.grid()
plt.savefig('learning_rate_vs_mape.png', dpi = 600)
plt.show()


