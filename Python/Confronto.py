import os
path = os.getcwd()
path = path + "/Documents/GitHub/HPPS_NN/"
file1 = open(path + "HystoryMatlab.txt","r")
file2 = open(path + "Hystogram.txt","r")
i = 0
while True:
    read1 = file1.read(1)
    read2 =file2.read(1)
    if read1 == "" and read2 == "":
        print("uguali")
        break
    if not (read1 is read2):
        print("diversi")
        break
    
    i = i+1
    print(i)
    

file1.close()
file2.close()