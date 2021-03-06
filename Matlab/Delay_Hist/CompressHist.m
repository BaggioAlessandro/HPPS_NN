function CompressHist(numb_neurons, f)
import magicFunctions;
load delaysn
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

my_save3D('d1Matlab', d1, 10, numb_neurons,'%10.13f ');
save d1
