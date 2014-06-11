function correlogram_topology()
%The function allows the plotting of a correlogram between two vectors, whose elements are contained in .txt or .csv files, used as input. To use this function, please digit:
%correlogram('nameFile1','nameFile2');
%where the input are two filenames contained in the workig directory. Please make sure the formatting of the files are numbers separated by "," and the decimal mark is "."
%The function will automatically save the correlogram in a .jpeg image in the working directory.
%To plot an autocorrelogram, simply repeat the same filename in both input fields.

data = dlmread('01.txt', ' ');
N_NEURONS = 10;
N_CAMP = 300000;
MAX_LAGS = 200;
edges_ecc = zeros(N_NEURONS, N_NEURONS);
edges_ini = zeros(N_NEURONS, N_NEURONS);
xx=-30:30;
for i=1:N_NEURONS
    t1_binned = data(((i-1)*N_CAMP)+1:(i*N_CAMP));
    for j=1:N_NEURONS
        tic;
        t2_binned = data(((j-1)*N_CAMP)+1:(j*N_CAMP));
       

        xc = xcorr(t2_binned, t1_binned,MAX_LAGS); % actual crosscorrelation
        toc
        xc(MAX_LAGS+1)=0;
        %prendi l'intorno dello 0
        xcb=xc(MAX_LAGS-29:MAX_LAGS+31);
        %calculating mean and standard deviation
        n = 2*MAX_LAGS;
        mean = sum(xc)/n; 
        stdev = sqrt(sum((xc - mean).^2)/n);

        flag1=0;flag2=0;massimo1=0;massimo2=0;

        for h=31:35
            if((xcb(h)>(mean+stdev*3.09)) && (xcb(h)>massimo1))
                massimo1=xcb(h);
                flag1 = 1;
            end
        end
        if(flag1 ~= 0)
            edges_ecc(i,j) = 1;
        end
        %Same for negative time shifts
        for h=25:30
            if((xcb(h)>(mean+stdev*3.09)) && (xcb(h)>massimo2))
                massimo2=xcb(h);
                flag2=1;
            end
        end
        if(flag2 ~= 0)
            edges_ecc(j,i) = 1;
        end
        
        
    
        %TROUGHS: if the short-latency waveform is exponential, we consider the
        %connection existing and inhibitory

        %fitting an exponential curve on the data between 1 ms and 10 ms.
        %Unfortunately the only way to fit an exponential in matlab is finding the
        %polynomial fitting for the logarithm of xcb which gives the coefficients
        %for the exponential function
        %For a positive number of shifts
        x_exp=32:52;
        y_exp=xcb(x_exp);
        y_exp=y_exp';
        P= polyfit(x_exp, log(y_exp), 1);
        fun=polyval(P,x_exp);
        %if the fitting is good enough, we can say the curve is an exponential and
        %the trough is found.

        yresid = y_exp - fun;
        SSresid=sum(yresid.^2);
        SStotal=(length(y_exp)-1)*var(y_exp);
        %R2 is defined as 1-the residual sum of squares/N-1*variance (see
        %statistics and linear regression for more information)
        rsq=1-SSresid/SStotal;

        if(rsq>0.9)
            edges_ini(i,j) = 1;
        end
    
        %Same for a negative number of shifts
        x_exp=10:30;
        y_exp=xcb(x_exp);
        y_exp=y_exp';
        P= polyfit(x_exp, log(y_exp), 1);
        %la rigua che segue è sovrascritta dalla riga dopo
        fun=polyval(P,x_exp);

        %if the fitting is good enough, we can say the curve is an exponential and
        %the trough is found.

        yresid = log(y_exp) - fun;
        SSresid=sum(yresid.^2);
        SStotal=(length(y_exp)-1)*var(log(y_exp));
        %R2 is defined as 1-the residual sum of squares/N-1*variance (see
        %statistics and linear regression for more information)
        rsq=1-SSresid/SStotal;

        if(rsq>0.8)
            edges_ini(j,i) = 1;
        end
    end
end

disp('lucaculo');