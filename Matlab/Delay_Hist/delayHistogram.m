function delayHistogram(f_name,numb_neurons,numb_camp)
%Lettura in input del matrice degli spikes

start_input = tic;
path = pwd;
file_name = strcat(path,'\',f_name,'.txt');
f2 = fopen (file_name, 'r');
s = fscanf(f2,'%g ',[numb_camp numb_neurons]);
fclose(f2);

t_input = toc(start_input)
start_delay = tic;
t_iteration_delay = zeros(numb_neurons, numb_neurons);
delays=zeros(numb_camp,numb_neurons,numb_neurons); %crea una matrice di 0 3000*40*40
for i=1:numb_neurons
  for j=1:numb_neurons
      i
      j
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
mean_iteration_time = mean (mean (t_iteration_delay))

my_save3D('HystoryMatlab', delays , 10, numb_neurons,'%g ');


save delays
