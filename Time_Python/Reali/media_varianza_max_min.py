import csv
import os

N_NEURON = 10

def media(my_list):
    if(len(my_list)>0):
        tot = 0.0
        for i in range(len(my_list)):
            tot += my_list[i]

        return tot/len(my_list)

def varianza(my_list):
    if(len(my_list)>0):
        tot = 0.0
        mean = media(my_list)
        for i in range(len(my_list)):
            tot += pow((my_list[i] - mean), 2)
        
        return tot/len(my_list)

def max(my_list):
    max = 0.0
    for i in range(len(my_list)):
        if(max < my_list[i]):
            max = my_list[i]

    return max
    
def min(my_list):
    min = 999999999.0
    for i in range(len(my_list)):
        if(min > my_list[i]):
            min = my_list[i]
    return min
    
    

destination = "Reali\\elaborazione_iterazione.txt"

source = "Reali\\time_iteration.txt"

path = os.getcwd()
path = path + "\\Documents\\GitHub\\HPPS_NN\\Time_Python\\"

path2 = os.getcwd()
path2 = path2 + "\\Documents\\GitHub\\HPPS_NN\\Time_Python\\"

        
time = []
size = []
string = []

with open(path + source, 'rt') as file1:
    reader = csv.reader(file1, delimiter=' ', lineterminator = "\n")
    for h in reader:
        string.append(h)

    i=0    
    for i in range(len(string)):
        time.append(float(string[i][0]))
        size.append(float(string[i][3]))
        
index_max = 0
index_min = 0
mean = 0
it_per_size = []
mean_it_per_size = 0
variance_it_per_size = 0

print(len(time))
for j in range(len(time)):
    mean += time[j]
    it_per_size.append(time[j]/size[j])
    if(time[index_max] < time[j]):
        index_max = j   
    
    if(time[index_min] > time[j]):
        index_min = j

mean = mean /(N_NEURON*N_NEURON)
        
mean_it_per_size = media(it_per_size)
variance_it_per_size = varianza(it_per_size)
    
with open(path2 + destination, 'w') as file2:
    file2.write("media iterazione = " + str(mean) + "\n")
    file2.write("max iterazione = " + str(time[index_max]) + "\n")
    file2.write("min iterazione = " + str(time[index_min]) + "\n")
    file2.write("media iterazione/size 1 = " + str(mean_it_per_size) + "\n")
    file2.write("varianza iterazione/size 1 = " + str(variance_it_per_size) + "\n")
    file2.write("max iterazione/size 1 = " + str(max(it_per_size)) + "\n")
    file2.write("min iterazione/size 1 = " + str(min(it_per_size)) + "\n")


    