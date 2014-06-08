import random
import datetime
import numpy as np
import os


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
time1= datetime.datetime.now()
a = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/A.csv", dtype=np.float32,delimiter = ',')
b = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Vecchio/B.csv", dtype=np.float32,delimiter = ',')
print(a[0])
print(a[1])
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

xc = np.zeros(30000) 
print(0)
delta_cross = datetime.timedelta()
time1= datetime.datetime.now()
for i in range(0,MAX_LAG):
    xc[i] = np.inner(t1_binned[i:-1],t2_binned[0:-i-1])
time2= datetime.datetime.now()
delta_cross = time2-time1

print(delta_cross)
#xc = np.correlate(data[0], data[1])
print(xc[0:5])
time2= datetime.datetime.now()
