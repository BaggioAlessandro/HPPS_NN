data= np.random.random_integers(0,1,(40,5000))
np.savetxt(path + "HPPS_inputData.txt", data, fmt = '%01d')