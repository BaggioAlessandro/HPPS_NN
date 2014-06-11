import os
import numpy as np

def edges_cal(tresh_peak, weight_diff_fire, N_NEURONS):
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"
    delay = np.empty((N_NEURONS,N_NEURONS,N_DELAYS), dtype=int)
    for i in range(0, N_NEURONS):
        delay[i] = np.loadtxt(path + "delay_line_"+str(i)+".txt", dtype=int)
    
    edges = np.zeros((N_NEURONS, N_NEURONS));
    
    d1_20 = delay[:,0:20,0:20]

    max = np.max(d1_20,1);
    
    
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            if (d1_20[1,i,j] > max[i,j]*tresh_peak): #tresh_peak=0.85
                edges[i,j] = 1;
            
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            if (max[i,j] == d1_20[0,i,j] ):
                edges[i,j] = 0;
            
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            count=0;
            tot = 0;
            if (edges[i,j] == 1):
                for h in range(0,N_NEURONS):
                    if (h != i and edges[h,j] == 1 ):
                        if ((d1_20[1,h,j]/2) > d1_20[1,i,j] * (d1_20[0,h,h] / d1_20[0,i,i]/weight_diff_fire)):  #weight_diff_fire = 0.5
                            count = count + 1;
                        
                        tot = tot+1;
                    
                
                if (count > 0):
                    edges[i,j] = 0;
                
            
        
    
