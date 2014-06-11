import numpy as np

#path = os.getcwd()
#path = path + "/Documents/GitHub/HPPS_NN/"
#delay = np.empty((9,9,1000), dtype=int)
#for i in range(0, 9):
 #   delay[i] = np.loadtxt(path + "delay_line_"+str(i)+".txt", dtype=int)


delay_hist = delayMatrics_v5("01_new_10.txt",9,3000000,1000,9)
#edges_cal(0.85, 0.5, N_NEURONS)
