# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 13:42:59 2018

@author: zck2g15
"""

import numpy as np
import matplotlib.pyplot as plt
execfile("./../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)



"""
=============================================================================
NREL Dataset
=============================================================================
"""

EWMA_MAPE_NREL_same =  [49.586,47.485,49.543,49.586,47.485,49.327,47.505]
EWMA_MAPE_NREL_diff =  [49.586,46.026,49.099,49.586,46.026,49.288,46.069]

methods = np.linspace(1,7,num=7)


plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_NREL_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,EWMA_MAPE_NREL_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of EWMA on NREL dataset with different methods')
plt.grid()
plt.savefig('MAPE_EWMA_NREL_7methods.png', dpi = 600)
plt.show()

EWMA_change_same_NREL = []
EWMA_change_diff_NREL = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    EWMA_change_same_NREL.append(EWMA_MAPE_NREL_same[j]-EWMA_MAPE_NREL_same[0])
    EWMA_change_diff_NREL.append(EWMA_MAPE_NREL_diff[j]-EWMA_MAPE_NREL_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(2)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,EWMA_change_same_NREL,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,EWMA_change_diff_NREL,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-5,5)
#plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
plt.grid()
plt.savefig('MAPE_EWMA_NREL_7methods_inc_dec.png', dpi = 600)
plt.show()



"""QLSEP"""
QLSEP_MAPE_NREL_same = [47.142,46.553,47.082,47.142,46.633,48.118,46.651]
QLSEP_MAPE_NREL_diff = [47.142,45.239,47.882,47.197,45.249,48.218,45.305]


plt.figure(3)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,QLSEP_MAPE_NREL_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_NREL_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of QLSEP on NREL dataset with different methods')
plt.grid()
plt.savefig('MAPE_QLSEP_NREL_7methods.png', dpi = 600)
plt.show()

QLSEP_change_same_NREL = []
QLSEP_change_diff_NREL = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    QLSEP_change_same_NREL.append(QLSEP_MAPE_NREL_same[j]-QLSEP_MAPE_NREL_same[0])
    QLSEP_change_diff_NREL.append(QLSEP_MAPE_NREL_diff[j]-QLSEP_MAPE_NREL_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(4)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,QLSEP_change_same_NREL,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,QLSEP_change_diff_NREL,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-5,5)
#plt.title('MAPE increase/decrease from baseline (QLSEP-NREL)')
plt.grid()
plt.savefig('MAPE_QLSEP_NREL_7methods_inc_dec.png', dpi = 600)
plt.show()



"""
=============================================================================
HCD Dataset
=============================================================================
"""
EWMA_MAPE_HCD_same =  [54.835,52.216,54.804,54.835,52.206,54.924,52.264]
EWMA_MAPE_HCD_diff =  [54.835,51.278,56.062,54.835,51.278,54.814,51.327]


methods = np.linspace(1,7,num=7)


plt.figure(3)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_HCD_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,EWMA_MAPE_HCD_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of EWMA on HCD dataset with different methods')
plt.grid()
plt.savefig('MAPE_EWMA_HCD_7methods.png', dpi = 600)
plt.show()


EWMA_change_same_HCD = []
EWMA_change_diff_HCD = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    EWMA_change_same_HCD.append(EWMA_MAPE_HCD_same[j]-EWMA_MAPE_HCD_same[0])
    EWMA_change_diff_HCD.append(EWMA_MAPE_HCD_diff[j]-EWMA_MAPE_HCD_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(8)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,EWMA_change_same_HCD,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,EWMA_change_diff_HCD,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-5,5)
#plt.title('MAPE increase/decrease from baseline (EWMA-HCD)')
plt.grid()
plt.savefig('MAPE_EWMA_HCD_7methods_inc_dec.png', dpi = 600)
plt.show()




"""QLSEP"""
QLSEP_MAPE_HCD_same = [46.879,47.255,47.077,46.878,47.274,47.060,47.288]
QLSEP_MAPE_HCD_diff = [46.879,46.666,47.727,46.889,46.667,46.786,46.712]

plt.figure(4)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,QLSEP_MAPE_HCD_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_HCD_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of QLSEP on HCD dataset with different methods')
plt.grid()
plt.savefig('MAPE_QLSEP_HCD_7methods.png', dpi = 600)
plt.show()

QLSEP_change_same_HCD = []
QLSEP_change_diff_HCD = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    QLSEP_change_same_HCD.append(QLSEP_MAPE_HCD_same[j]-QLSEP_MAPE_HCD_same[0])
    QLSEP_change_diff_HCD.append(QLSEP_MAPE_HCD_diff[j]-QLSEP_MAPE_HCD_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(8)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,QLSEP_change_same_HCD,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,QLSEP_change_diff_HCD,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-5,5)
#plt.title('MAPE increase/decrease from baseline (QLSEP-HCD)')
plt.grid()
plt.savefig('MAPE_QLSEP_HCD_7methods_inc_dec.png', dpi = 600)
plt.show()

"""
=============================================================================
LCD Dataset
=============================================================================
"""
EWMA_MAPE_LCD_same =  [62.484,66.069,67.171,62.484,66.069,62.531,66.054]
EWMA_MAPE_LCD_diff =  [62.484,63.391,67.909,62.485,63.391,62.506,63.384]


methods = np.linspace(1,7,num=7)


plt.figure(5)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_LCD_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,EWMA_MAPE_LCD_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of EWMA on LCD dataset with different methods')
plt.grid()
plt.savefig('MAPE_EWMA_LCD_7methods.png', dpi = 600)
plt.show()


EWMA_change_same_LCD = []
EWMA_change_diff_LCD = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    EWMA_change_same_LCD.append(EWMA_MAPE_LCD_same[j]-EWMA_MAPE_LCD_same[0])
    EWMA_change_diff_LCD.append(EWMA_MAPE_LCD_diff[j]-EWMA_MAPE_LCD_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(8)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,EWMA_change_same_LCD,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,EWMA_change_diff_LCD,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-7,7)
#plt.title('MAPE increase/decrease from baseline (EWMA-LCD)')
plt.grid()
plt.savefig('MAPE_EWMA_LCD_7methods_inc_dec.png', dpi = 600)
plt.show()


"""QLSEP"""


QLSEP_MAPE_LCD_same = [51.049,56.491,53.957,51.056,56.496,51.078,56.463]
QLSEP_MAPE_LCD_diff = [51.049,52.477,54.92,51.062,52.474,50.973,52.443]

plt.figure(6)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,QLSEP_MAPE_LCD_same,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_LCD_diff,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart


legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('Overall MAPE (%)')
plt.ylim(40,70)
#plt.title('Performance of QLSEP on LCD dataset with different methods')
plt.grid()
plt.savefig('MAPE_QLSEP_LCD_7methods.png', dpi = 600)
plt.show()






QLSEP_change_same_LCD = []
QLSEP_change_diff_LCD = []
for j in range(1,len(EWMA_MAPE_NREL_same)):
    QLSEP_change_same_LCD.append(QLSEP_MAPE_LCD_same[j]-QLSEP_MAPE_LCD_same[0])
    QLSEP_change_diff_LCD.append(QLSEP_MAPE_LCD_diff[j]-QLSEP_MAPE_LCD_diff[0])
    
    
six_methods = np.linspace(2,7,num=6)

plt.figure(8)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(six_methods,QLSEP_change_same_LCD,align='center',label = 'Same',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,QLSEP_change_diff_LCD,align='center',label = 'Diff',color = 'b',alpha = 0.2) # A bar chart

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Methods')
plt.ylabel('MAPE increase/decrease (%)')
plt.ylim(-7,7)
#plt.title('MAPE increase/decrease from baseline (QLSEP-LCD')
plt.grid()
plt.savefig('MAPE_QLSEP_LCD_7methods_inc_dec.png', dpi = 600)
plt.show()

