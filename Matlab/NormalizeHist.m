function NormalizeHist(numb_neurons)
load delays_real_example
start_normal = tic;
for i=1:numb_neurons
  for j=1:numb_neurons
    delaysn(:,i,j) = delays(:,i,j)./sum(delays(:,i,j));   %delay normalizzato sulla somma totale dei delay i,j
  end
end
t_normal = toc(start_normal)

save delaysn