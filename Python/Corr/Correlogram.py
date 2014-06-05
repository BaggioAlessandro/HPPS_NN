import random
import datetime
import numpy as np
import os

def hist3(my_list, fine):
    hist = np.zeros((1,fine), dtype=int)
    hist[0][my_list[:][0]] += 1
    return hist[0]

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

data= np.loadtxt(path + "01.txt", dtype=int)

a = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/A.csv", dtype=np.float32,delimiter = ',')
b = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/B.csv", dtype=np.float32,delimiter = ',')

#fine = (max (a[len(a) - 1], b[len(b) - 1])) / 0.0001


#t1_binned = np.histogram(a)
#t2_binned = np.histogram(b)

#print(t1_binned[0])
xc = np.zeros(200)
count = 0 
for i in range(-5,5):
    print(i)
    for j in range(0, len(data[0])):
        if not (i+j >= 300000 or i+j < 0):
            xc[count] = xc[count] + data[0][j]*data[1][j+i]
    count = count + 1
    
#xc = np.correlate(data[0], data[1])
print(data[0])
print(xc)
