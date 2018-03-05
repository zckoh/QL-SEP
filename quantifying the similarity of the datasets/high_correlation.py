# -*- coding: utf-8 -*-
"""
Created on Mon Mar 05 14:34:13 2018

Highly correlated data (actual) 20 days

@author: zckoh
"""


import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)
execfile("./../QLSEP_class.py")


#Importing True values collected from both boxes(Samples per Min)
tmp = []
lux_B1 = []
slot = 30

for i in range(1,21):
    with open("./../highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

#Initialise the variables list
distance = []
sum_datapoints1 = []
similarity = []

for x in range(len(lux_B1)):
    for y in range(len(lux_B2[x])):
        #Find Euclidean distance for each data point
        d_tmp = np.sqrt(np.square(lux_B2[x][y]-lux_B1[x][y]))
        distance.append(d_tmp)
        #Sum of datapoints in Box 1
        sum_datapoints1.append(lux_B1[x][y])
    #Compute the Similarity for each day
    similarity_tmp = np.sum(distance)/np.sum(sum_datapoints1)
    #Store the computed similarity value
    similarity.append(similarity_tmp)
    #Reset the temporary lists
    sum_datapoints1 = []
    distance = []



print similarity
print np.mean(similarity)
print lux_B1[13]
print lux_B2[13]


