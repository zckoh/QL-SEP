# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 11:00:58 2018

@author: zck2g15
"""

import numpy as np



"""
=============================================================================
NREL Dataset
=============================================================================
"""

EWMA_MAPE_NREL = [49.586,46.026,49.099,49.586,46.026,49.288,46.069]
QLSEP_MAPE_NREL = [47.142,45.239,47.882,47.197,45.249,48.218,45.305]

methods = np.linspace(1,7,num=7)


plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_NREL,align='center',label = 'EWMA',color = 'b',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_NREL,align='center',label = 'QLSEP',color = 'r',alpha = 0.2) # A bar chart


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
plt.title('Performance of EWMA & QLSEP on NREL dataset with different methods')
plt.show()

"""
=============================================================================
HCD Dataset
=============================================================================
"""
EWMA_MAPE_HCD = [54.835,51.278,56.062,54.835,51.278,54.814,51.327]
QLSEP_MAPE_HCD = [46.879,46.666,47.727,46.889,46.667,46.786,46.712]

methods = np.linspace(1,7,num=7)


plt.figure(2)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_HCD,align='center',label = 'EWMA',color = 'b',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_HCD,align='center',label = 'QLSEP',color = 'r',alpha = 0.2) # A bar chart


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
plt.title('Performance of EWMA & QLSEP on HCD dataset with different methods')
plt.show()


"""
=============================================================================
LCD Dataset
=============================================================================
"""
EWMA_MAPE_LCD = [62.484,63.391,67.909,62.485,63.391,62.506,63.384]
QLSEP_MAPE_LCD = [51.049,52.477,54.92,51.062,52.474,50.973,52.443]

methods = np.linspace(1,7,num=7)


plt.figure(2)
fig, ax = plt.subplots(figsize=(7.5,4))
plt.bar(methods,EWMA_MAPE_LCD,align='center',label = 'EWMA',color = 'b',alpha = 0.2) # A bar chart
plt.bar(methods,QLSEP_MAPE_LCD,align='center',label = 'QLSEP',color = 'r',alpha = 0.2) # A bar chart


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
plt.title('Performance of EWMA & QLSEP on LCD dataset with different methods')
plt.show()