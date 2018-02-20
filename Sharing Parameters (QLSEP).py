# -*- coding: utf-8 -*-
"""
Created on Tue Jan 02 18:05:09 2018

@author: zckoh

QLSEP model (With 2 nodes sharing)
"""

import numpy as np
import matplotlib.pyplot as plt
import itertools
np.set_printoptions(threshold=np.nan)

checking_slot = 80
index = 18


def safe_div(x,y):
    if y == 0:
        return 0
    return x / y
"""
#Importing True values collected from both boxes(Samples per Min)
lux_b1_true = []
slot_true = 1
tmp = []
for i in range(1,21):
    with open("./Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot_true)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    f.close()
    lux_b1_true.append([float(k) for k in tmp])
    tmp = []
"""
tmp = []
lux_B1 = []
slot = 30

for i in range(1,21):
    with open("./Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []



class QLSEP_node:
    def __init__(self,learning_rate,alpha,N):
        """Return a QLSEP node object"""
        self.learning_rate = learning_rate
        self.alpha = alpha
        self.N = N
        self.EWMA_val = np.array([[float(0)]*(1440/slot)]*days)
        self.QLSEP_val = np.array([[float(0)]*(1440/slot)]*days)
        self.PER = np.array([float(0)]*24)
        self.PER_list = []
        self.PE_list = np.array([float(0)]*24)
        self.OPER = 1
        self.OPER_list = []
        self.P = []
        for i in range(N):
            self.P.append(i+1)
        self.PER_previous = 0
        self.PE = 0
        self.q_values = np.array([float(1)]*(1440/slot))
        
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
        self.OPER = np.sum(self.PER)/24
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

"""(learning_rate, alpha, N)"""
node1 = QLSEP_node(0.01,0.4,3)
node2 = QLSEP_node(0.01,0.4,3)
sharing_flag = 0
total_shared_counts = 0

for x in range(0,days):
    total_shared_counts = 0
    for y in range(0,1440/slot):
        """Node 1 predicting"""
        node1.EWMA(x,y,lux_B1[x-1][y])
        node1.Calculate_PER(x,y,lux_B1[x][y-1])
        node1.contention_flag =  0
        node1.Q_val_update(x,y)
        #Set a flag to request
        if(node1.PER_previous > 0.5):
            node1.contention_flag = 1
        node1.QLSEP_prediction(x,y)
        
        
        
        """Node 2 predicting"""
        node2.EWMA(x,y,lux_B2[x-1][y])
        node2.Calculate_PER(x,y,lux_B2[x][y-1])
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
                node1.q_values[x] = weighted_avg_node1
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
    print total_shared_counts
        #check the flag
        #if high for that node, send request and listen request
        #if received a high, send the q value and that PER and accept
        
        
        



print node1.q_values


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
plt.title('Light intensity Box 2 (day = %s)' % str(index+1))




a = np.amax(lux_B1[index])
b = a*0.05

MAPE_QLSEP = 0
QLSEP_MAPE_N_COUNTER = 0

for i in range(len(node1.QLSEP_val[index])):
    if(lux_B1[index][i]!=0):#Must not be 0
        if(lux_B1[index][i]>b):#Must be greater than 5% 
            QLSEP_MAPE_N_COUNTER += 1
            MAPE_QLSEP += abs((lux_B1[index][i]-node1.QLSEP_val[index][i])/lux_B1[index][i])
        #print predicted_val_WCMA[index][i]

print b
#print MAPE_QLSEP
#MAPE_QLSEP = MAPE_QLSEP*100/(1440/slot)
MAPE_QLSEP = MAPE_QLSEP*100/QLSEP_MAPE_N_COUNTER
print QLSEP_MAPE_N_COUNTER
print "MAPE (QLSEP) = %s%%"% MAPE_QLSEP


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
    
    
a = np.amax(lux_tmp_b1)
b = a*0.05

MAPE_QLSEP_overall = 0
QLSEP_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(lux_tmp_b1)):
    if(lux_tmp_b1[i]!=0):
        if(lux_tmp_b1[i]>b):
            QLSEP_MAPE_N_COUNTER += 1
            MAPE_QLSEP_overall += abs((lux_tmp_b1[i]-lux_pre_QLSEP_tmp_b1[i])/lux_tmp_b1[i])

MAPE_QLSEP_overall = MAPE_QLSEP_overall*100/QLSEP_MAPE_N_COUNTER
#MAPE_QLSEP_overall = MAPE_QLSEP_overall*100/(1440*len(lux)/slot)
print QLSEP_MAPE_N_COUNTER
print "MAPE (QLSEP) overall = %s%%"% MAPE_QLSEP_overall


a = np.amax(lux_tmp_b1)
b = a*0.05

MAPE_EWMA_overall = 0
EWMA_MAPE_N_COUNTER = 0
#print predicted_val_WCMA[index]
for i in range(len(lux_tmp_b1)):
    if(lux_tmp_b1[i]!=0):
        if(lux_tmp_b1[i]>b):
            EWMA_MAPE_N_COUNTER += 1
            MAPE_EWMA_overall += abs((lux_tmp_b1[i]-lux_pre_EWMA_tmp_b1[i])/lux_tmp_b1[i])

MAPE_EWMA_overall = MAPE_EWMA_overall*100/EWMA_MAPE_N_COUNTER
#MAPE_EWMA_overall = MAPE_EWMA_overall*100/(1440*len(lux)/slot)

print EWMA_MAPE_N_COUNTER
print "MAPE (EWMA) overall = %s%%"% MAPE_EWMA_overall    



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

#print node1.q_values

'''
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
plt.xlabel('Iterations (days)')
plt.ylabel('OPER')
plt.title('OPER against Iterations')
'''