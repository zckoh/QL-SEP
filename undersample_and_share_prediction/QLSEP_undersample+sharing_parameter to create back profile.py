# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:47:50 2018

@author: zckoh
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y

checking_slot = 80

tmp = []
lux_B1 = []
slot = 30
"""getting data"""
for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

EWMA_val = np.array([[float(0)]*(1440/slot)]*days)

"""Set to have intertwine sampling """
tmp_int = []
lux_b1_int = []
lux_b2_int = []
min_btw_slot_intertwine = 60
for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]        
    lux_b1_int.append([float(a) for a in tmp_int])
    tmp_int = []
    
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_int.append(lines)
        tmp_int = [w.replace('\n', '') for w in tmp_int]
    
    lux_b2_int.append([float(s) for s in tmp_int])    
    tmp_int = []
    
tmp_intt = []
lux_b1_intt = []
lux_b2_intt = []

for i in range(1,21):
    with open("./highly correlated data/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
        
    lux_b1_intt.append([float(b) for b in tmp_intt])
    tmp_intt = []
    
    with open("./highly correlated data/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 30, None, min_btw_slot_intertwine)
        for lines in fifthlines:
            tmp_intt.append(lines)
        tmp_intt = [w.replace('\n', '') for w in tmp_intt]
    
    lux_b2_intt.append([float(i) for i in tmp_intt])
    tmp_intt = []


class QLSEP_node:
    def __init__(self,learning_rate,alpha,N):
        """Return a QLSEP node object"""
        self.learning_rate = learning_rate
        self.alpha = alpha
        self.N = N
        self.EWMA_val = np.array([[float(0)]*(1440/slot/2)]*days)
        self.QLSEP_val = np.array([[float(0)]*(1440/slot/2)]*days)
        self.PER = np.array([float(0)]*12)
        self.PER_list = []
        self.PE_list = np.array([float(0)]*12)
        self.OPER = 1
        self.OPER_list = []
        self.P = []
        for i in range(N):
            self.P.append(i+1)
        self.PER_previous = 0
        self.PE = 0
        self.q_values = np.array([float(1)]*(1440/slot/2))
        
        """Variables below used for sharing Q values"""
        self.contention_flag = 0
        """need to know how many neighbours"""
        self.received_PER = np.array([float(0)*1])
        self.requests = np.array([float(0)*1])
        self.received_q_val = np.array([float(0)*1])
        self.weights_4_neighbours = np.array([float(1)])
        

    def EWMA(self,x,y,lux):
        """Predicts EWMA for 1 slot"""
        self.EWMA_val[x][y] = self.alpha*float(self.EWMA_val[x][y-1]) + (1-self.alpha)*float(lux)
        return self.EWMA_val[x][y]
    
    def Calculate_PER(self,x,y,lux):
        self.PER = self.PER[1:]
        self.PE_list = self.PE_list[1:]
        #find PER of the previous slot
        #if Lux is 0, no need to calculate PER (set to 0)
        if(lux==0):
            self.PER_previous = 0
            self.PE = 0
            if(y==checking_slot):
                self.PER_list.append(self.PER_previous)
        else: #calculate PER for previous slot
            self.PER_previous = np.absolute(safe_div((lux-self.QLSEP_val[x][y-1]),self.QLSEP_val[x][y-1]))
            self.PE = safe_div((lux-self.QLSEP_val[x][y-1]),self.QLSEP_val[x][y-1])
            if(y==checking_slot):
                print "PER_previous : %s"% self.PER_previous
                print "OPER : %s" % self.OPER
                self.PER_list.append(self.PER_previous)
        #Append to the PER list
        self.PER = np.append(self.PER,self.PER_previous)
        self.PE_list = np.append(self.PE_list,self.PE)
    
    def Q_val_update(self,x,y):
        if(self.PER_previous < self.OPER):
            reward = 1
            self.q_values[y] = self.q_values[y] + self.learning_rate*(reward-self.q_values[y])
            if(y==checking_slot):
                print "Q_value at time: %s " % self.q_values[y]
        #if now prediction error getting worse than average (Bad)
        else:
            reward = -1
            #Reduce the learning rate aggresively
            learning_rate_aggressive = self.PER_previous*self.learning_rate
            self.q_values[y] = self.q_values[y] + learning_rate_aggressive*(reward-self.q_values[y])
            if(y==checking_slot):
                print "Q_value at time: %s " % self.q_values[y]
        
    def request_Q_val(self):
        return 1
    
    def Pass_Q_val(self,x,y):
        return self.q_values[x][y-1]
    
    def accept_Q_val(self,x,y,q_value):
        self.q_values[x][y] = q_value
        
    def QLSEP_prediction(self,x,y):
        #update new OPER
        self.OPER = np.sum(self.PER)/12
        if(y==checking_slot):
            self.OPER_list.append(self.OPER)
            print self.PER
        sum_dot = 0

        for i in range(1,self.N+1):
            dot = self.PE_list[-(i)]*(self.q_values[y+1-i])*self.P[-i]
            sum_dot += dot
        #calculate DR - average of energy increase/decrease ratio
        #print sum_dot
        DR = sum_dot / np.sum(self.P)
        #calculate QLSEP value
        #print "DR = %s" % DR 
        self.QLSEP_val[x][y] = (self.EWMA_val[x][y])*(1+DR)

    def receive_request(self,request,PER,address):
        self.received_PER[address] = PER
        self.requests[address] = request

    def receive_q_val(self,q_value,address):
        self.received_q_val[address] = q_value



"""calculate EWMA then combine"""
"""original (Bad model)"""


"""New model"""
#EWMA_val_shared = np.array([[float(0)]*(1440/slot)]*days)
EWMA_val_shared = []
QLSEP_val_shared = []
index = 19
alpha = 0.4
node1 = QLSEP_node(0.01,0.4,3)
node2 = QLSEP_node(0.01,0.4,3)

for x in range(0,days):
    for y in range(0,1440/slot/2):
        """Node 1 predicting"""
        node1.EWMA(x,y,lux_b1_int[x-1][y])
        node1.Calculate_PER(x,y,lux_b1_int[x][y-1])
        node1.Q_val_update(x,y)
        node1.QLSEP_prediction(x,y)
        
        """Node 2 predicting"""
        node2.EWMA(x,y,lux_b2_intt[x-1][y])
        node2.Calculate_PER(x,y,lux_b2_intt[x][y-1])
        node2.Q_val_update(x,y)
        node2.QLSEP_prediction(x,y)

for x in range(0,days):
    EWMA_val_shared.append([item for pair in zip(node1.EWMA_val[x], node2.EWMA_val[x]) for item in pair])
    QLSEP_val_shared.append([item for pair in zip(node1.QLSEP_val[x], node2.QLSEP_val[x]) for item in pair])


lux_tmp_b1 = []
lux_pre_EWMA_tmp_b1 = []
lux_pre_QLSEP_tmp_b1 = []
QLSEP_val_shared_tmp_b1 = []

lux_tmp_b2 = []
lux_pre_EWMA_tmp_b2 = []
lux_pre_QLSEP_tmp_b2 = []
    
how_many = 0

    #do for ten days
for i in range(how_many,len(lux_B1)):
    EWMA_10 = [float(j) for j in node1.EWMA_val[i]]
    QLSEP_10 = [float(j) for j in node1.QLSEP_val[i]]
    shared = [float(j) for j in QLSEP_val_shared[i]]
    #append all seen values into the same array to get the 10 days
    lux_pre_EWMA_tmp_b1 += EWMA_10
    lux_tmp_b1 +=lux_B1[i]
    lux_pre_QLSEP_tmp_b1 += QLSEP_10
    QLSEP_val_shared_tmp_b1 += shared

    EWMA_10 = [float(j) for j in node2.EWMA_val[i]]
    QLSEP_10 = [float(j) for j in node2.QLSEP_val[i]]
    #append all seen values into the same array to get the 10 days
    lux_pre_EWMA_tmp_b2 += EWMA_10
    lux_tmp_b2 +=lux_B1[i]
    lux_pre_QLSEP_tmp_b2 += QLSEP_10

a = np.amax(lux_tmp_b1)
b = a*0.05

MAPE_QLSEP_overall = 0
QLSEP_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(lux_pre_QLSEP_tmp_b1)):
    if(lux_tmp_b1[i*2]!=0):
        if(lux_tmp_b1[i*2]>b):
            QLSEP_MAPE_N_COUNTER += 1
            MAPE_QLSEP_overall += abs((lux_tmp_b1[i*2]-lux_pre_QLSEP_tmp_b1[i])/lux_tmp_b1[i*2])
                    
MAPE_QLSEP_overall = MAPE_QLSEP_overall*100/QLSEP_MAPE_N_COUNTER
#MAPE_QLSEP_overall = MAPE_QLSEP_overall*100/(1440*len(lux)/slot)
#print QLSEP_MAPE_N_COUNTER
print "MAPE (QLSEP) overall = %s%% (Box 1 alone)"% MAPE_QLSEP_overall

MAPE_QLSEP_overall = 0
QLSEP_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(QLSEP_val_shared_tmp_b1)):
    if(lux_tmp_b1[i]!=0):
        if(lux_tmp_b1[i]>b):
            QLSEP_MAPE_N_COUNTER += 1
            MAPE_QLSEP_overall += abs((lux_tmp_b1[i]-QLSEP_val_shared_tmp_b1[i])/lux_tmp_b1[i])
                    
