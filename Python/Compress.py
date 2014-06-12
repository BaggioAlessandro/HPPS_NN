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
    
def compress(n_file_input, factor, n_neurons, n_delays, do_media, n_file_output):
    delay = np.empty((n_neurons,n_neurons,n_delays), dtype=int)
    for i in range(0, n_neurons):
        delay[i] = np.loadtxt(n_file_input+str(i)+".txt", dtype=int)

    d1 = np.zeros ((n_neurons, n_neurons, np.floor(n_delays/factor)+1))
    for i in range(0, np.int64(np.floor(n_delays/factor))):   #check +1
        d1[:,:,i] = np.sum(delay[:,:,i*factor:(i+1)*factor], 2)
    
    if(n_delays%factor != 0):
        i = i+1
        d1[:,:,i]= np.sum(delay[:,:,(i)*f:], 2)
        
    if(do_media):
        for i in range(0,n_neurons):
            for j in range(0,n_neurons):
                d1[i,j,1:-1] -= np.int64(np.mean(d1[i,j,1:200]))
        
        for i in range(0,n_neurons):
            for j in range(0,n_neurons):
                for h in range (0,d1.shape[2]):
                    if (d1[i,j,h] < 0):
                        d1[i,j,h] = 0        
    for i in range(0,n_neurons):
        np.savetxt(n_file_output+str(i)+".txt" ,d1[i,:,:], fmt = '%01d')
    
                
    
    mySave_3D(d1[:,:,0:20], n_file_output + "tot", n_neurons, n_delays)