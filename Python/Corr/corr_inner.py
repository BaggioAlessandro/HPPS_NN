import random
import datetime
import numpy as np
import os
import matplotlib as plt


MAX_LAG = 200

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

fine = (max (a[-1], b[-1])) / 0.001



a += 0.0005 #serve per arrotondare
a *= 1000
a = np.int32(a)
b += 0.0005 #serve per arrotondare
b *= 1000
b = np.int32(b)

fine += 0.5 #serve a arrotondare
fine = int(fine)

t1_binned = hist3(a, 300000)
t2_binned = hist3(b, 300000)

xc = np.zeros(2*MAX_LAG+1) 

delta_tot = datetime.timedelta()
time1= datetime.datetime.now()
for i in range(0,MAX_LAG+1):
    xc[MAX_LAG-i] = np.sum(t1_binned[i:-1]*t2_binned[0:-i-1])
print(xc[200])
print(xc[201])
#t1 e t2 invertiti
for i in range(1,MAX_LAG+1):
    xc[i+MAX_LAG] = np.inner(t2_binned[i:-1],t1_binned[0:-i-1])

mySave_1D(xc,'lucaculo')
#lag a 0 messa a 0
xc[200] = 0
xcb=xc[MAX_LAG-29:MAX_LAG+31]
xx = np.arange(-30,30)
n = 2*MAX_LAG
mean = np.mean(xc)
stdev = np.sqrt(np.var(xc))

flag1=0
flag2=0
massimo1=0
massimo2=0

for i in range(31,35):
    if((xcb[i]>(mean+stdev*3.09)) and (xcb[i]>massimo1)):
        massimo1=xcb[i]
        istante=xx[i]*0.5
        flag1 = 1


if(flag1 != 0):
    print('Peak at ' + str(istante) +' ms. An excitatory connection is present.\n')


#Same for negative time shifts
for i in range(25,30):
    if((xcb[i]>(mean+stdev*3.09)) and (xcb[i]>massimo2)):
        massimo2=xcb[i]
        istante=xx[i]*0.5
        flag2=1

if(flag2 != 0):
    print('Peak at ' + str(istante) +' ms. An excitatory connection is present.\n')

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
    print('There is an inhibitory connection.\n')


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
    print('There is an inhibitory connection.\n')



delta_tot = time2-time1
print(delta_tot)
