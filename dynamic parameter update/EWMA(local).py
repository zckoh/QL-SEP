# -*- coding: utf-8 -*-
"""
Created on Sun Mar 04 14:10:21 2018

Dynamic update for local EWMA prediction model
Alpha adapt


@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
execfile("./../QLSEP_class.py")
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


"""Define the 24 slots Model"""
EWMA_valb1_static = np.array([[float(0)]*(1440/slot/2)]*days)
EWMA_valb1_dynamic_a1 = np.array([[float(0)]*(1440/slot/2)]*days)
EWMA_valb1_dynamic_a2 = np.array([[float(0)]*(1440/slot/2)]*days)

#PER of previous slot
PER_a1 = 0
PER_a2 = 0

"""Initialise the parameters"""
index = 5
alpha = 0.4

a1 = 0.4
increment = 0.001
a2 = a1-increment
"""
for x in range(0,days):
    for y in range(0,1440/slot/2):
        #Static parameter model
        EWMA_valb1_static[x][y] = alpha*(EWMA_valb1_static[x][y-1]) + (1-alpha)*(float(lux_B1[x-1][y]))
        
        #using alpha-adapt algo
        #a1
        EWMA_valb1_dynamic_a1[x][y] = a1*(EWMA_valb1_dynamic_a1[x][y-1]) + (1-a1)*(float(lux_B1[x-1][y]))
        #a2
        EWMA_valb1_dynamic_a2[x][y] = a2*(EWMA_valb1_dynamic_a2[x][y-1]) + (1-a2)*(float(lux_B1[x-1][y]))
        
        #calculate PER
        min_threshold = np.amax(lux_B1[x])*0.03
        if(lux_B1[x][y]<=min_threshold):
            PER_previous_a1 = 0
            PER_previous_a2 = 0
        else: #calculate PER for previous slot
            PER_previous_a1 = np.absolute(safe_div((lux_B1[x][y]-EWMA_valb1_dynamic_a1[x][y]),EWMA_valb1_dynamic_a1[x][y]))
            PER_previous_a2 = np.absolute(safe_div((lux_B1[x][y]-EWMA_valb1_dynamic_a2[x][y]),EWMA_valb1_dynamic_a2[x][y]))

        #Update the parameter during the day
        if(lux_B1[x][y]<=min_threshold):
            a2 = a2
        else:
            if(PER_previous_a1>PER_previous_a2): #Current alpha good
                if(a2<=a1):
                    a2 = a2 - increment
                elif(a2>a1):
                    a2 = a2 + increment

            elif(PER_previous_a1<PER_previous_a2): #current alpha bad
                if(a2<=a1):
                    a2 = a2 + increment
                elif(a2>a1):
                    a2 = a2 - increment
            else:
                a2 = a2 + increment
                
        #print "slot = %s\tPER_a1 = %s\tPER_a2 = %s\tA1 = %s\tA2 = %s"%(y,PER_previous_a1,PER_previous_a2,a1,a2)
"""
for x in range(0,days):
    for y in range(0,1440/slot/2):
        min_threshold = np.amax(lux_B1[x])*0.03
        if(lux_B1[x][y-1]<=min_threshold):
            PER_previous_a1 = 0
            PER_previous_a2 = 0
        else: #calculate PER for previous slot
            PER_previous_a1 = np.absolute(safe_div((lux_B1[x][y-1]-EWMA_valb1_dynamic_a1[x][y-1]),EWMA_valb1_dynamic_a1[x][y-1]))
            PER_previous_a2 = np.absolute(safe_div((lux_B1[x][y-1]-EWMA_valb1_dynamic_a2[x][y-1]),EWMA_valb1_dynamic_a2[x][y-1]))

        #Update the parameter during the day
        if(lux_B1[x][y-1]<=min_threshold):
            a2 = a2
        else:
            if(PER_previous_a1>PER_previous_a2): #Current alpha good
                if(a2<=a1):
                    a2 = a2 - increment
                elif(a2>a1):
                    a2 = a2 + increment

            elif(PER_previous_a1<PER_previous_a2): #current alpha bad
                if(a2<=a1):
                    a2 = a2 + increment
                elif(a2>a1):
                    a2 = a2 - increment
            else:
                a2 = a2 + increment
        #Static parameter model
        EWMA_valb1_static[x][y] = alpha*(EWMA_valb1_static[x][y-1]) + (1-alpha)*(float(lux_B1[x-1][y]))
        
        #using alpha-adapt algo
        #a1
        EWMA_valb1_dynamic_a1[x][y] = a1*(EWMA_valb1_dynamic_a1[x][y-1]) + (1-a1)*(float(lux_B1[x-1][y]))
        #a2
        EWMA_valb1_dynamic_a2[x][y] = a2*(EWMA_valb1_dynamic_a2[x][y-1]) + (1-a2)*(float(lux_B1[x-1][y]))
        
        #calculate PER

                
                
[mape_a2,no_a2] = MAPE_overall(lux_B1,EWMA_valb1_dynamic_a2,days)
[mape_a1,no_a1] = MAPE_overall(lux_B1,EWMA_valb1_dynamic_a1,days)

[mape_original,no_original] = MAPE_overall(lux_B1,EWMA_valb1_static,days)

print "24 slots"
print "MAPE = %s%% , N = %s (using a1)" % (mape_a1,no_a1)
print "MAPE = %s%% , N = %s (using a2)" % (mape_a2,no_a2)
print "MAPE = %s%% , N = %s (static)" % (mape_original,no_original)




#plot the prediction
time48 = np.linspace(1,1440, num = 1440/slot)
time24 = np.linspace(1,1440, num = 1440/slot/2)

index = 80

plt.figure(1)
fig, ax = plt.subplots(figsize=(7.5,4))
ax.plot(time48,lux_original[index],'g',label = 'Actual (48 slots)')
ax.plot(time24 ,EWMA_valb1_dynamic_a2[index],'r',label = 'a2')
ax.plot(time24,EWMA_valb1_dynamic_a1[index],'b',label = 'a1')

legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Min)')
plt.ylabel('Light Intensity (klux)')
plt.title('Box day %s (NREL data)' % str(index+1))
plt.grid()
plt.show()




