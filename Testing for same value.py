# -*- coding: utf-8 -*-
"""
Created on Tue Jan 02 18:05:09 2018

@author: zckoh

QLSEP model for single node
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

#Importing True values collected from both boxes(Samples per Min)
lux_b1_true = []
slot_true = 1
tmp = []
for i in range(22,32):
    with open("./Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot_true)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b1_true.append([float(k) for k in tmp])
    tmp = []


days = 10

tmp = []
lux = []
slot = 30
same = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.2, 0.99, 2.15, 2.96, 4.08, 4.93, 5.66, 7.43, 5.92, 6.27, 6.06, 6.57, 5.14, 4.88, 4.78, 2.16, 1.3, 0.38, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
'''
for i in range(22,32):
    with open("./Box 1/%s-11-17.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux.append([float(i) for i in tmp])
    tmp = []
'''
for i in range(0,days):
    lux.append(same)

EWMA_val = np.array([[float(0)]*(1440/slot)]*days)
QLSEP_val = np.array([[float(0)]*(1440/slot)]*days)
alpha = 0.4
index = 8
#initialise Q value (+1) for each slot
q_values = np.array([[float(1)]*(1440/slot)]*days)
N = 3
P = []
for i in range(N):
    P.append(i+1)

OPER = 1
PER = np.array([float(0)]*24)
learning_rate = 0.001
PER_list = [] #contains everydays PER
OPER_list = [] #contains everyday OPER
checking_slot = 19
print len(lux)

for x in range(0,days):
    print "day %s" %x
    for y in range(0,1440/slot):
        #EWMA algorithm
        EWMA_val[x][y] = alpha*float(EWMA_val[x][y-1]) + (1-alpha)*float(lux[x-1][y])
        #EWMA_val[x][y] = alpha*float(EWMA_val[x][y-1]) + (1-alpha)*float(lux[x][y-1])
        #Remove the last slot in PER list
        PER = PER[1:]
        #find PER of the previous slot
        #if Lux is 0, no need to calculate PER (set to 0)
        if(lux[x][y-1]==0):
            PER_previous = 0
            if(y==checking_slot):
                PER_list.append(PER_previous)
        else: #calculate PER for previous slot
            PER_previous = np.absolute(safe_div((lux[x][y-1]-QLSEP_val[x][y-1]),QLSEP_val[x][y-1]))
            if(y==checking_slot):
                print "PER_previous : %s"% PER_previous
                print "OPER : %s" % OPER
                PER_list.append(PER_previous)
            #print lux[x][y-1]
            #print EWMA_val[x][y-1]
            #print QLSEP_val[x][y-1]
            #print np.absolute(safe_div((lux[x][y-1]-EWMA_val[x][y-1]),EWMA_val[x][y-1]))
        #Append to the PER list
        PER = np.append(PER,PER_previous)
        #if now prediction error getting bettter than average (Good)
        #print PER
        if(PER_previous < 1):
            #Dont update the q_values, let it stay the same
            q_values[x][y] = q_values[x-1][y]
        else:
            if(PER_previous < OPER):
                reward = 1
            #if (y==24):
             #   print"OPER = %s" % OPER
              #  print "Previous PER = %s" % PER_previous
               # print "learning_rate = %s" % learning_rate
                #print q_values[x-1][y]
                #q_values[x][y] = q_values[x][y-1] + learning_rate*(reward-q_values[x][y-1])
                #update the q_value of todays slot using yesterdays vale of this slot
                q_values[x][y] = q_values[x-1][y] + learning_rate*(reward-q_values[x-1][y])
                if(y==checking_slot):
                    print "Q_value at time: %s " % q_values[x][y]
        #if now prediction error getting worse than average (Bad)
            else:
                reward = -1
                #Reduce the learning rate aggresively
                learning_rate_aggressive = PER_previous*learning_rate
            #q_values[x][y] = q_values[x][y-1] + learning_rate*(reward-q_values[x][y-1])
            #if (y == 24):
                #print"OPER = %s" % OPER
                #print "Previous PER = %s" % PER_previous
                #print "aggressive reduction of q_value"
                #print "learning_rate = %s" % learning_rate_aggressive
                #print q_values[x-1][y]

                q_values[x][y] = q_values[x-1][y] + learning_rate_aggressive*(reward-q_values[x-1][y])
                if(y==checking_slot):
                    print "Q_value at time: %s " % q_values[x][y]
        #update new OPER
        OPER = np.sum(PER)/24
        #print "OPER = %s" % OPER
        if(y==checking_slot):
            OPER_list.append(OPER)
            print PER
        sum_dot = 0

        for i in range(1,N+1):
            dot = PER[-(i)]*(q_values[x][y+1-i])*P[-i]
            sum_dot += dot
        #calculate DR - average of energy increase/decrease ratio
        #print sum_dot
        DR = sum_dot / np.sum(P)
        #calculate QLSEP value
        #print "DR = %s" % DR 
        QLSEP_val[x][y] = (EWMA_val[x][y])*(1+DR)

print len(PER_list)
#print q_values[index]
time = np.linspace(1,1440, num = 1440/slot)
time_true = np.linspace(1,1440, num = 1440/slot_true)    


plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,EWMA_val[index],'r',label='EWMA')
ax.plot(time,QLSEP_val[index],'b',label= 'QLSEP')
ax.plot(time,lux[index],'g',label='Actual')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.ylim([0,15])
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')
plt.title('Light intensity sampled every 30 mins %s/11/2017' % str(20+index+1))


#PLot OPER against iteration
plt.figure(2)
iterations = np.linspace(1,days, num = days)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(iterations,PER_list,'x')
plt.grid()

#plot PER against iteration
plt.figure(3)
iterations = np.linspace(1,days, num = days)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(iterations,OPER_list,'x')
plt.grid()