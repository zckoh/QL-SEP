# -*- coding: utf-8 -*-
"""
Created on Mon Apr 09 16:49:30 2018

@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
execfile("./../../../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)


"""
=============================================================================
NREL Dataset
=============================================================================
"""
EWMA_MAPE_NREL_diff =  [49.586,46.026,49.099,49.586,46.026,49.267,46.057]
EWMA_MAPE_NREL =  [49.586,47.485,49.543,49.586,47.485,49.323,47.497]


methods = np.linspace(1,7,num=7)


EWMA_change_same_NREL = []
EWMA_change_diff_NREL = []

for j in range(1,len(EWMA_MAPE_NREL)):
    EWMA_change_same_NREL.append((EWMA_MAPE_NREL[j]-EWMA_MAPE_NREL[0]))
    EWMA_change_diff_NREL.append((EWMA_MAPE_NREL_diff[j]-EWMA_MAPE_NREL_diff[0]))
    
    
six_methods = np.linspace(2,7,num=6)


plt.figure(2)
fig, ax = plt.subplots(figsize=(6,4))
plt.bar(six_methods,EWMA_change_diff_NREL,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
plt.bar(six_methods,EWMA_change_same_NREL,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart

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
plt.savefig('MAPE_EWMA_NREL_7methods_inc_dec(same).png', dpi = 200)
plt.show()


"""QLSEP"""
QLSEP_MAPE_NREL_diff = [47.634,45.719,48.433,47.477,45.681,48.696,45.705]
QLSEP_MAPE_NREL = [47.634,46.813,47.586,47.634,46.774,48.628,46.785]
methods = np.linspace(1,7,num=7)

print "QLSEP (NREL)"
QLSEP_change_same_NREL = []
QLSEP_change_diff_NREL = []
for j in range(1,len(QLSEP_MAPE_NREL)):
    QLSEP_change_same_NREL.append((QLSEP_MAPE_NREL[j]-QLSEP_MAPE_NREL[0]))
    QLSEP_change_diff_NREL.append((QLSEP_MAPE_NREL_diff[j]-QLSEP_MAPE_NREL_diff[0]))
    print "M%s : %s" % (j+1,(QLSEP_MAPE_NREL[j]-QLSEP_MAPE_NREL[0]))
    
six_methods = np.linspace(2,7,num=6)


# =============================================================================
# plt.figure(2)
# fig, ax = plt.subplots(figsize=(6,4))
# plt.bar(six_methods,QLSEP_change_diff_NREL,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
# plt.bar(six_methods,QLSEP_change_same_NREL,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart
# 
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# 
# 
# plt.xlabel('Methods')
# plt.ylabel('MAPE increase/decrease (%)')
# plt.ylim(-5,5)
# #plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
# plt.grid()
# plt.savefig('MAPE_QLSEP_NREL_7methods_inc_dec(same).png', dpi = 200)
# plt.show()
# =============================================================================

"""
=============================================================================
HCD Dataset
=============================================================================
"""

EWMA_MAPE_HCD_diff =  [54.835,51.278,56.062,54.835,51.278,54.785,51.317]
EWMA_MAPE_HCD =  [54.835,52.216,54.804,54.835,52.216,54.920,52.253]
methods = np.linspace(1,7,num=7)


EWMA_change_same_HCD = []
EWMA_change_diff_HCD = []
for j in range(1,len(EWMA_MAPE_HCD)):
    EWMA_change_same_HCD.append((EWMA_MAPE_HCD[j]-EWMA_MAPE_HCD[0]))
    EWMA_change_diff_HCD.append((EWMA_MAPE_HCD_diff[j]-EWMA_MAPE_HCD_diff[0]))
      
six_methods = np.linspace(2,7,num=6)

# =============================================================================
# 
# plt.figure(2)
# fig, ax = plt.subplots(figsize=(6,4))
# plt.bar(six_methods,EWMA_change_diff_HCD,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
# plt.bar(six_methods,EWMA_change_same_HCD,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart
# 
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# 
# plt.xlabel('Methods')
# plt.ylabel('MAPE increase/decrease (%)')
# plt.ylim(-5,5)
# #plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
# plt.grid()
# plt.savefig('MAPE_EWMA_HCD_7methods_inc_dec(same).png', dpi = 200)
# plt.show()
# =============================================================================

"""QLSEP"""
QLSEP_MAPE_HCD_diff = [46.973,46.768,47.824,46.968,46.750,46.865,46.780]
QLSEP_MAPE_HCD = [46.973,47.367,47.172,46.981,47.362,47.154,47.375]
methods = np.linspace(1,7,num=7)


QLSEP_change_same_HCD = []
QLSEP_change_diff_HCD = []
print "QLSEP (HCD)"
for j in range(1,len(QLSEP_MAPE_HCD)):
    QLSEP_change_same_HCD.append((QLSEP_MAPE_HCD[j]-QLSEP_MAPE_HCD[0]))
    QLSEP_change_diff_HCD.append((QLSEP_MAPE_HCD_diff[j]-QLSEP_MAPE_HCD_diff[0]))
    print "M%s : %s" % (j+1,(QLSEP_MAPE_HCD[j]-QLSEP_MAPE_HCD[0]))
      
six_methods = np.linspace(2,7,num=6)

# =============================================================================
# plt.figure(2)
# fig, ax = plt.subplots(figsize=(6,4))
# plt.bar(six_methods,QLSEP_change_diff_HCD,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
# plt.bar(six_methods,QLSEP_change_same_HCD,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart
# 
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# 
# plt.xlabel('Methods')
# plt.ylabel('MAPE increase/decrease (%)')
# plt.ylim(-5,5)
# #plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
# plt.grid()
# plt.savefig('MAPE_QLSEP_HCD_7methods_inc_dec(same).png', dpi = 200)
# plt.show()
# =============================================================================



"""
=============================================================================
LCD Dataset
=============================================================================
"""
EWMA_MAPE_LCD_diff = [62.484,63.391,67.909,62.485,63.391,62.502,63.379]
EWMA_MAPE_LCD = [62.484,66.069,67.171,62.484,66.069,62.532,66.027]
methods = np.linspace(1,7,num=7)


EWMA_change_same_LCD = []
EWMA_change_diff_LCD = []
print "QLSEP (LCD)"
for j in range(1,len(EWMA_MAPE_LCD)):
    EWMA_change_same_LCD.append((EWMA_MAPE_LCD[j]-EWMA_MAPE_LCD[0]))
    EWMA_change_diff_LCD.append((EWMA_MAPE_LCD_diff[j]-EWMA_MAPE_LCD_diff[0]))
    
six_methods = np.linspace(2,7,num=6)


# =============================================================================
# plt.figure(2)
# fig, ax = plt.subplots(figsize=(6,4))
# plt.bar(six_methods,EWMA_change_diff_LCD,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
# plt.bar(six_methods,EWMA_change_same_LCD,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart
# 
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# 
# plt.xlabel('Methods')
# plt.ylabel('MAPE increase/decrease (%)')
# plt.ylim(-7,7)
# #plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
# plt.grid()
# plt.savefig('MAPE_EWMA_LCD_7methods_inc_dec(same).png', dpi = 200)
# plt.show()
# 
# =============================================================================
"""QLSEP"""
QLSEP_MAPE_LCD_diff = [51.093,52.523,54.976,51.051,52.467,51.010,52.457]
QLSEP_MAPE_LCD = [51.093,56.555,54.021,51.092,56.553,51.121,56.513]
methods = np.linspace(1,7,num=7)


QLSEP_change_same_LCD = []
QLSEP_change_diff_LCD = []

for j in range(1,len(QLSEP_MAPE_LCD)):
    QLSEP_change_same_LCD.append((QLSEP_MAPE_LCD[j]-QLSEP_MAPE_LCD[0]))
    QLSEP_change_diff_LCD.append((QLSEP_MAPE_LCD_diff[j]-QLSEP_MAPE_LCD_diff[0]))
    print "M%s : %s" % (j+1,(QLSEP_MAPE_LCD[j]-QLSEP_MAPE_LCD[0]))
    
six_methods = np.linspace(2,7,num=6)

# =============================================================================
# plt.figure(2)
# fig, ax = plt.subplots(figsize=(6,4))
# plt.bar(six_methods,QLSEP_change_diff_LCD,align='center',label = 'Different',color = 'r',alpha = 0.2) # A bar chart
# plt.bar(six_methods,QLSEP_change_same_LCD,align='center',label = 'Same',color = 'b',alpha = 0.2) # A bar chart
# 
# legend = ax.legend(loc='upper right', shadow=True)
# frame = legend.get_frame()
# frame.set_facecolor('1.0')
# for label in legend.get_texts():
#     label.set_fontsize('medium')
# for label in legend.get_lines():
#     label.set_linewidth(1.5)  # the legend line width
# 
# plt.xlabel('Methods')
# plt.ylabel('MAPE increase/decrease (%)')
# plt.ylim(-7,7)
# #plt.title('MAPE increase/decrease from baseline (EWMA-NREL)')
# plt.grid()
# plt.savefig('MAPE_QLSEP_LCD_7methods_inc_dec(same).png', dpi = 200)
# plt.show()
# =============================================================================
