import random
import datetime
import numpy as np
import os

def hist3(my_list, fine):
    hist = np.zeros((1,fine), dtype=int)
    hist[0][my_list[:]] += 1
    return hist

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

a = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Nuovo/A.csv", dtype=np.float32,delimiter = ',')
b = np.loadtxt(path + "/DatiReali/Rete_10/Modello_Nuovo/B.csv", dtype=np.float32,delimiter = ',')

fine = (max (a[len(a) - 1], b[len(b) - 1])) / 0.0001


t1_binned = hist3(a, fine)
t2_binned = hist3(b, fine)

xc = np.correlate(t1_binned , t2_binned)

print (xc)