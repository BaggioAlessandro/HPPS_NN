numb_neurons = 10;
numb_camp = 5000;
f=10;

%Lettura in input del matrice degli spikes
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

t_iteration_delay = zeros(numb_neurons, numb_neurons);
delays=zeros(numb_camp,numb_neurons,numb_neurons); %crea una matrice di 0 3000*40*40
for i=1:numb_neurons
  for j=1:numb_neurons
    qi=find(s(:,i)==1); %estrae i time degli spike di i
    qj=find(s(:,j)==1); %estrae i time degli spike di j
    for k=1:length(qi)
      q=qj-qi(k);   %differenza degli skipe di j con gli spike di i
      q2=q(find(q>=0)); %filtro q per prendere solo i maggiori
      if length(q2)>0
        h=histc(q2,0:numb_camp);
        delays(:,i,j)=delays(:,i,j)+reshape(h(1:numb_camp),numb_camp,1);
      end
    end
  end
end

for i=1:numb_neurons
  for j=1:numb_neurons
    delaysn(:,i,j) = delays(:,i,j)./sum(delays(:,i,j));   %delay normalizzato sulla somma totale dei delay i,j
  end
end

d1=zeros(floor(length(delaysn)./f)+1,numb_neurons,numb_neurons);    %è come se andasse a comprimere la matrice di partenza lungo l'asse del tempo
for i=1:floor(length(delaysn)./f)
  d1(i,:,:)=sum(delaysn(((i-1)*f)+1:i*f, :, :),1);  %1 indica che la somma è fatta lungo la prima dimensione
end
if i<length(delaysn)./f %gestisce la posizione 501
  i=i+1;
  d1(i,:)=sum(delaysn((i-1)*f+1:end,:,:),1);
end
m_d1=squeeze(max(d1,[],1)); %ritorna il valore massimo per ogni riga lungo la prima dimensione

m_delaysn=squeeze(max(delaysn,[],1));
save delays01 delays delaysn m_delaysn d1 m_d1