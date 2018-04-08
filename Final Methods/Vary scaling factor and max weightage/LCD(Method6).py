# -*- coding: utf-8 -*-
"""
Created on Sun Apr 08 21:33:40 2018

@author: zckoh
"""



import numpy as np
import matplotlib.pyplot as plt
import itertools
import matplotlib.mlab as mlab
from mpl_toolkits.mplot3d import axes3d

execfile("./../../QLSEP_class.py")
np.set_printoptions(threshold=np.nan)
np.set_printoptions(precision=4)

class prettyfloat(float):
    def __repr__(self):
        return "%0.4f" % self


#Get the original 48 slots data
tmp = []
lux_B1 = []
slot = 30
"""getting data"""
for i in range(1,21):
    with open("./../../Less Correlated/Box 1/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B1.append([float(i) for i in tmp])
    tmp = []
days = len(lux_B1)

lux_B2 = []

for i in range(1,21):
    with open("./../../Less Correlated/Box 2/day%s.txt" %i , 'r') as f:
        fifthlines = itertools.islice(f, 0, None, slot)
        for lines in fifthlines:
            tmp.append(lines)
        tmp = [w.replace('\n', '') for w in tmp]
    lux_B2.append([float(i) for i in tmp])
    tmp = []

days = len(lux_B1)


#split into 2 arrays  (Box 1)
lux_B1_even = []
lux_B2_odd = []
for x in range(len(lux_B1)):
    even = lux_B1[x][0:][::2]
    lux_B1_even.append(even)
    odd = lux_B2[x][1::][::2]
    lux_B2_odd.append(odd)
    
    





m_w_lst = np.linspace(0,1, num = 22)
MAPE_QLSEP_lst = []


for j in range(len(m_w_lst)):
    param = m_w_lst[j]
    for k in range(len(m_w_lst)):
        max_weightage = m_w_lst[k]
        node1 = QLSEP_node(0.001,0.1,3,60,days,50)
        node2 = QLSEP_node(0.001,0.1,3,60,days,50)
        for x in range(0,days):
            for y in range(0,1440/60):
                #Node1 updates its alpha & predicts for next slot
                node1.alpha_adapt(x,y,(np.amax(lux_B1_even[x])*0.03),lux_B1_even[x][y-1])
                node1.Calculate_PER(x,y,lux_B1_even[x][y-1],(np.amax(lux_B1_even[x])*0.03))

                #Node2 updates its alpha & predicts for next slot
                node2.alpha_adapt(x,y,(np.amax(lux_B2_odd[x])*0.03),lux_B2_odd[x][y-1])
                node2.EWMA_dynamic(x,y,lux_B2_odd[x-1][y])
                node2.Calculate_PER(x,y,lux_B2_odd[x][y-1],(np.amax(lux_B2_odd[x])*0.03))
                node2.Q_val_update(x,y)
                node2.QLSEP_prediction(x,y)
        
                ratio = param*safe_div(node1.PER_previous,node2.PER_previous)
                if(ratio>max_weightage):
                    ratio = max_weightage
                elif(ratio<0):
                    ratio=0
                node1.a2=(max_weightage-ratio)*node2.a2+(1-max_weightage+ratio)*node1.a2

                node1.EWMA_dynamic(x,y,lux_B1_even[x-1][y])
                node1.Q_val_update(x,y)
                node1.QLSEP_prediction(x,y)
                
        [mape_b1_QLSEP, no_b1_QLSEP] = MAPE_overall(lux_B1_even,node1.QLSEP_val,days)
        [mape_b1_EWMA, no_b1_EWMA] = MAPE_overall(lux_B1_even,node1.EWMA_val,days)

        [mape_b2_QLSEP, no_b2_QLSEP] = MAPE_overall(lux_B2_odd,node2.QLSEP_val,days)
        [mape_b2_EWMA, no_b2_EWMA] = MAPE_overall(lux_B2_odd,node2.EWMA_val,days)
        
        MAPE_QLSEP_lst.append(mape_b1_QLSEP)

"""Make the axes"""
C_points = []
W_points = []

for j in range(len(m_w_lst)):
    for k in range(len(m_w_lst)):
        C_points.append(m_w_lst[j])
        W_points.append(m_w_lst[k])

C_points = map(prettyfloat,C_points)
W_points = map(prettyfloat,W_points)
MAPE_QLSEP_lst = map(prettyfloat,MAPE_QLSEP_lst)

#==============================================================================
# print C_points
# print W_points
# print MAPE_QLSEP_lst
# 
#==============================================================================


print "Best parameter value for C and W"
number = np.argmin(MAPE_QLSEP_lst)
print "MAPE = %s " % MAPE_QLSEP_lst[number]
print "Max Weightage = %s " % W_points[number]
print "Scaling Factor = %s" % C_points[number]

MAPE_QLSEP_lst[np.argmax(MAPE_QLSEP_lst)] = MAPE_QLSEP_lst[np.argmax(MAPE_QLSEP_lst)+2]

fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(111,projection='3d')
ax.scatter(W_points,C_points,MAPE_QLSEP_lst)
ax.set_ylabel('C')
ax.set_xlabel(r'$W_{max}$')
ax.set_zlabel('MAPE')
ax.grid()
#plt.title(r'How MAPE varies w.r.t max weightage and scaling factor')
#plt.savefig('MAPE_vs_C_W(Method6).png',dpi=600)


# =============================================================================
# 
# plt.figure(1)
# fig, ax = plt.subplots(figsize=(7.5,4))
# ax.plot(m_w_lst,MAPE_QLSEP_lst,'b')
# plt.xlabel('Weightage')
# plt.ylabel('MAPE (%)')
# plt.grid()
# #plt.savefig('alpha_vs_mape.png', dpi = 600)
# plt.show()
# =============================================================================
