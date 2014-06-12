def delayMatrics_v5(n_file, n_neurons,n_camp, n_delays, n_threads, output_folder_name):
    import random
    import datetime
    import numpy as np
    import os
    import threading
    from threading import Thread
    
    ##Functions
    def my_subctract_v3(my_list, item):
        q = my_list - item
        return q
        
    def hist3(my_list):
        hist = np.zeros((1,n_delays), dtype=int)
        hist[0][my_list[:]] += 1
        return hist

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
    
    #data= np.loadtxt(path + n_file, dtype=int)    
    data = np.empty((n_neurons,n_camp), dtype=int)
    for i in range(0, n_neurons):
        print(path + "/" + n_file + "/"+str(i)+"_01.txt")
        data[i] = np.loadtxt(path + "/" + n_file + "/"+str(i)+"_01.txt", dtype=int)
    
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
            
    
    for i in range(0,n_neurons):
        np.savetxt(path + "Delay_temp/" + output_folder_name +"/delay_line_"+str(i)+".txt" ,delay[i,:,:], fmt = '%01d')
    return delay;