import numpy as np
import os


def compress():
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/Python/Blocchi/"
    delay_n = np.load(path + "delay_n.npy")
    
    d1 = np.zeros ((N_NEURONS, N_NEURONS, np.floor(N_CAMP/factor)+1))
    for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
        d1[:,:,i] = np.sum(delay_n[:,:,i*factor:(i+1)*factor], 2)
    
    if(N_CAMP%factor != 0): 
        i = i+1
        d1[:,:,i]= np.sum(delay_n[:,:,(i)*f:], 2)
    
    return d1

def d1():
    factor = 10
    
    N_NEURONS = 10

    N_CAMP = 1200

    N_DELAYS = 100

    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/Python/Blocchi/"
    d1 = compress()
    d1_100 = d1[:,:,0:100]
    d1_100n = np.zeros((N_NEURONS,N_NEURONS,100))
    sum2 = np.sum(d1_100, 2)
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            d1_100n[i,j,:] = d1_100[i,j,:]/np.sum(d1_100[i,j,:])
    
    np.save(path + "d1_100n.npy", d1_100n)
