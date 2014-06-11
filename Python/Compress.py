import numpy as np
import os

def compress(n_file_input, factor, N_NEURONS, N_CAMP, n_file_output):
    delay = np.empty((N_NEURONS,N_NEURONS,N_DELAYS), dtype=int)
    for i in range(0, N_NEURONS):
        delay[i] = np.loadtxt(n_file_input+str(i)+".txt", dtype=int)

    d1 = np.zeros ((N_NEURONS, N_NEURONS, np.floor(N_CAMP/factor)+1))
    for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
        d1[:,:,i] = np.sum(delay[:,:,i*factor:(i+1)*factor], 2)
    
    if(N_CAMP%factor != 0):
        i = i+1
        d1[:,:,i]= np.sum(delay[:,:,(i)*f:], 2)
        
    for i in range(0,N_NEURONS):
        np.savetxt(n_file_output+str(i)+".txt" ,delay[i,:,:], fmt = '%01d')
    