import csv
import os

CAMP = 300.0
RESOLUTION = 0.0001
PRECISION = 0.00001
N_NEURON = 16

destination = "01_new_10.txt"

path = os.getcwd()
path = path + "\\Documents\\GitHub\\HPPS_NN\\DatiReali\\Rete_10\\Modello_Nuovo\\"

path2 = os.getcwd()
path2 = path2 + "\\Documents\\GitHub\\HPPS_NN\\Input\\10_new_model\\"

nomi = ["A.csv","B.csv","C.csv","D.csv","E.csv","F.csv","G.csv","H.csv","I.csv"]
poi=0
for i in nomi:
    time_stamp = []
    with open(path + i, 'rt') as file1:
        reader = csv.reader(file1, delimiter=',', skipinitialspace=True)
        for h in reader:
            culo=0
            
        for string in h:
            time_stamp.append(float(string))
    
    print(len(time_stamp))
    i = i[0]
    with open(path2 + str(poi) + "_01.txt", 'w') as file2:
        count = RESOLUTION
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
            
            count = count + RESOLUTION
        
        while count <= CAMP:
            file2.write("0 ")
            count = count + RESOLUTION
        file2.write("\n")
            
        if(k != len(time_stamp)):
            print("merda"+i+str(k))
    print(poi)
    poi += 1