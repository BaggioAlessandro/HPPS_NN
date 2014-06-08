import random
import datetime
import numpy as np
import os
import matplotlib as plt


MAX_LAG = 200
N_NEURONS = 10
RESOLUTION = 0.001
ROUND = RESOLUTION *0.05

def hist3(my_list, fine):
    hist = np.zeros((1,fine+1), dtype=int)
    hist[0][my_list[:]] += 1
    return hist[0]
    
def mySave_2D (my_matrix,fileName):
    file = open(path+ fileName +".txt", "w")
    for i in range(0,my_matrix.shape()[0]):
        for j in range(0,my_matrix.shape()[1]):
            file.write(str(my_matrix[i][j]) + " ")
        
        file.write("\n")    
    file.close
    
def mySave_1D (my_matrix,fileName):
    file = open(path+ fileName +".txt", "w")
    for i in range(0,my_matrix.size):
        file.write(str(my_matrix[i]) + " ")
        file.write("\n")    
    file.close

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

delta_tot = datetime.timedelta()
a = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/A.csv", dtype=np.float32,delimiter = ',')
b = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/B.csv", dtype=np.float32,delimiter = ',')

fine = (max (a[-1], b[-1])) / RESOLUTION

data= np.loadtxt(path + "01.txt", dtype=int)
edges_ecc = np.zeros((N_NEURONS,N_NEURONS))
edges_ini = np.zeros((N_NEURONS,N_NEURONS))
for i in range(0,N_NEURONS):
    t1_binned = data[i][:]
    xx = np.arange(-30,30)
    for j in range(0,N_NEURONS):
        t2_binned = data[j][:]
        xc = np.zeros(2*MAX_LAG+1)
        #lag di 0 rimane a 0
        for k in range(1,MAX_LAG+1):
            xc[MAX_LAG-k] = np.sum(t1_binned[k:-1]*t2_binned[0:-k-1])

        #t1 e t2 invertiti
        for k in range(1,MAX_LAG+1):
            xc[k+MAX_LAG] = np.inner(t2_binned[k:-1],t1_binned[0:-k-1])

        xcb=xc[MAX_LAG-29:MAX_LAG+31]
        n = 2*MAX_LAG
        mean = np.mean(xc)
        stdev = np.sqrt(np.var(xc))

        flag1=0
        flag2=0
        massimo1=0
        massimo2=0

        for h in range(31,35):
            if((xcb[h]>(mean+stdev*3.09)) and (xcb[h]>massimo1)):
                massimo1=xcb[h]
                istante=xx[h]
                flag1 = 1


        if(flag1 != 0):
            edges_ecc[i][j] = 1


        #Same for negative time shifts
        for h in range(25,30):
            if((xcb[h]>(mean+stdev*3.09)) and (xcb[h]>massimo2)):
                massimo2=xcb[h]
                istante=xx[h]
                flag2=1

        if(flag2 != 0):
            edges_ecc[j][i] = 1

        #TROUGHS: if the short-latency waveform is exponential, we consider the
        #connection existing and inhibitory

        #fitting an exponential curve on the data between 1 ms and 10 ms.
        #Unfortunately the only way to fit an exponential in matlab is finding the
        #polynomial fitting for the logarithm of xcb which gives the coefficients
        #for the exponential function
        #For a positive number of shifts
        x_exp = np.arange(32,52)
        y_exp=xcb[32:52]

        #y_exp=y_exp'

        P= np.polyfit(x_exp, np.log(y_exp), 1)
        fun=np.polyval(P,x_exp)
        #if the fitting is good enough, we can say the curve is an exponential and
        #the trough is found.

        yresid = y_exp - fun
        SSresid=np.sum(np.power(yresid, 2))
        SStotal=(y_exp.size-1)*np.var(y_exp)
        #R2 is defined as 1-the residual sum of squares/N-1*variance (see
        #statistics and linear regression for more information)
        rsq=1-SSresid/SStotal
    
        if(rsq>0.9):
            edges_ini[i][j] = 1


        #Same for a negative number of shifts
        x_exp = np.arange(10,30)
        y_exp=xcb[x_exp]
        y_log = np.log(y_exp)
        #y_exp=y_exp'

        P= np.polyfit(x_exp, y_log, 1)
        fun=np.polyval(P,x_exp)
        #if the fitting is good enough, we can say the curve is an exponential and
        #the trough is found.

        yresid = y_log - fun
        SSresid=np.sum(np.power(yresid, 2))
        SStotal=(y_exp.size-1)*np.var(y_log)
        #R2 is defined as 1-the residual sum of squares/N-1*variance (see
        #statistics and linear regression for more information)
        rsq=1-SSresid/SStotal

        if(rsq>0.8):
            edges_ini[j][i] = 1

print(edges_ecc)
