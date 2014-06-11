def delayMatrics_v5(n_file, n_neurons,n_camp, n_delays, n_threads):
    import random
    import datetime
    import numpy as np
    import os
    import threading
    from threading import Thread
    
   # n_neurons = 10
    
    #n_camp = 300000

    #n_delays = 100
    
   # factor = 10
    
   # TRESHOLD = 0.016
    
    ##Functions
    def my_subctract_v3(my_list, item):
        q = my_list - item
        return q
        
    def hist3(my_list):
        hist = np.zeros((1,n_delays), dtype=int)
        hist[0][my_list[:]] += 1
        return hist
        
    def compress():
        d1 = np.zeros ((n_neurons, n_neurons, np.floor(n_camp/factor)+1))
        for i in range(0, np.int64(np.floor(n_camp/factor))):   #check +1
            d1[:,:,i] = np.sum(delay_n[:,:,i*factor:(i+1)*factor], 2)
        
        if(n_camp%factor != 0): 
            i = i+1
            d1[:,:,i]= np.sum(delay_n[:,:,(i)*f:], 2)
        
        return d1
        
    def mySave_3D (my_matrix,fileName):
        file = open(path+ fileName +".txt", "w")
        for i in range(0,n_neurons):
            for j in range(0,n_neurons):
                #file.write("coppia " + str(i+1) + " " + str(j+1) + "\n")
                for k in range(0, n_delays):
                    file.write(str(my_matrix[i][j][k]) + " ")
                file.write("\n")  
        file.close
        
    
    def mySave_2D (my_matrix,fileName):
        file = open(path+ fileName +".txt", "w")
        for i in range(0,n_neurons):
            for j in range(0,n_neurons):
                file.write(str(my_matrix[i][j]) + " ")
            
            file.write("\n")    
        file.close
        
    def inner_cicle(index1,index2,index1Final,index2Final):
        for i in range (index1, index1Final):
            qi = np.where(data[i][:] > 0)
            vi = qi[0]
            for j in range (index2, index2Final):
                qj = np.where(data[j][:] > 0)
                #prendo solo il vettore
                vj = qj[0]
                for h in range(0,vi.size):
                    q2 = my_subctract_v3(vj[ ((vj >= vi[h]) & (vj<vi[h]+n_delays)) ], vi[h])
                        
                    if q2.size>0:
                        
                        my_hist = hist3(q2)
                            
                        delay[i][j][:] += my_hist[0][:]
    
    ##
    
    ##Performance Evaluation and Input handling
    delta_tot = datetime.timedelta()
    delta_time_load = datetime.timedelta()
    delta_time_post = datetime.timedelta()
    time_start = datetime.datetime.now()
    
    path = os.getcwd()
    path = path + "/Documents/GitHub/HPPS_NN/"    
    time_load1 = datetime.datetime.now()    
    print(path)    
    data= np.loadtxt(path + n_file, dtype=int)    
    time_load2 = datetime.datetime.now()
    delta_time_load = time_load2-time_load1    
    delay= np.zeros ((n_neurons,n_neurons,n_delays), dtype=int)
    delay_n= np.zeros ((n_neurons,n_neurons,n_delays))
    ##
    
    ##Body
    thread_list = []
    #inizio calcolo della matrice di delay
    
    if (n_threads > 1):
        num_compare_thread = int((n_neurons)/n_threads)
        print(num_compare_thread)
        for n in range(num_compare_thread,n_neurons,num_compare_thread):
            if ((n + num_compare_thread) < n_neurons):
                thread_list.append (Thread(target = inner_cicle, args = (n-num_compare_thread,0,n,n_neurons)))
            else:
                thread_list.append (Thread(target = inner_cicle, args = (n-num_compare_thread,0,n_neurons,n_neurons)))
            thread_list[-1].start()
    else:
        thread_list.append (Thread(target = inner_cicle, args = (0,0,n_neurons,n_neurons)))
        thread_list[-1].start()
      
    
    for i in range(len(thread_list)):
        thread_list[i].join()
    
    sum = np.sum(delay, 2)
    
    #print(time_post - time_start)            
    for i in range(0,n_neurons):
        for j in range(0,n_neurons):
            delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(n_delays)]
            
    mySave_3D(delay,'Hystogram')
    return delay;