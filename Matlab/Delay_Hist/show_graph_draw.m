function show_graph_draw=show_graph_draw()
% nodelist is a 5-digit integer [row1|row2|row3|row4|row5] that plots rowX
% if rowX is non-zero; or a list of nodes [ node1 node2 ... ] e.g. 1:64
% if not specified, all 22 active nodes [25..64] will be shown.
% can pass [] or omit other params to use default values.

load edges
rr = 0;
firstonly = true;
threshold = 1;

if (~exist('fig') || isempty(fig) )
    fig = 580;
end
figure(fig); clf; set(fig,'DoubleBuffer','on') %Flash-free rendering

nodes = 1:numb_neurons;

channel_pairs = nchoosek( nodes, 2 );
channel_pairs = sortrows( channel_pairs );

rand( 'state', 0 );
warning off MATLAB:divideByZero;
LTable = 1./eye(numb_neurons) - 1;            % put zeros on diagonal and inf elsewhere
i = 0;
excised_nodes = [];
for node = nodes
    i = i + 1;
    if ( isempty( find( [ edges(node,:) edges(:,node)' ] ) ) )  % doesn't connect to anything, nothing connects to it
        nodes = [ nodes(1:i-1) nodes(i+1:end) ];    % excise node out of nodes
        i = i - 1;
        excised_nodes(end+1) = node;
        continue;                                   % don't plot
    end
    y = 8 - floor((node-1)/8) + .5*(rand-.5);
    x = mod(node-1,8) + 1 + .5*(rand-.5);
    node_coordinates(node,:) = [x y];
    plot( x, y, 'ko', 'linewidth', 2, 'markersize', 20 ); hold on;
    tx = text( x, y, sprintf('%d', node) );
    set( tx, 'fontsize', 10, 'fontweight', 'bold', 'horizontalalignment', 'center' );
    LTable(node,:) = ShortestPath( node, 1, LTable(node,:), edges );
end

running_length=0; running_neighbors=0; running_cluster=0;
i = 0;
for node = nodes
    i = i + 1;
    neighbors = find( LTable(node,:) < inf );   % includes acquaintances (non-immediate neighbors)
    neighbors = neighbors( find( LTable(node,neighbors) > 0 ) );    % exclude the node itself (with length 0)
    num_neighbors = length( neighbors );
    total_length = sum( LTable(node,neighbors) );
    avg_length = total_length / num_neighbors;
    running_length = running_length + total_length;
    running_neighbors = running_neighbors + num_neighbors;
    disp_string = strcat( 'Node %2d / [%2d] neighbors:', repmat( ' %2d', 1, num_neighbors ) );
    disp( sprintf( disp_string, node, num_neighbors, neighbors ) );
    
    degree(i) = length( find( edges(node,:) ) );        
    disp_string = strcat( '        / path length   :', repmat( ' %2d', 1, num_neighbors ), '   <%.2f> / degree %d' );
    disp( sprintf( disp_string, LTable(node,neighbors), avg_length, degree(i) ) );

    neighbors = find( edges(node,:) );          % only adjacent neighbors
    num_neighbors = length( neighbors );
    if ( num_neighbors > 1 )
        pairs = nchoosek( neighbors, 2 );
        denom = num_neighbors * (num_neighbors-1);
    else
        pairs = [];
        denom = 1;
    end
    
    total_edges = 0;
    for pair = 1:size(pairs,1)
        ChA = pairs( pair, 1 );
        ChB = pairs( pair, 2 );
        if ( edges( ChA, ChB ) )
            total_edges = total_edges + 1;
        end
        if ( edges( ChB, ChA ) )
            total_edges = total_edges + 1;
        end        
    end
    running_cluster = running_cluster + total_edges/denom;

    disp( sprintf( '        / C(%d) = %d / %d = %.2f', node, total_edges, denom, total_edges/denom ) );
end

if (length(nodes))
  
disp( sprintf( '\nTotal # nodes = %d', length(nodes) ) );
disp_string = strcat( 'Excised nodes = ', repmat( ' %2d', 1, length(excised_nodes) ) );     % no neighbors AND not any node's neighbor
disp( sprintf( disp_string, excised_nodes ) );
L = running_length / running_neighbors;
disp( sprintf( '<length>, L   = %d / %d  = %.3f', running_length, running_neighbors, L ) );
C = running_cluster / length(nodes);
disp( sprintf( '<C(i)>, C     = %.2f / %d = %.3f       1/N = %.3f      #times larger than 1/N = %.2f', running_cluster, length(nodes), C, ...
    1/length(nodes), C*length(nodes) ) );

axis off;
tt = title( sprintf( 'Edge Connectivity Graph:   threshold=%.2f, firstonly=%d', threshold, firstonly ) ); 
set (tt, 'fontsize', 12, 'fontweight', 'bold' );
AX = axis;
tx = text( 0.1*AX(1)+0.9*AX(2), 0.4*AX(3)+0.6*AX(4), ...
           sprintf( 'L = %.3f\nC = %.3f\nTot # nodes = %d', L, C, length(nodes) ) );
set (tx, 'fontsize', 12, 'fontweight', 'bold' );
drawnow;

colormap('default');
default_colormap = colormap;
r = 0.1;
[ChA,ChB,val] = find( edges );
max_val = max(val);
min_val = min(val);
for edgenum = 1:length(ChA)
    u = node_coordinates( ChA(edgenum), : );
    v = node_coordinates( ChB(edgenum), : );
    w = v - u;
    w = w / sqrt( w(1)^2 + w(2)^2 );
    u = u + r*w;
    v = v - r*w;
    color = round( (val(edgenum)-min_val)/(max_val-min_val) * 63 + ...
		   0.5);
    color=63;
    h = arrowline( [u(1) v(1)], [u(2) v(2)], 'color', default_colormap(color,:), 'arrowsize', 200 );
%    disp( sprintf( '%2d->%2d : %.2f', ChA(edgenum), ChB(edgenum), val(edgenum) ) );    
    drawnow;
end

print('-depsc', sprintf('-f%d',fig),sprintf('graphD%dF%.2frR%dN.eps', firstonly, threshold, rr))

figure(fig+1);clf;
hist( degree );
xlabel( 'Degree, k', 'fontsize', 12, 'fontweight', 'bold' );
ylabel( 'Number of occurences', 'fontsize', 12, 'fontweight', 'bold' );
tt = title( sprintf( 'Histogram of Degree Distribution   / firstonly = %d, threshold= %.2f', firstonly, threshold ) );
set (tt, 'fontsize', 12, 'fontweight', 'bold' );
AX = axis;
tx = text( 0.8*AX(1)+0.2*AX(2), 0.2*AX(3)+0.8*AX(4), ...
           sprintf( 'Tot # nodes = %d', length(nodes) ) );
set (tx, 'fontsize', 12, 'fontweight', 'bold' );       
print('-depsc', sprintf('-f%d',fig+1),sprintf('graphD%dF%.2fR%dD.eps', firstonly, threshold,rr))

x=1:max(degree);
degree_hist=hist(degree, x);
r=regress(degree_hist', [x' ones(length(x),1)]);

x_log=log10(x);
degree_hist_log=log10(degree_hist);
degree_hist_log(find(degree_hist_log==-inf))=0;
r_log=regress(degree_hist_log', [x_log' ones(length(x_log),1)]);


figure(fig+2);clf;
plot(x, degree_hist);
hold on;
plot(x, r(1).*x+r(2), 'r');
AX = axis;
text( 0.8*AX(1)+0.2*AX(2), 0.8*AX(3)+0.2*AX(4), sprintf( 'k= %.2f', r_log(2) ) );
plot(10.^x_log, 10.^(r_log(1).*x_log+r_log(2)), 'g');
tt = title( sprintf( 'Histogram of Degree Distribution lin  / firstonly = %d, threshold= %.2f', firstonly, threshold ) );
print('-depsc', sprintf('-f%d',fig+2),sprintf('graphD%dF%.2fR%dDlin.eps', firstonly, threshold, rr))

figure(fig+3);clf;
plot(x_log, degree_hist_log);
hold on;
plot(x_log, r_log(1).*x_log+r_log(2), 'r');
AX = axis;
text( 0.8*AX(1)+0.2*AX(2), 0.8*AX(3)+0.2*AX(4), sprintf( 'k= %.2f', r_log(2) ) );
tt = title( sprintf( 'Histogram of Degree Distribution log  / firstonly = %d, threshold= %.2f', firstonly, threshold ) );
print('-depsc', sprintf('-f%d',fig+3),sprintf('graphD%dF%.2fR%dDlog.eps', firstonly, threshold,rr))
show_graph_d{1}=L;
show_graph_d{2}=C;
show_graph_d{3}=degree;
else
show_graph_d{1}=nan;
show_graph_d{2}=nan;
show_graph_d{3}=[];
end
return; 