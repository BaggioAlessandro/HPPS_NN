import random
import datetime
import numpy as np

N_NEURONS = 40

N_CAMP = 5000

data= np.random.random_integers(0,20,(N_NEURONS,N_CAMP))

delay= np.zeros ((N_NEURONS,N_NEURONS,N_CAMP))

def gen_rand_data():
    for i in range(0,N_NEURONS):
        for j in range(0,N_CAMP):
            if data[i][j]!=1:
                data[i][j]=0
    
def from_data_to_spike(i):
    qi = []
    for k in range(0,N_CAMP):
            if data[i][k]>0 :
                qi.append(k)
    return qi

def my_subctract(my_list, item):
    q = np.empty ((my_list.shape), dtype=int)
    q2 = np.empty ((my_list.shape), dtype=int)
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
        if index1 > q2.size-1:
            hist.append(0)
        else:
            if(my_list[index1] == index2):
                hist.append(1)
            else:
                hist.append(0)
            index1 += 1
    return hist
    


#genero random data
gen_rand_data()

file = open("HPPS_data.txt", "w")
file.write(np.array2string(data))
file.close()
#inizio calcolo della matrice di delay
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        #file1 = open("HPPS_time1.txt", "a")
        
        qi = np.where(data[i][:] > 0)   #tupla contenente un array
        qj = np.where(data[j][:] > 0)
        vi = qi[0]  #prendo solo il vettore
        vj = qj[0]
        
        #level 3
        delta1 = datetime.timedelta()        
        delta2 = datetime.timedelta()
        print(vi.size)
        for h in range(0,vi.size):
            time1 = datetime.datetime.now() 
            #time 1 start
            q2 = my_subctract_v3(vj, vi[h])
                        
            if q2.size>0:
                time21 = datetime.datetime.now() 
                my_hist = hist1(q2)
                time22 = datetime.datetime.now() 
                delta2 = delta2 + time22-time21
                delay[i][j] = [my_hist[p] + delay[i][j][p] for p in range(len(my_hist))]
            #timestamp finished 1
            time2 = datetime.datetime.now()
            delta1 = delta1 + time2-time1
            
        
        if(vi.size > 0):
            media = delta2/vi.size
            print(media)
            with open("HPPS_time1.txt", "w") as file1:
                file1.write('\n'+str(media.microseconds.real)) 
    print(i)
    
sum=[[]]
    
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        sum[i][j] = [delay[i][j][p] for p in range(N_CAMP)]
            
for i in range(0,N_NEURONS):
    for j in range(0,N_NEURONS):
        delay[i][j] = [delay[i][j][p]/sum[i][j] for p in range(N_CAMP)]
        
        
print("fine")

    