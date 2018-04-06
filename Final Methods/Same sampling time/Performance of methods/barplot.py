# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 11:00:58 2018

@author: zck2g15
"""

import numpy as np
import matplotlib.pyplot as plt
execfile("./../../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)



"""
=============================================================================
NREL Dataset
=============================================================================
"""

EWMA_MAPE_NREL =  [49.586,47.485,49.543,49.586,47.485,49.327,47.505]
QLSEP_MAPE_NREL = [47.142,46.553,47.082,47.142,46.633,48.118,46.651]

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
EWMA_MAPE_HCD =  [54.835,52.216,54.804,54.835,52.206,54.924,52.264]
QLSEP_MAPE_HCD = [46.879,47.255,47.077,46.878,47.274,47.060,47.288]

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
EWMA_MAPE_LCD =  [62.484,66.069,67.171,62.484,66.069,62.531,66.054]
QLSEP_MAPE_LCD = [51.049,56.491,53.957,51.056,56.496,51.078,56.463]

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