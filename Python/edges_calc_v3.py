import os
import numpy as np

def edges_cal(tresh_peak, weight_diff_fire, N_NEURONS):
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"
    np.loadtxt(path + "Histogram_Python.txt")
    edges = zeros(N_NEURONS, N_NEURONS);

    max = np.max(d1_20,1);
    
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            if (d1_20[2,i,j] > max[1,i,j]*tresh_peak): #tresh_peak=0.85
                edges[i,j] = 1;
            
        
    
    
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            if (max[1,i,j] == d1_20[1,i,j] ):
                edges[i,j] = 0;
            
        
    
    
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            count=0;
            tot = 0;
            if (edges[i,j] == 1):
                for h in range(0,N_NEURONS):
                    if (h != i and edges[h,j] == 1 ):
                        if ((d1_20[2,h,j]/2) > d1_20[2,i,j] * (d1_20[1,h,h] / d1_20[1,i,i]/weight_diff_fire)):  #weight_diff_fire = 0.5
                            count = count + 1;
                        
                        tot = tot+1;
                    
                
                if (count > 0):
                    edges[i,j] = 0;
                
            
        
    
