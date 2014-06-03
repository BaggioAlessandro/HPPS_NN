function main
numn = 10;
numc = 300000;
factor = 10;
threshold = 0.1;

start_all = tic;

%NON FARE CAZZATE BAGGIO, onn sovrascrivere mai l'histogram reale
%delayHistogram('01',numn,numc)
%NormalizeHist(numn)
%CompressHist(numn, factor)
edgesCalc(threshold,numn)


t_all = toc(start_all)
