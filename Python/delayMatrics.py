import random
import datetime
import numpy as np
import os

N_NEURONS = 10

N_CAMP = 1200

def gen_rand_data():
    for i in range(0,N_NEURONS):
        for j in range(0,N_CAMP):
            if data[i][j]!=1:
                data[i][j]=0
    

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"
data= np.loadtxt(path + "HPPS_inputData.txt", dtype=int)

delay= np.zeros ((N_NEURONS,N_NEURONS,N_CAMP), dtype=int)

delay_n= np.zeros ((N_NEURONS,N_NEURONS,N_CAMP))

factor = 10


def from_data_to_spike(i):
    qi = []
    for k in range(0,N_CAMP):
            if data[i][k]>0 :
                qi.append(k)
    return qi

def my_subctract(my_list, item):
    q = np.empty ((my_list.shape), dtype = int)
    q2 = np.empty ((my_list.shape), dtype = int)
    index = 0
    #if q2.size == 0:
    #    return q2
    for w in range(0,my_list.size):
        q[w] = my_list[w] - item
        if q[w]>=0:
            q2[index] = q[w]
            index += 1
    return q2

def my_subctract_v2(my_list, item):
    q = np.empty ((my_list.shape), dtype=int)
    index = 0
    for w in range(0,my_list.size):
        temp = my_list[w] - item
        if temp >= 0:
            q[index] = temp
            index = index + 1
    return q
    
def my_subctract_v3(my_list, item):
    q = my_list - item
    q = q[ np.where( q >= 0) ]
    return q
    
def hist1(my_list):
    hist = []
    index1 = 0
    for index2 in range(0, N_CAMP):
        if index1 > my_list(my_list.size-1):
            hist.append(0)
        else:
            if(my_list[index1] == index2):
                hist.append(1)
            else:
                hist.append(0)
            index1 += 1
    return hist

def hist2(my_list):
    hist = np.zeros((1,N_CAMP), dtype=int)
    for index in range(0, my_list.size):
        hist[0][my_list[index]] = hist[0][my_list[index]] + 1
    return hist
    
def hist3(my_list):
    hist = np.zeros((1,N_CAMP), dtype=int)
    hist[0][my_list[:]] += 1
    return hist
    
def compress():
    d1 = np.zeros ((N_NEURONS, N_NEURONS, np.floor(N_CAMP/factor)+1))
    for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
        d1[:,:,i] = np.sum(delay[:,:,i*factor:(i+1)*factor], 2)
    
    if(N_CAMP%factor != 0):
        i = i+1
        for j in range(np.int64(np.floor(N_CAMP/factor))*factor, N_CAMP):
            d1[:][:][i]= d1[:][:][i] + delay_n[:][:][j]
    
    return d1
    
def mySave (my_matrix,fileName):
    file = open(path+ fileName +".txt", "w")
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
          file.write("coppia " + str(i+1) + " " + str(j+1) + "\n")
          for k in range(0, 10):
                file.write(str(my_matrix[i][j][k]) + " ")
          file.write("\n")  
    file.close

#genero random data
gen_rand_data()
delta1 = datetime.timedelta()
temp = datetime.timedelta()
 
#inizio calcolo della matrice di delay
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        
        time21 = datetime.datetime.now()
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
                                 
        time22 = datetime.datetime.now()
        delta1 = delta1 + time22 - time21
    print(i)

media = delta1/(N_NEURONS * N_NEURONS)
print(media)
with open(path+"time_iteration.txt", "w") as file1:
    file1.write(str(media.seconds.real)+","+str(media.microseconds.real)) 
    
sum = np.sum(delay, 2)
            
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(N_CAMP)]
        

d1 = compress()
d1_100 = d1[:][:][0:100]
d1_100n = np.zeros((N_NEURONS,N_NEURONS,100))
sum2 = np.sum(d1_100, 2)
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        for p in range(0, 100):
            d1_100n[i][j][p] = d1_100[i][j][p]/sum2[i][j]
            
mySave(delay,"Hystogram")
mySave(d1, "d1Python")
mySave(d1_100n, "d1_100nPython")

np.savez("HPPS_dataPrep.npy", delay = delay, delay_n = delay_n, d1 = d1, d1_100n = d1_100n )   #save also d1        
        


("fine")

    