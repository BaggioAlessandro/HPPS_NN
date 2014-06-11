import numpy as np
import os
N_CAMP = 300000
N_NEURONS = 10
factor = 10

#delay = np.empty((9,9,1000), dtype=int)
#for i in range(0, 9):
 #   delay[i] = np.loadtxt(path + "delay_line_"+str(i)+".txt", dtype=int)

path1 = os.getcwd()
path1 = path + "/Documents/GitHub/HPPS_NN/Delay_temp/"

path2 = os.getcwd()

#delay_hist = delayMatrics_v5("01.txt", N_NEURONS, N_CAMP,100,10)
compress(path1 + "Not_Compress/delay_line_", factor, N_NEURONS, N_CAMP, path1 + "Compress/delay_line_compress_")
edges_cal(path1 + "Compress/delay_line_", 0.85, 0.5, N_NEURONS)
