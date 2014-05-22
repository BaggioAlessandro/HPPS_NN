function my_save3D(string_name, matrix , num_stamp , n_neur, typef)
path = pwd;
file_name = strcat(path,'/',string_name,'.txt');
f1 = fopen (file_name, 'w');
for i = 1:n_neur
        for j = 1:n_neur
          fprintf(f1, 'coppia %g %g \n', i,j) ;
          for k = 1:num_stamp
            fprintf(f1, typef , matrix(k,i,j));
          end
          fprintf(f1, '\n');
        end
end
fclose(f1);
end