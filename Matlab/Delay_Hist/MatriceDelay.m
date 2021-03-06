function main
numb_neurons = 10;
numb_camp = 300000;
f=10;
threshold = 0.4;

%Lettura in input del matrice degli spikes

%tmp_dati = csvread('C:\Users\Luca\Documents\GitHub\HPPS_NN\DatiReali\A.txt');

start_delay = tic;
start_all = tic;
start_input = tic;
path = pwd;
file_name = strcat(path,'\01.txt')
f2 = fopen (file_name, 'r');
s = fscanf(f2,'%g ',[numb_camp numb_neurons]);
fclose(f2);

t_input = toc(start_input)

%t_iteration_delay = zeros(numb_neurons, numb_neurons);
delays=zeros(numb_camp,numb_neurons,numb_neurons); %crea una matrice di 0 3000*40*40
for i=1:numb_neurons
    i
  for j=1:numb_neurons
    %t1 = tic;
    qi=find(s(:,i)==1); %estrae i time degli spike di i
    qj=find(s(:,j)==1); %estrae i time degli spike di j
    j
    for k=1:length(qi)
      q=qj-qi(k);   %differenza degli skipe di j con gli spike di i
      q2=q(find(q>=0)); %filtro q per prendere solo i maggiori
      if length(q2)>0
        h=histc(q2,0:numb_camp);
        delays(:,i,j)=delays(:,i,j)+reshape(h(1:numb_camp),numb_camp,1);
      end
    %t_iteration_delay(i,j) = toc(t1);
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
t_compress = toc(start_compress)


%mean_iteration_time = mean (mean (t_iteration_delay))
%save fdelays01 fdelays fdelaysn m_fdelaysn m_fd1 fd1

d1_100=d1(1:101,:,:);
    for i=1:numb_neurons
      for j=1:numb_neurons
        d1_100n(:,i,j)=d1_100(:,i,j)./sum(d1_100(:,i,j));
      end
    end

%Seconda parte
conn=zeros(numb_neurons,numb_neurons);
  conn_cum=zeros(numb_neurons,numb_neurons);
  conn_time=inf*ones(numb_neurons,numb_neurons);
  for i=1:numb_neurons
    for j=1:numb_neurons
      q=find(d1_100n(:,i,j)>=threshold);
      if (not(isempty(q)))
        conn(i,j)=d1_100n(q(1),i,j);
        conn_cum(i,j)=sum(d1_100n(q,i,j)); %somma dei camponamenti sopra la soglia
        conn_time(i,j)=q(1); %q(1) primo istante di tempo sopra la soglia
      end
    end
  end
  %toglie i casi 1-1 2-2 3-3 4-1
  conn_n = conn - diag(diag(conn)); %ok solo per matrici quadrate
  conn_cum_n = conn_cum - diag(diag(conn_cum));
  
edges = zeros(numb_neurons, numb_neurons);  
edges = conn_cum_n;

nn=find([ max(edges,[],2)+max(edges,[],1)']>0);
ne=sum(sum(edges>0));

nnodes=nn;
edgesR=zeros(numb_neurons);
xi=0;
x=[];
for i=nnodes'
  for j=nnodes'
    if (i~=j)
      xi=xi+1;
      x(xi,:)=[i j];
    end
  end
end

for i=1:ne
  xx=ceil(rand*xi);
  q=x(xx,:);
  edgesR(q(1),q(2))=1;
  x=x([1:xx-1 xx+1:end],:);
  xi=xi-1;
end

start_save = tic;
%Stampa su file dell'histogram
my_save3D('HystoryMatlab', delays , 10, numb_neurons,'%g ');
my_save3D('d1Matlab', d1, 10, numb_neurons,'%10.13f '); 
my_save3D('d1_100nMatlab', d1_100n, 10, numb_neurons, '%10.13f ');
my_save2D('edgesMatlab', edges, numb_neurons, '%10.5f ');

t_save = toc(start_save)
t_all = toc(start_all)
saveTime('t_all',t_all,numb_neurons,numb_camp);
saveTime('t_input',t_input,numb_neurons,numb_camp);
saveTime('t_delay',t_delay,numb_neurons,numb_camp);
saveTime('t_normal',t_normal,numb_neurons,numb_camp);
saveTime('t_compress',t_compress,numb_neurons,numb_camp);
saveTime('t_save',t_save,numb_neurons,numb_camp);
%saveTime('mean_iteration_time',mean_iteration_time,numb_neurons,numb_camp);

end

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

function saveTime(string_name, value, numb_ne, numb_camp)
path = pwd;
file_name = strcat(path,'/timeDataMatlab.txt');
f1 = fopen(file_name, 'a+');
fprintf(f1, '%s %g %g %g\n', string_name, value, numb_ne, numb_camp );
fclose(f1);
end
