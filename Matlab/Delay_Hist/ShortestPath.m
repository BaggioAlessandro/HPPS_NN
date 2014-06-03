function LTable = ShortestPath( X, L, LTable, Edges )
% Updates vector LTable with length of shortest path from node X to N-1 other nodes.
% To use this function, initialize LTable as follows:
% LTable = repmat(inf,1,N); LTable(X) = 0;
% Edges is a NxN matrix: non-zero Edges(i,j) indicates an edge i->j
% e.g. load edges; X=54; LTable=repmat(inf,1,64); LTable(X)=0; ShortestPath(X,1,LTable,edges)

ToVisitList = [];
for n = find( Edges(X,:) )          % find list of edges emanating from X
    if ( LTable(n) > L )            % if shortest path stored > current path length
        LTable(n) = L;
        ToVisitList(end+1) = n;
    end
end

for n = ToVisitList
    LTable = ShortestPath( n, L+1, LTable, Edges );
end

return;