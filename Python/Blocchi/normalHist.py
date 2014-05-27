import numpy as np
import os

def normalHist():
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/Python/Blocchi/"
    
    delay= np.load(path + "delay.npy", dtype=int)
    
    delay_n= np.zeros ((N_NEURONS,N_NEURONS,N_DELAYS))
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(N_CAMP)]
            
    np.save(path + "delays_n.npy", delays_n)

        