MAPE_QLSEP_overall = MAPE_QLSEP_overall*100/QLSEP_MAPE_N_COUNTER
print "MAPE (QLSEP) overall = %s%% (Box 1 shared)"% MAPE_QLSEP_overall

time = np.linspace(1,1440, num = 1440/slot)
timeb1 = []
timeb2 = []

for i in range(len(time)):
    if(i%2==0):
        timeb1.append(time[i])
    else:
        timeb2.append(time[i])



plt.figure(1)
fig, ax = plt.subplots(figsize=(7,4))
ax.plot(time,lux_B1[index],'g',label = 'Actual Box 1')
#ax.plot(time,lux_B2[index],'y',label = 'Actual Box 2')
#ax.plot(timeb1,lux_b1_int[index],'bx',label = 'Box 1')
ax.plot(timeb1,node1.QLSEP_val[index],'b',label = 'Undersample (no sharing)')
#ax.plot(timeb2,node2.QLSEP_val[index],'rx',label = 'QLSEP Box 2(Bad)')
ax.plot(time,EWMA_val_shared[index],'y',label = 'EWMA')
ax.plot(time,QLSEP_val_shared[index],'r',label = 'Undersample + sharing')
"""
ax.plot(timeb2,node1.EWMA_val[index],'b',label = 'EWMA Box 1(Bad)')
ax.plot(time,EWMA_val_shared[index],'r',label = 'EWMA Box 1')
"""
#ax.plot(time2,EWMA_valb1[index],'rx',label='EWMA')
legend = ax.legend(loc='upper right', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('1.0')
for label in legend.get_texts():
    label.set_fontsize('medium')
for label in legend.get_lines():
    label.set_linewidth(1.5)  # the legend line width
plt.xlabel('Time(Hour)')
plt.ylabel('Light Intensity (klux)')
plt.ylim([0,15])
plt.title('Day %s (Box 1)' % str(index+1))
#plt.savefig('cloudy_day_plot.png', bbox_inches='tight')
