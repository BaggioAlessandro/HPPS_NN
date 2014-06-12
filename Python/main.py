import numpy as np
import os
N_CAMP = 300000
N_NEURONS = 10
N_DELAYS = 100
factor = 1
media = True
TRESHOLD = 0.005

#delay_hist = delayMatrics_v5("Input", 9, 3000000,1000,9)


path = os.getcwd()
path1 = "C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Not_Compress/"

path1 = path1 + "/Document/GitHub/HPPS_NN/Delay_temp/"

path2 = os.getcwd()

#delay_hist = delayMatrics_v5("Input/10_new_model", N_NEURONS, N_CAMP,N_DELAYS,N_NEURONS,"Not_Compress_10_new")
#compress("C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Not_Compress_10_new/delay_line_", factor, N_NEURONS, N_DELAYS, media , "C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Compress/delay_line_")
postIniziale("C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Not_Compress_10_old/delay_line_", factor, N_NEURONS, N_DELAYS, TRESHOLD , "C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Compress/delay_line_")

#edges_cal("C:/Users/Ale/Documents/GitHub/HPPS_NN/Delay_temp/Compress/delay_line_", factor, 0.85, 0.5, N_NEURONS, N_DELAYS)
