def delayMatrics_v4(n_threads):
    import random
    import datetime
    import numpy as np
    import os
    import threading
    from threading import Thread
    
    N_NEURONS = 10
    
    N_CAMP = 300000

    N_DELAYS = 100
    
    CONVERSION = 1000000
    
    factor = 10
    
    INF = 1000000
    
    TRESHOLD = 0.016
    
    ##Functions
    def my_subctract_v3(my_list, item):
        q = my_list - item
        return q
        
    def hist3(my_list):
        hist = np.zeros((1,N_DELAYS), dtype=int)
        hist[0][my_list[:]] += 1
        return hist
        
    def compress():
        d1 = np.zeros ((N_NEURONS, N_NEURONS, np.floor(N_CAMP/factor)+1))
        for i in range(0, np.int64(np.floor(N_CAMP/factor))):   #check +1
            d1[:,:,i] = np.sum(delay_n[:,:,i*factor:(i+1)*factor], 2)
        
        if(N_CAMP%factor != 0): 
            i = i+1
            d1[:,:,i]= np.sum(delay_n[:,:,(i)*f:], 2)
        
        return d1
        
    def mySave_3D (my_matrix,fileName):
        file = open(path+ fileName +".txt", "w")
        for i in range(0,N_NEURONS):
            for j in range(0,N_NEURONS):
                file.write("coppia " + str(i+1) + " " + str(j+1) + "\n")
                for k in range(0, 10):
                    file.write(str(my_matrix[i][j][k]) + " ")
                file.write("\n")  
        file.close
        
    
    def mySave_2D (my_matrix,fileName):
        file = open(path+ fileName +".txt", "w")
        for i in range(0,N_NEURONS):
            for j in range(0,N_NEURONS):
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
                    q2 = my_subctract_v3(vj[ ((vj >= vi[h]) & (vj<vi[h]+N_DELAYS)) ], vi[h])
                        
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
    data= np.loadtxt(path + "01.txt", dtype=int)    
    time_load2 = datetime.datetime.now()
    delta_time_load = time_load2-time_load1    
    delay= np.zeros ((N_NEURONS,N_NEURONS,N_DELAYS), dtype=int)
    delay_n= np.zeros ((N_NEURONS,N_NEURONS,N_DELAYS))
    ##
    
    ##Body
    thread_list = []
    #inizio calcolo della matrice di delay
    
    if (n_threads > 1):
        num_compare_thread = int((N_NEURONS)/n_threads)
        print(num_compare_thread)
        for n in range(num_compare_thread,N_NEURONS,num_compare_thread):
            if ((n + num_compare_thread) < N_NEURONS):
                thread_list.append (Thread(target = inner_cicle, args = (n-num_compare_thread,0,n,N_NEURONS)))
            else:
                thread_list.append (Thread(target = inner_cicle, args = (n-num_compare_thread,0,N_NEURONS,N_NEURONS)))
            thread_list[-1].start()
    else:
        thread_list.append (Thread(target = inner_cicle, args = (0,0,N_NEURONS,N_NEURONS)))
        thread_list[-1].start()

     #   for j in range(0,N_NEURONS):
     #       thread_list.append (Thread(target = inner_cicle, args = (i,j,qi[0])) )
     #       thread_list[-1].start()
            
    
    for i in range(len(thread_list)):
        thread_list[i].join()
    
    sum = np.sum(delay, 2)
    
    print(time_post - time_start)            
    for i in range(0,N_NEURONS):
        for j in range(0,N_NEURONS):
            delay_n[i][j] = [delay[i][j][p]/sum[i][j] for p in range(N_DELAYS)]
            
    mySave_3D(delay,'Hystogram')