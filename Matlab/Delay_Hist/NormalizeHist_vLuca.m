function NormalizeHist_vLuca(numb_neurons)
load delays_mod
start_normal = tic;
for i=1:numb_neurons
  for j=1:numb_neurons
    delaysn(:,i,j) = delays(:,i,j)./(delays(1,j,j));   %delay normalizzato sulla somma totale dei delay i,j
  end
end

t_normal = toc(start_normal)

my_save3D('delaysn', delaysn, 10, numb_neurons,'%10.13f '); 
save delaysn