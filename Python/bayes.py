def bayesian(n_file, n_neurons, n_camp):
    import os
    import numpy as np
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"
    
    data = np.empty((n_neurons,n_camp), dtype=int)
    
    for i in range(0, n_neurons):
        print(path + "/" + n_file + "/"+str(i)+"_01.txt")
        data[i] = np.loadtxt(path + "/" + n_file + "/"+str(i)+"_01.txt", dtype=int)
    
    prob1 = np.empty((n_neurons,n_neurons), dtype = float) # A dato B
    
    prob2 = np.empty((n_neurons,n_neurons,n_neurons), dtype = float) # Prob(A|B,C)
    
    prob3= np.empty((n_neurons,n_neurons,n_neurons,n_neurons), dtype = float)
    
    prob4 = np.empty((n_neurons,n_neurons,n_neurons,n_neurons,n_neurons), dtype = float)

    prob5 = np.empty((n_neurons,n_neurons,n_neurons,n_neurons,n_neurons,n_neurons), dtype = float)
    
    for  i in range(3, n_neurons):
        print(i)
        qi = np.where(data[i][:] > 0)
        vi = qi[0]
        for j in range (3, n_neurons):
            fireGiusti = 0
            qj = np.where(data[j][:] > 0)
            vj = qj[0]
            for h in range (0,vj.size):
                print(h)
                for k in range (0, vi.size):
                    if(vj[h]- vi[k] < 0 and vj[h]- vi[k] > -230):
                        fireGiusti = fireGiusti + 1
                    if(vj[h]- vi[k] < -230):
                        break
                
            prob1[i][j] = fireGiusti/vj.size
    
    print(prob1)