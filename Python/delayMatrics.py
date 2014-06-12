import random
import datetime
import numpy as np
import os

N_NEURONS = 10

N_CAMP = 1200

CONVERSION = 1000000

factor = 10

INF = 1000000

TRESHOLD = 0.016

delta_tot = datetime.timedelta()
delta_time_load = datetime.timedelta()
delta_time_post = datetime.timedelta()


time_start = datetime.datetime.now()
path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

time_load1 = datetime.datetime.now()

data= np.loadtxt(path + "HPPS_inputData.txt", dtype=int)

time_load2 = datetime.datetime.now()
delta_time_load = time_load2-time_load1

path = path + "Time_Python/Analisi1/"
delay= np.zeros ((N_NEURONS,N_NEURONS,N_CAMP), dtype=int)
delay_n= np.zeros ((N_NEURONS,N_NEURONS,N_CAMP))

def my_subctract_v3(my_list, item):
    q = my_list - item
    q = q[ np.where( q >= 0) ]
    return q
    
def hist3(my_list):
    hist = np.zeros((1,N_CAMP), dtype=int)
    hist[0][my_list[:]] += 1
    return hist
    
def compress():
    d1 = np.zeros ((N_NEURONS, N_NEURONS, np.floor(N_CAMP/factor)+1))
    for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
        d1[:,:,i] = np.sum(delay_n[:,:,i*factor:(i+1)*factor], 2)
    
    if(N_CAMP%factor != 0): 
        i = i+1
        d1[:,:,i]= np.sum(delay[:,:,(i)*f:], 2)
    
    return d1
    
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
 
#inizio calcolo della matrice di delay
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        delta_it = datetime.timedelta()
        time_it_start = datetime.datetime.now()
       
        qi = np.where(data[i][:] > 0)   #tupla contenente un array
        qj = np.where(data[j][:] > 0)
        
        #prendo solo il vettore
        vi = qi[0]  
        vj = qj[0]
        
        for h in range(0,vi.size):
            
            q2 = my_subctract_v3(vj, vi[h])
            
            if q2.size>0:
                
                my_hist = hist3(q2)
                
                delay[i][j][:] += my_hist[0][:] 
                
        time_it_fine = datetime.datetime.now()
        delta_it = time_it_fine - time_it_start
        with open(path+"time_iteration.txt", "a") as file1:
            file1.write(str((delta_it.seconds.real*CONVERSION + delta_it.microseconds.real)/CONVERSION) + " n_1 = " + str(vi.size) + " i = " + str(i) + " j = " + str(j) + "\n")
        
    print(i)
sum = np.sum(delay, 2)

time_post = datetime.datetime.now()            
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(N_CAMP)]
        

d1 = compress()
d1_100 = d1[:,:,0:100]
d1_100n = np.zeros((N_NEURONS,N_NEURONS,100))
sum2 = np.sum(d1_100, 2)
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        d1_100n[i,j,:] = d1_100[i,j,:]/np.sum(d1_100[i,j,:])


mySave_3D(d1, "d1Python")
mySave_3D(d1_100n, "d1_100nPython")
        

conn = np.zeros((N_NEURONS,N_NEURONS))
conn_cum = np.zeros((N_NEURONS,N_NEURONS))
conn_time= INF * np.ones((N_NEURONS,N_NEURONS))
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
      q = np.where(d1_100n[i,j,:]>=TRESHOLD)
      q = q[0]
      print(q)
      if q.size > 0:
        conn[i,j] = d1_100n[i,j, q[0]]
        conn_cum[i,j] = np.sum(d1_100n[i,j,q])
        conn_time[i,j]=q[1]

np.fill_diagonal(conn, 0)
np.fill_diagonal(conn_cum, 0)
  
edges = conn_cum
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        if(edges[i,j] > 0):
            edges[i,j] = 1
        
time_fine = datetime.datetime.now()
delta_tot = time_fine - time_start

time_post2 = datetime.datetime.now()            

with open(path+"time_all_program1.txt", "a") as file1:
    file1.write(str((delta_tot.seconds.real*CONVERSION + delta_tot.microseconds.real)/CONVERSION)+"\n")
            
with open(path+"time_load.txt", "a") as file1:
    file1.write(str((delta_time_load.seconds.real*CONVERSION + delta_time_load.microseconds.real)/CONVERSION)+"\n")
    
with open(path+"time_post.txt", "a") as file1:
    file1.write(str((delta_time_post.seconds.real*CONVERSION + delta_time_post.microseconds.real)/CONVERSION)+"\n")
            
mySave_3D(delay,"Hystogram")
mySave_2D(edges, "edges")

np.savez("HPPS_dataPrep.npy", delay = delay, delay_n = delay_n, d1 = d1, d1_100n = d1_100n )   #save also d1        
        


("fine")

    