import numpy as np
import os

def normalHist(delay, n_neurons, n_delays):
    sum = np.sum(delay, 2)
    delay_n= np.zeros ((n_neurons,n_neurons,n_delays))
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if sum[i][j] != 0:
                delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(n_delays)]
            else:
                delay_n[i][j] = [0 for p in range(n_delays)]
    return delay_n
    

