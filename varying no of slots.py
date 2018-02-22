# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:39:01 2018

Vary the no of slots per day and calculating its MAPE

No sharing of parameters

@author: zckoh
"""
import numpy as np
import matplotlib.pyplot as plt
import itertools

from QLSEP_class import QLSEP_node

np.set_printoptions(threshold=np.nan)

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

"""Import data"""
tmp = []
lux_B1 = []
slot = 30
for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

"""Different sampling frequency"""
lux_60min = []
lux_90min = []
lux_120min = []

tmp_60 = []
tmp_90 = []
tmp_120 = []

#save for each 2,3,4 times
for x in range(len(lux_B1)):
    for i in range(len(lux_B1[x])):
        if(i%2==0):
            tmp_60.append(lux_B1[x][i])
        if(i%3==0):
            tmp_90.append(lux_B1[x][i])
        if(i%4==0):
            tmp_120.append(lux_B1[x][i])
    lux_60min.append(tmp_60)
    tmp_60 = []
    lux_90min.append(tmp_90)
    tmp_90 = []
    lux_120min.append(tmp_120)
    tmp_120 = []

"""calculate EWMA + QLSEP for each total slot"""

"""48 slots"""

        



