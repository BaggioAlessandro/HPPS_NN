function saveTime(string_name, value, numb_ne, numb_camp)
path = pwd;
file_name = strcat(path,'/timeDataMatlab.txt');
f1 = fopen(file_name, 'a+');
fprintf(f1, '%s %g %g %g\n', string_name, value, numb_ne, numb_camp );
fclose(f1);
end