import os
import numpy as np

def mySave_2D (my_matrix,fileName, n_neurons):
    file = open(fileName +".txt", "w")
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            file.write(str(my_matrix[i][j]) + " ")
        
        file.write("\n")    
    file.close

def edges_cal(n_file, tresh_peak, weight_diff_fire, n_neurons, n_delays):
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"
    delay = np.empty((n_neurons,n_neurons,np.floor(n_delays/factor)+1), dtype=int)
    for i in range(0, n_neurons):
        delay[i] = np.loadtxt(n_file+str(i)+".txt", dtype=int)
    
    edges = np.zeros((n_neurons, n_neurons))
    
    d1_20 = delay[:,:,0:20]

    max_arr = np.argmax(d1_20,2)
    
    
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if (max_arr[i][j] < 5): #tresh_peak=0.85
                edges[i,j] = 1;
    
    
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            if (max_arr[i,j] == 0 ):
                edges[i,j] = 0;
    
    print(edges)
    for i in range(0,n_neurons):
        list = []
        max_list = []
        for j in range(0,n_neurons):
            count=0;
            tot = 0;
            if (edges[j,i] == 1):
                list.append(j)
                max_list.append(d1_20[max_arr[j,i],j,i])
                
        maximum = max(max_list)
        print(max_list.index(max(max_list)))
        index_max = list[max_list.index(max(max_list))]
        for h in range(0,len(list)):
            if ((d1_20[h,i,max_arr[h,i]]/2) > maximum * (d1_20[h,h,0] / d1_20[index_max,index_max,0]/weight_diff_fire)):  #weight_diff_fire = 0.5
                    edges[j,i] = 0
    print("\n")
    print(edges)
                    
    mySave_2D(edges, "C:/Users/Ale/Documents/GitHub/HPPS_NN/edges_delay_python", n_neurons)
                
            
        
    
