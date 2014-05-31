function mainv2
numn = 10;
numc = 300000;
factor = 1;
threshold = 0.45;

start_all = tic;

%NON FARE CAZZATE BAGGIO, onn sovrascrivere mai l'histogram reale
%delayHistogram('01',numn,numc)
%media(numn, numc)
%NormalizeHist_v2(numn)
%CompressHist(numn, factor)
edgesCalc_v3(threshold,numn)

t_all = toc(start_all)
