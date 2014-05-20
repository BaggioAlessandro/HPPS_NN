function show_graph_d=show_graph_d2( threshold, fig, firstonly )
% nodelist is a 5-digit integer [row1|row2|row3|row4|row5] that plots rowX
% if rowX is non-zero; or a list of nodes [ node1 node2 ... ] e.g. 1:64
% if not specified, all 22 active nodes [25..64] will be shown.
% can pass [] or omit other params to use default values.

numb_neurons = 10;

if (firstonly)
  if (~exist('fd1'))
    load fdelays01 fd1;
  end
  if (~exist('fd1_100n'))
    fd1_100=fd1(1:101,:,:);
    for i=1:numb_neurons
      for j=1:numb_neurons
        fd1_100n(:,i,j)=fd1_100(:,i,j)./sum(fd1_100(:,i,j));
      end
    end
  end
else
  if (~exist('d1'))
    load delays01 d1;
  end
  if (~exist('d1_100n'))
    d1_100=d1(1:101,:,:);
    for i=1:numb_neurons
      for j=1:numb_neurons
        d1_100n(:,i,j)=d1_100(:,i,j)./sum(d1_100(:,i,j));
      end
    end
  end
end

noderow{1} = [ 25 26 27 30 31 ];
noderow{2} = [ 35 36 ];
noderow{3} = [ 41 43 44 46 ];
noderow{4} = [ 49 50 51 52 54 ];
noderow{5} = [ 57 58 59 60 63 64 ];
if ( exist('nodelist') && length(nodelist) )    % exists and non-empty
  q=1;
else
    nodes = 25:64;
end

if (firstonly)
  fconn=zeros(40,40);
  fconn_cum=zeros(40,40);
  fconn_time=inf*ones(40,40);
  for i=1:40
    for j=1:40
      q=find(fd1_100n(:,i,j)>=threshold);
      if (not(isempty(q)))
        fconn(i,j)=fd1_100n(q(1),i,j);
        fconn_cum(i,j)=sum(fd1_100n(q,i,j));
        fconn_time(i,j)=q(1);
      end
    end
  end
  fconn_n=fconn-diag(diag(fconn));
  fconn_cum_n=fconn-diag(diag(fconn_cum));
else
  conn=zeros(40,40);
  conn_cum=zeros(40,40);
  conn_time=inf*ones(40,40);
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
  %toglie i casi 1-1 2-2 3-3 4-4
  conn_n=conn-diag(diag(conn)); %ok solo per matrici quadrate
  culo = diag(diag(conn_cum))
  conn_cum_n=conn_cum-diag(diag(conn_cum));
end

edges=zeros(64);
if (firstonly)
  edges(25:64,25:64)=fconn_cum_n;
else
  edges(25:64,25:64)=conn_cum_n;
end

nn=find([ max(edges,[],2)+max(edges,[],1)']>0)
ne=sum(sum(edges>0))

nnodes=nn;
edgesR=zeros(64);
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

show_graph_draw(threshold, fig, firstonly, edges, 0);
show_graph_draw(threshold, fig+10, firstonly, edgesR, 1);
return;