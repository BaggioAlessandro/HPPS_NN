import datetime
import numpy as np
import os
from threading import Thread

N_NEURONS = 10

N_CAMP = 1200

N_DELAYS = 100

CONVERSION = 1000000

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

data= np.loadtxt(path + "01.txt", dtype=int)

delay= np.zeros ((N_NEURONS,N_NEURONS,N_DELAYS), dtype=int)

def my_subctract_v3(my_list, item):
    q = my_list - item
    return q
    
def hist3(my_list):
    hist = np.zeros((1,N_DELAYS), dtype=int)
    hist[0][my_list[:]] += 1
    return hist
    
def mySave_3D (my_matrix,fileName):
    file = open(path+ fileName +".txt", "w")
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
          file.write("coppia " + str(i+1) + " " + str(j+1) + "\n")
          for k in range(0, 100):
                file.write(str(my_matrix[i][j][k]) + " ")
          file.write("\n")  
    file.close
    

def mySave_2D (my_matrix,fileName):
    file = open(path+ fileName +".txt", "w")
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            file.write(str(my_matrix[i][j]) + " ")
        
        file.write("\n")    
    file.close
    
def inner_cicle(index1,index2, vi):
    #tupla contenente un array
    qj = np.where(data[j][:] > 0)
        
    #prendo solo il vettore
    vj = qj[0]
    for h in range(0,vi.size):
        q2 = my_subctract_v3(vj[ ((vj >= vi[h]) & (vj<vi[h]+N_DELAYS)) ], vi[h])
            
        if q2.size>0:
               
            my_hist = hist3(q2)
                
            delay[index1][index2][:] += my_hist[0][:]
    
thread_list = []
#inizio calcolo della matrice di delay
for i in range(0,N_NEURONS):
    qi = np.where(data[i][:] > 0)   #tupla contenente un array
    
    #prendo solo il vettore
    for j in range(0,N_NEURONS):
        thread_list.append (Thread(target = inner_cicle, args = (i,j,qi[0] )) )
        thread_list[-1].start()
        
    print(i)

for i in range(len(thread_list)):
    thread_list[i].join()
