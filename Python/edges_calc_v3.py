import os
import numpy as np

def mySave_2D (my_matrix,fileName, n_neurons):
    file = open(fileName +".txt", "w")
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            file.write(str(my_matrix[i][j]) + " ")
        
        file.write("\n")    
    file.close

def edges_cal(n_file, factor, tresh_peak, weight_diff_fire, n_neurons, n_delays):
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"
    delay = np.empty((n_neurons,n_neurons, np.floor(n_delays/factor)+1), dtype=int)
    for i in range(0, n_neurons):
        delay[i] = np.loadtxt(n_file+str(i)+".txt", dtype=int)
    
    edges = np.zeros((n_neurons, n_neurons));
    
    d1_20 = delay[:,:,0:20]

    max = np.argmax(d1_20,2);
    
    
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if (max[i][j] < 10): #tresh_peak=0.85
                edges[i,j] = 1;
            
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if (max[i,j] == 0):
                edges[i,j] = 0;
            
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            count=0;
            tot = 0;
            if (edges[i,j] == 1):
                for h in range(0,n_neurons):
                    if (h != i and edges[h,j] == 1 ):
                        if ((d1_20[h,j,max[h,j]]/2) > d1_20[i,j,max[i,j]] * np.sqrt(d1_20[h,h,0] / d1_20[i,i,0])):  #weight_diff_fire = 0.5
                            count = count + 1;
                        
                        tot = tot+1;
                    
                if (count > 0):
                    edges[i,j] = 0;
    print(edges)
    mySave_2D(edges, "C:/Users/Ale/Documents/GitHub/HPPS_NN/edges_delay_python", n_neurons)
                
            
        
    
