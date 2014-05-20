import numpy as np
import os

path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"
data= np.random.random_integers(0,1,(10,1200))
np.savetxt(path + "HPPS_inputData.txt", data, fmt = '%01d')