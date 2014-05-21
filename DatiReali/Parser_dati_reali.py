import csv
import os

CAMP = 300.0
PRECISION = 0.0001
N_NEURON = 10

destination = "01.txt"

path = os.getcwd()
path = path + "\\Documents\\GitHub\\HPPS_NN\\DatiReali\\"

path2 = os.getcwd()
path2 = path2 + "\\Documents\\GitHub\\HPPS_NN\\"

nomi = ["A.csv","B.csv","C.csv","D.csv","E.csv","F.csv","G.csv","H.csv","I.csv","L.csv"]

for i in nomi:
    time_stamp = []
    with open(path + i, 'rt') as file1:
        reader = csv.reader(file1, delimiter=',', skipinitialspace=True)
        for h in reader:
            culo=0
            
        for string in h:
            time_stamp.append(float(string))
    
    print(len(time_stamp))
    with open(path2 + destination, 'a') as file2:
        count = 0.001
        j = 0
        k = 0
        while count <= CAMP:
            if(j >= len(time_stamp)):
                break
            if(abs(time_stamp[j]-count) < PRECISION):
                k += 1
                j += 1
                file2.write("1 ")
            else:
                file2.write("0 ")
            
            count = count + 0.001
        
        while count <= CAMP:
            file2.write("0 ")
            count = count + 0.001
        file2.write("\n")
            
        if(k != len(time_stamp)):
            print("merda"+i)
    