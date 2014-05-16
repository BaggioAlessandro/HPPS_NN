import numpy as np

N_NEURONS = 5

N_CAMP = 50

INF = 100000
# caricamento di d1_100n

def find_graph(threshold, firstOnly):
    if(firstOnly):
        first_spike(threshold)
    else:
        all_data(threshold)

def all_data(threshold):
    conn = np.zeros ((N_NEURONS, N_NEURONS))
    conn_cum = np.zeros ((N_NEURONS, N_NEURONS))
    conn_time = np.zeros ((N_NEURONS, N_NEURONS))
    for i in range(0, N_NEURONS):
        for j in range(0, N_NEURONS):
            q = np.where(d1_100n[i][j][:] >= threshold)
            v = q[0]
            if(v.size > 0):
                conn[i][j] = d1_100n[i][j][v[0]]
                conn_cum[i][j] = np.sum( d1_100n[i][j][v])
                conn_time[i][j] = v[0]
            else:
                conn_time[i][j] = INF
    
    np.fill_diagonal(conn, 0)
    np.fill_diagonal(conn_cum, 0)
    
def first_spike(threshold):
    a=0        
   
   
#main    
d1_100n = np.random.random((N_NEURONS,N_NEURONS,100))
find_graph(0.8, False)