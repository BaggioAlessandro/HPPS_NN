function my_save2D(string_name, matrix, n_neur, typef)
path = pwd;
file_name = strcat(path,'/',string_name,'.txt');
f1 = fopen (file_name, 'w');
for i = 1:n_neur
    for j = 1:n_neur
      fprintf(f1, typef, matrix(i,j));
    end
     fprintf(f1, '\n');
end
fclose(f1);
end