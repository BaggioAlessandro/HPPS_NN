function NormalizeHist_v2(numb_neurons)
load delays_mod
start_normal = tic;
for i=1:numb_neurons
  for j=1:numb_neurons
    delaysn(:,i,j) = delays(:,i,j)./sum(delays(:,i,j));   %delay normalizzato sulla somma totale dei delay i,j
  end
end
t_normal = toc(start_normal)
my_save3D('prova', delays , 20 , numb_neurons, '%g ')
save delaysn