import numpy as np
import os

def compress(n_file_input, factor, n_neurons, N_CAMP, n_file_output):
    delay = np.empty((n_neurons,n_neurons,N_CAMP), dtype=int)
    for i in range(0, n_neurons):
        delay[i] = np.loadtxt(n_file_input+str(i)+".txt", dtype=int)

    d1 = np.zeros ((n_neurons, n_neurons, np.floor(N_CAMP/factor)+1))
    for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
        d1[:,:,i] = np.sum(delay[:,:,i*factor:(i+1)*factor], 2)
    
    if(N_CAMP%factor != 0):
        i = i+1
        d1[:,:,i]= np.sum(delay[:,:,(i)*f:], 2)
        
    for i in range(0,n_neurons):
        np.savetxt(n_file_output+str(i)+".txt" ,delay[i,:,:], fmt = '%01d')
    