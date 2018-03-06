# -*- coding: utf-8 -*-
"""
Created on Tue Jan 02 18:05:09 2018

@author: zckoh

QLSEP model (With 2 nodes sharing)
(Actual Data)

"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)
execfile("./../QLSEP_class.py")

index = 18

#Importing True values collected from both boxes(Samples per Min)
tmp = []
lux_B1 = []
slot = 60

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

#No sharing 


node1_ns = QLSEP_node(0.003,0.4,3,slot,days,50)
node2_ns = QLSEP_node(0.003,0.4,3,slot,days,50)

for x in range(0,days):
    for y in range(0,1440/slot):
        node1_ns.EWMA(x,y,lux_B1[x-1][y])
        node1_ns.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1_ns.Q_val_update(x,y)
        node1_ns.QLSEP_prediction(x,y)
        
        node2_ns.EWMA(x,y,lux_B2[x-1][y])
        node2_ns.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2_ns.Q_val_update(x,y)
        node2_ns.QLSEP_prediction(x,y)
        
#sharing
        
"""(learning_rate, alpha, N, Min per slot, days, checking_slot)"""
node1 = QLSEP_node(0.003,0.4,3,slot,days,50)
node2 = QLSEP_node(0.003,0.4,3,slot,days,50)

sharing_flag = 1
total_average = []
total_shared_counts = 0

for x in range(0,days):
    total_shared_counts = 0
    for y in range(0,1440/slot):
        """Node 1 predicting"""
        node1.EWMA(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1],(np.amax(lux_B1[x])*0.03))
        node1.contention_flag =  0
        node1.Q_val_update(x,y)
        #Set a flag to request
        if(node1.PER_previous > 0.5):
            node1.contention_flag = 1
        node1.QLSEP_prediction(x,y)
        
        
        
        """Node 2 predicting"""
        node2.EWMA(x,y,lux_B2[x-1][y])
        node2.Calculate_PER(x,y,lux_B2[x][y-1],(np.amax(lux_B2[x])*0.03))
        node2.contention_flag = 0
        node2.Q_val_update(x,y)
        #Set a flag to request
        if(node2.PER_previous > 0.5):
            node2.contention_flag = 1
        node2.QLSEP_prediction(x,y)
        
        
        if(sharing_flag==1):
            sharing_flag = 0
            
            """Now check for contention flags"""
            if(node1.contention_flag):
                total_shared_counts += 1
                """Send Request(contention_flag) + PER(PER_previous) as broadcast to that cluster"""
                """All other nodes within cluster receives the broadcast"""
                node2.receive_request(node1.contention_flag,node1.PER_previous,0)
            if(node2.contention_flag):
                
                node1.receive_request(node2.contention_flag,node2.PER_previous,0)
        
            """Check/Compare PER of all the received"""
            """If receiver better prediction than sender"""
            if(node1.contention_flag):
                if(node2.PER_previous < node1.PER_previous):
                    """send the Q value to the sender"""
                    node1.receive_q_val(node2.q_values[y],0)
                else:
                    """Send a zero value to the sender"""
                    node1.receive_q_val(0,0)
        
            if(node2.contention_flag):
                if(node1.PER_previous < node2.PER_previous):
                    """send the Q value to the sender"""
                    node2.receive_q_val(node1.q_values[y],0)
                else:
                    """Send a zero value to the sender"""
                    node2.receive_q_val(0,0)
        
            """After all Q values have been sent and received"""
            """Update its Q value using the weighted average"""
        
        
            if(node1.contention_flag):
                """node 1"""
                #if Q value received is empty, use original predicted q value
                if(node1.received_q_val[0] == 0):
                    node1.received_q_val[0] = node1.q_values[y]
                    #calculate weighted average
                    weighted_sum_node1 = 0
                    for i in range(len(node1.received_q_val)):
                        weighted_sum_node1 += node1.received_q_val[i] * node1.weights_4_neighbours[i]
                        weighted_avg_node1 = weighted_sum_node1/(1)
                else:
                    weighted_sum_node1 = 0
                    for i in range(len(node1.received_q_val)):
                        weighted_sum_node1 += node1.received_q_val[i] * node1.weights_4_neighbours[i]
                        weighted_avg_node1 = weighted_sum_node1/(1)
                #Update that Q value
                node1.q_values[y] = weighted_avg_node1
            if(node2.contention_flag):
                """node 2"""
                #if Q value received is empty, use original predicted q value
                if(node2.received_q_val[0] == 0):
                    node2.received_q_val[0] = node2.q_values[y]
                    #calculate weighted average
                    weighted_sum_node2 = 0
                    for i in range(len(node2.received_q_val)):
                        weighted_sum_node2 += node2.received_q_val[i] * node2.weights_4_neighbours[i]
                        weighted_avg_node2 = weighted_sum_node2/(1)
                else:
                    weighted_sum_node2 = 0
                    for i in range(len(node1.received_q_val)):
                        weighted_sum_node2 += node2.received_q_val[i] * node2.weights_4_neighbours[i]
                        weighted_avg_node2 = weighted_sum_node2/(1)
                #Update that Q value
                node2.q_values[y] = weighted_avg_node2
        
        sharing_flag += 1
    total_average.append(total_shared_counts)

total_average = np.array(total_average)
print total_average
print total_average.mean()
time = np.linspace(1,1440, num = 1440/slot)
    

time = np.linspace(1,1440, num = 1440/slot)


plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,node1.EWMA_val[index],'r',label='EWMA')
ax.plot(time,node1.QLSEP_val[index],'b',label= 'QLSEP')
ax.plot(time,lux_B1[index],'g',label='Actual')
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
plt.grid()
plt.title('Light intensity Box 1 (day = %s)' % str(index+1))


plt.figure(2)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,node2.EWMA_val[index],'r',label='EWMA')
ax.plot(time,node2.QLSEP_val[index],'b',label= 'QLSEP')
ax.plot(time,lux_B2[index],'g',label='Actual')
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.ylim([0,15])
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')
plt.grid()
plt.title('Light intensity Box 2 (day = %s)' % str(index+1))






"""Plot for 20 days"""
lux_tmp_b1 = []
lux_pre_EWMA_tmp_b1 = []
lux_pre_QLSEP_tmp_b1 = []


lux_tmp_b2 = []
lux_pre_EWMA_tmp_b2 = []
lux_pre_QLSEP_tmp_b2 = []

how_many = 0

#do for ten days
for i in range(how_many,len(lux_B1)):
    EWMA_10 = [float(j) for j in node1.EWMA_val[i]]
    QLSEP_10 = [float(j) for j in node1.QLSEP_val[i]]
    #append all seen values into the same array to get the 10 days
    lux_pre_EWMA_tmp_b1 += EWMA_10
    lux_tmp_b1 +=lux_B1[i];
    lux_pre_QLSEP_tmp_b1 += QLSEP_10
    
    EWMA_10 = [float(j) for j in node2.EWMA_val[i]]
    QLSEP_10 = [float(j) for j in node2.QLSEP_val[i]]
    #append all seen values into the same array to get the 10 days
    lux_pre_EWMA_tmp_b2 += EWMA_10
    lux_tmp_b2 +=lux_B1[i];
    lux_pre_QLSEP_tmp_b2 += QLSEP_10
    



print "========================================"
print "No sharing (Original)"
print "========================================\n"

[mape_b1_QLSEP_ns, no_b1_QLSEP_ns] = MAPE_overall(lux_B1,node1_ns.QLSEP_val,days)
[mape_b1_EWMA_ns, no_b1_EWMA_ns] = MAPE_overall(lux_B1,node1_ns.EWMA_val,days)

[mape_b2_QLSEP_ns, no_b2_QLSEP_ns] = MAPE_overall(lux_B2,node2_ns.QLSEP_val,days)
[mape_b2_EWMA_ns, no_b2_EWMA_ns] = MAPE_overall(lux_B2,node2_ns.EWMA_val,days)

print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA_ns,no_b1_EWMA_ns)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_EWMA_ns,no_b2_EWMA_ns)


print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP_ns,no_b1_QLSEP_ns)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_QLSEP_ns,no_b2_QLSEP_ns)


print "========================================"
print "Sharing Q values based on PER"
print "========================================\n"


[mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1,node1.QLSEP_val,days)
[mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1,node1.EWMA_val,days)

[mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2,node2.QLSEP_val,days)
[mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2,node2.EWMA_val,days)



print "EWMA prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_EWMA,no_b1_EWMA)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_EWMA,no_b2_EWMA)


print "QLSEP prediction"
print "MAPE = %s%% , N = %s (Box 1)" % (mape_b1_QLSEP,no_b1_QLSEP)
print "MAPE = %s%% , N = %s (Box 2)\n" % (mape_b2_QLSEP,no_b2_QLSEP)




time_20 = np.linspace(0,1440*(len(lux_B1)-how_many), num = 1440*(len(lux_B1)-how_many)/slot)


plt.figure(3)
fig, ax = plt.subplots(figsize=(20,4))
ax.plot(time_20,lux_pre_EWMA_tmp_b1,'r',label='EWMA')
ax.plot(time_20,lux_pre_QLSEP_tmp_b1,'b',label= 'QLSEP')
ax.plot(time_20,lux_tmp_b1,'g',label='Actual')
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.ylim([0,30])
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')
plt.grid()
plt.title('Light intensity Box 1 For 20 days')





plt.figure(4)
fig, ax = plt.subplots(figsize=(20,4))
ax.plot(time_20,lux_pre_EWMA_tmp_b2,'r',label='EWMA')
ax.plot(time_20,lux_pre_QLSEP_tmp_b2,'b',label= 'QLSEP')
ax.plot(time_20,lux_tmp_b2,'g',label='Actual')
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.ylim([0,30])
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')
plt.grid()
plt.title('Light intensity Box 2 For 20 days')
