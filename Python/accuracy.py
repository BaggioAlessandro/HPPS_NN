import os
import numpy as np
path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"

edges = np.loadtxt(path + "DatiReali/Rete_20/edges_Real.txt", dtype=int)
#edges = np.loadtxt(path + "DatiReali/Rete_10/Modello_Nuovo/edges_Real.txt", dtype=int)

rif = np.loadtxt(path + "edges_delay_python.txt", dtype=int)

TP = 0
TN = 0
FP = 0
FN = 0

error_list = []

for i in range(0,edges.shape[0]):
    for j in range(0, edges.shape[1]):
        single_error = []
        if(edges[i,j] == rif[i,j] and edges[i,j]==1):
            TP +=1
        
        if(edges[i,j] == rif[i,j] and edges[i,j]==0):
            TN +=1
            
        if(edges[i,j] != rif[i,j] and edges[i,j]==0):
            FP +=1
            single_error.append(i+1)
            single_error.append(j+1)
            single_error.append('FP')
            
            error_list.append(single_error)
        
        if(edges[i,j] != rif[i,j] and edges[i,j]==1):
            FN +=1   
            single_error.append(i+1)
            single_error.append(j+1)
            single_error.append('FN')
             
            error_list.append(single_error)
            
print('TP = ' + str(TP) + ' | ' + 'FN = ' + str(FN))
print('________|________\n')            
print('FP = ' + str(FP) + ' | ' + 'TN = ' + str(TN))
print(error_list)