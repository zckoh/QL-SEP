# -*- coding: utf-8 -*-
"""
Created on Fri Apr 06 11:00:58 2018

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

EWMA_MAPE_NREL =  [49.586,46.026,49.099,49.586,46.026,49.267,46.057]
QLSEP_MAPE_NREL = [47.634,45.719,48.433,47.477,45.681,48.696,45.705]

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
EWMA_MAPE_HCD =  [54.835,51.278,56.062,54.835,51.278,54.785,51.317]
QLSEP_MAPE_HCD = [46.973,46.768,47.824,46.968,46.750,46.865,46.780]

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
EWMA_MAPE_LCD = [62.484,63.391,67.909,62.485,63.391,62.502,63.379]
QLSEP_MAPE_LCD = [51.093,52.523,54.976,51.051,52.467,51.010,52.457]

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