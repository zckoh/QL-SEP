# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 16:59:05 2018

Class Definition for QLSEP 

ONLY EDIT THIS for the class

@author: zckoh
"""

import numpy as np

def safe_div(x,y):
    if y == 0:
        return 0
    return x / y


class QLSEP_node:
    def __init__(self,learning_rate,alpha,N,slot,days,checking_slot):
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
        self.checking_slot = checking_slot
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
            if(y==self.checking_slot):
                self.PER_list.append(self.PER_previous)
        else: #calculate PER for previous slot
            self.PER_previous = np.absolute(safe_div((lux-self.QLSEP_val[x][y-1]),self.QLSEP_val[x][y-1]))
            self.PE = safe_div((lux-self.QLSEP_val[x][y-1]),self.QLSEP_val[x][y-1])
            if(y==self.checking_slot):
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
            if(y==self.checking_slot):
                print "Q_value at time: %s " % self.q_values[y]
        #if now prediction error getting worse than average (Bad)
        else:
            reward = -1
            #Reduce the learning rate aggresively
            learning_rate_aggressive = self.PER_previous*self.learning_rate
            self.q_values[y] = self.q_values[y] + learning_rate_aggressive*(reward-self.q_values[y])
            if(y==self.checking_slot):
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
        if(y==self.checking_slot):
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