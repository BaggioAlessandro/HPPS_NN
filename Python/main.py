import numpy as np
import os
N_CAMP = 3000000
N_NEURONS = 9
N_DELAYS = 1000
factor = 10

#delay_hist = delayMatrics_v5("Input", 9, 3000000,1000,9)


path = os.getcwd()
path1 = "C:/Users/Luca/Documents/GitHub/HPPS_NN/Delay_temp/Not_Compress/"
delay = np.empty((9,9,1000), dtype=int)
for i in range(0, 9):
    delay[i] = np.loadtxt(path1 + "delay_line_"+str(i)+".txt", dtype=int)
delay_n = normalHist(delay,9,1000)

print(delay_n)

path1 = path1 + "/Document/GitHub/HPPS_NN/Delay_temp/"

path2 = os.getcwd()

#delay_hist = delayMatrics_v5("Input", N_NEURONS, N_CAMP,N_DELAYS,9)
compress("C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Not_Compress/delay_line_", factor, N_NEURONS, N_DELAYS, "C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Compress/delay_line_")


#edges_cal("C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Compress/delay_line_", 0.85, 0.5, N_NEURONS, N_DELAYS)
