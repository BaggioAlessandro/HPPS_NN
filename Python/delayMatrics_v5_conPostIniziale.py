import numpy as np
import os
def mySave_3D (my_matrix,fileName, n_neurons, n_delays):
        file = open(fileName +".txt", "w")
        for i in range(0,n_neurons):
            for j in range(0,n_neurons):
                file.write("coppia " + str(i+1) + " " + str(j+1) + "\n")
                for k in range(0, my_matrix.shape[2]):
                    file.write(str(my_matrix[i][j][k]) + " ")
                file.write("\n")  
        file.close
        
def mySave_2D (my_matrix,fileName, n_neurons):
    file = open(fileName +".txt", "w")
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            file.write(str(my_matrix[i][j]) + " ")
        
        file.write("\n")    
    file.close

def compress(n_neurons,n_camp,factor):
    d1 = np.zeros ((n_neurons, n_neurons, np.floor(n_camp/factor)+1))
    for i in range(0, np.int64(np.floor(n_camp/factor))):   #check +1
        d1[:,:,i] = np.sum(delay_n[:,:,i*factor:(i+1)*factor], 2)
    
    if(n_camp%factor != 0): 
        i = i+1
        d1[:,:,i]= np.sum(delay_n[:,:,(i)*factor:], 2)
    return d1

def postIniziale(n_file_input, factor, n_neurons, n_camp, treshold, n_file_output):
    INF = 10000000
    delay = np.empty((n_neurons,n_neurons,n_camp), dtype=int)
    delay_n= np.empty((n_neurons,n_neurons,n_camp))

    for i in range(0, n_neurons):
        delay[i] = np.loadtxt(n_file_input+str(i)+".txt", dtype=int)

    sum = np.sum(delay, 2)
    
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            delay_n[i,j] = delay[i,j]/sum[i,j]            
    
    d1 = compress(n_neurons, n_camp, factor)
    d1_100 = d1[:,:,0:100]
    d1_100n = np.zeros((n_neurons,n_neurons,100))
    sum2 = np.sum(d1_100, 2)
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            d1_100n[i,j] = d1_100[i,j]/np.sum(d1_100[i,j,:])
    
    conn = np.zeros((n_neurons,n_neurons))
    conn_cum = np.zeros((n_neurons,n_neurons))
    conn_time= INF * np.ones((n_neurons,n_neurons))
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            q = np.where(d1_100n[i,j,:]>=TRESHOLD)
            q = q[0]
            if q.size > 0:
                conn[i,j] = d1_100n[i,j, q[0]]
                conn_cum[i,j] = np.sum(d1_100n[i,j,q])
                conn_time[i,j]=q[1]
    
    np.fill_diagonal(conn, 0)
    np.fill_diagonal(conn_cum, 0)
    
    edges = conn_cum
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if(edges[i,j] > 0):
                edges[i,j] = 1
        
    print(edges)
    mySave_2D(edges, "C:/Users/Ale/Documents/GitHub/HPPS_NN/edges_delay_python", n_neurons)
