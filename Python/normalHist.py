import numpy as np
import os

def normalHist(delay, n_neurons, n_delays, n_camp):
    sum = np.sum(delay, 2)
    delay_n= np.zeros ((n_neurons,n_neurons,n_delays))
    print(delay[0][0][0])
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(n_camp)]
    
    return delay_n;
    

