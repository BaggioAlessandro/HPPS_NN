function edgesCalc_v3(threshold,numb_neurons)
import magicFunctions
load d1
load delays_mod

startEdges = tic;
d1_100=d1(1:101,:,:);
    for i=1:numb_neurons
      for j=1:numb_neurons
        d1_100n(:,i,j)=d1_100(:,i,j)./sum(d1_100(:,i,j));
      end
    end
    
d1_20 = zeros(20,numb_neurons, numb_neurons);
d1_20 = delays(1:20,:,:);

edges = zeros(numb_neurons, numb_neurons);

index_max = max(d1_20,[],1);

for i=1:numb_neurons
    for j=1:numb_neurons
        if index_max(1,i,j) == d1_20(2,i,j) || d1_20(2,i,j) > index_max(1,i,j)*0.85
            edges(i,j) = 1;
        end
    end
end

for i=1:numb_neurons
    for j=1:numb_neurons
        if index_max(1,i,j) == d1_20(1,i,j) 
            edges(i,j) = 0;
        end
    end
end

for i=1:numb_neurons
    for j=1:numb_neurons
        count=0;
        tot = 0;
        if edges(i,j) == 1
            for h = 1:numb_neurons
                if h ~= i && edges(h,j) == 1 
                    if (d1_20(2,h,j)/2) > d1_20(2,i,j) * (d1_20(1,h,h) / d1_20(1,i,i))
                        count = count + 1;
                    end
                    tot = tot+1;
                end
            end
            if count > 0
                edges(i,j) = 0;
            end
        end
    end
end



save edges

t_edges = toc(startEdges)
my_save3D('d1_100nMatlab', d1_100n, 100, numb_neurons, '%10.13f ');
my_save2D('edgesMatlab', edges, numb_neurons, '%10.5f ');
