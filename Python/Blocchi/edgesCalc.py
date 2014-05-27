import numpy as np
import os

def edge():
    INF = 1000000
    
    N_NEURONS = 10

    N_CAMP = 1200

    N_DELAYS = 100
    
    TRESHOLD = 0.016
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/Python/Blocchi/"
    d1_100n = np.load(path + "d1_100n.npy")
    conn = np.zeros((N_NEURONS,N_NEURONS))
    conn_cum = np.zeros((N_NEURONS,N_NEURONS))
    conn_time= INF * np.ones((N_NEURONS,N_NEURONS))
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            q = np.where(d1_100n[i,j,:]>=TRESHOLD)
            q = q[0]
            if q.size > 0:
            conn[i,j] = d1_100n[i,j, q[0]]
            conn_cum[i,j] = np.sum(d1_100n[i,j,q])
            conn_time[i,j]=q[1]

    np.fill_diagonal(conn, 0)
    np.fill_diagonal(conn_cum, 0)
  
    edges = conn_cum
    
    np.savetxt(path + "edges.txt", edges, fmt = '%01d')
        
      