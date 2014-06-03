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

a = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Nuovo/A.csv", dtype=np.float32,delimiter = ',')
b = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Nuovo/B.csv", dtype=np.float32,delimiter = ',')

fine = (max (a[len(a) - 1], b[len(b) - 1])) / 0.0001


t1_binned = np.histogram(a, range = (0,fine))
t2_binned = np.histogram(b, range = (0,fine))

for i in range (0, 1000):
     print (t1_binned[i])
     
     
#xc = np.correlate(t1_binned, t2_binned, mode = 'valid')
