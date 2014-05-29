function edgesCalc_vLuca(threshold,numb_neurons)
import magicFunctions
load d1

startEdges = tic;
d1_100=d1(1:101,:,:);
    for i=1:numb_neurons
      for j=1:numb_neurons
        d1_100n(:,i,j)=d1_100(:,i,j);
      end
      end
for i=1:numb_neurons
  for j=1:numb_neurons
      for h=1:50
        if d1_100n(h,i,j) < 0
            d1_100n(h,i,j) = 0;   %delay normalizzato sulla somma totale dei delay i,j
        end
      end
  end
end
d1_m = d1_100n(2:22,:,:);

my_save3D('prova', d1_m , 20 , 10, '%10.13f ')

f=3;

d1_m2=zeros(floor(length(d1_m)./f)+1,numb_neurons,numb_neurons);    %è come se andasse a comprimere la matrice di partenza lungo l'asse del tempo
for i=1:floor(length(d1_m)./f)
  d1_m2(i,:,:)=sum(d1_m(((i-1)*f)+1:i*f, :, :),1);  %1 indica che la somma è fatta lungo la prima dimensione
end
if i<length(d1_m)./f %gestisce la posizione 501
  i=i+1;
  d1_m2(i,:,:)=sum(d1_m((i-1)*f+1:end,:,:),1);
end

my_save3D('prova2', d1_m2 , 6 , 10, '%10.13f ')


%Seconda parte
conn=zeros(numb_neurons,numb_neurons);
  conn_cum=zeros(numb_neurons,numb_neurons);
  conn_time=inf*ones(numb_neurons,numb_neurons);
  for i=1:numb_neurons
    for j=1:numb_neurons
      q=find(d1_m2(:,i,j)>=threshold);
      if (not(isempty(q)))
        conn(i,j)=d1_m2(q(1),i,j);
        conn_cum(i,j)=sum(d1_m2(q,i,j)); %somma dei camponamenti sopra la soglia
        conn_time(i,j)=q(1); %q(1) primo istante di tempo sopra la soglia
      end
    end
  end
  %toglie i casi 1-1 2-2 3-3 4-4
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

save edges

t_edges = toc(startEdges)
my_save3D('d1_100nMatlab', d1_100n, 100, numb_neurons, '%10.13f ');
my_save2D('edgesMatlab', edges, numb_neurons, '%10.5f ');
