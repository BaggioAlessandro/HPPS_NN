function media(numb_neurons, numb_camp)
load delays_real_example

for i=1:numb_neurons
  for j=1:numb_neurons
    delays(:,i,j) = floor(delays(:,i,j) - mean(delays(101:201,i,j)));   %delay normalizzato sulla somma totale dei delay i,j
  end
end

for i=1:numb_neurons
  for j=1:numb_neurons
      for h=1:numb_camp
        if delays(h,i,j) < 0
            delays(h,i,j) = 0;   %delay normalizzato sulla somma totale dei delay i,j
        end
      end
  end
end

save delays_mod



