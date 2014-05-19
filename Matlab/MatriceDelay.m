numb_neurons = 40;
numb_camp = 5000;
f=10;
start_all = tic;
%Lettura in input del matrice degli spikes
start_input = tic;
path = pwd;
path = path (1:end-7);
file_name = strcat(path,'\GitHub\HPPS_NN\HPPS_inputData.txt');
f2 = fopen (file_name, 'r');
str = '';
for l = 1:numb_camp
    str =  strcat(str, '%g ');
end
s1 = fscanf(f2, str ,[numb_camp numb_neurons]);
s = s1;
fclose(f2);
t_input = toc(start_input)

start_delay = tic;
t_iteration_delay = zeros(numb_neurons, numb_neurons);
delays=zeros(numb_camp,numb_neurons,numb_neurons); %crea una matrice di 0 3000*40*40
for i=1:numb_neurons
    i
  for j=1:numb_neurons
    t1 = tic;
    qi=find(s(:,i)==1); %estrae i time degli spike di i
    qj=find(s(:,j)==1); %estrae i time degli spike di j
    for k=1:length(qi)
      q=qj-qi(k);   %differenza degli skipe di j con gli spike di i
      q2=q(find(q>=0)); %filtro q per prendere solo i maggiori
      if length(q2)>0
        h=histc(q2,0:numb_camp);
        delays(:,i,j)=delays(:,i,j)+reshape(h(1:numb_camp),numb_camp,1);
      end
    t_iteration_delay(i,j) = toc(t1);
    end
  end
end
t_delay = toc(start_delay)

start_normal = tic;
for i=1:numb_neurons
  for j=1:numb_neurons
    delaysn(:,i,j) = delays(:,i,j)./sum(delays(:,i,j));   %delay normalizzato sulla somma totale dei delay i,j
  end
end
t_normal = toc(start_normal)

start_compress = tic;
d1=zeros(floor(length(delaysn)./f)+1,numb_neurons,numb_neurons);    %� come se andasse a comprimere la matrice di partenza lungo l'asse del tempo
for i=1:floor(length(delaysn)./f)
  d1(i,:,:)=sum(delaysn(((i-1)*f)+1:i*f, :, :),1);  %1 indica che la somma � fatta lungo la prima dimensione
end
if i<length(delaysn)./f %gestisce la posizione 501
  i=i+1;
  d1(i,:)=sum(delaysn((i-1)*f+1:end,:,:),1);
end
m_d1=squeeze(max(d1,[],1)); %ritorna il valore massimo per ogni riga lungo la prima dimensione

m_delaysn=squeeze(max(delaysn,[],1));
t_compress = toc(start_compress)

start_save = tic;
%Stampa su file dell'histogram
file_name = strcat(path,'\GitHub\HPPS_NN\HystoryMatlab.txt');
f1 = fopen (file_name, 'w');
for i = 1:numb_neurons
        for j = 1:numb_neurons
          fprintf(f1, 'coppia %g %g \n', i,j) ;
          for k = 1:10
            fprintf(f1, '%g ', delays(k,i,j));
          end
          fprintf(f1, '\n');
        end
end
fclose(f1);
t_save = toc(start_save)

t_all = toc(start_all)

mean_iteration_time = mean (mean (t_iteration_delay))
%save fdelays01 fdelays fdelaysn m_fdelaysn m_fd1 fd1