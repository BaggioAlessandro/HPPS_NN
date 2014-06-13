function correlogram_topology()
import my_save2D
import my_save3D
%The function allows the plotting of a correlogram between two vectors, whose elements are contained in .txt or .csv files, used as input. To use this function, please digit:
%correlogram('nameFile1','nameFile2');
%where the input are two filenames contained in the workig directory. Please make sure the formatting of the files are numbers separated by "," and the decimal mark is "."
%The function will automatically save the correlogram in a .jpeg image in the working directory.
%To plot an autocorrelogram, simply repeat the same filename in both input fields.

N_NEURONS = 9;
N_CAMP = 3000000;
MAX_LAGS = 2000;
f=10;
data = zeros(N_NEURONS,N_CAMP);
for i=0:(N_NEURONS-1)
    data(i+1,:) = dlmread(strcat(strcat('Input\10_new_model\',int2str(i)),'_01.txt'), ' ');
end
edges_ecc = zeros(N_NEURONS, N_NEURONS);
edges_ini = zeros(N_NEURONS, N_NEURONS);
my_save2D('edges_matlab', edges_ecc, N_NEURONS, '%g ');

xx=-30:30;
for i=1:N_NEURONS
    t1_binned = data(i,:);
    for j=1:N_NEURONS
        t2_binned = data(j,:);
       

        xc = xcorr(t2_binned, t1_binned,MAX_LAGS); % actual crosscorrelation
        d1=zeros(floor(length(xc)./f)+1,1);
        for i=1:floor(length(xc)./f)
          d1(i)=sum(xc(((i-1)*f)+1:i*f));  %1 indica che la somma è fatta lungo la prima dimensione
        end
        if i<length(xc)./f %gestisce la posizione 501
          i=i+1;
          d1(i)=sum(xc((i-1)*f+1:end));
        end
        d1 = d1';
        d1(MAX_LAGS/f+1)=0;
        %prendi l'intorno dello 0
        xcb=d1(MAX_LAGS/f-29:MAX_LAGS/f+31);
        %calculating mean and standard deviation
        n = 2*MAX_LAGS;
        mean = sum(d1(:),1)/n; 
        stdev = sqrt(sum((d1 - mean).^2)/n);

        flag1=0;flag2=0;massimo1=0;massimo2=0;

        for h=31:35
            if((xcb(h)>(mean+stdev*3.09)) && (xcb(h)>massimo1))
                massimo1=xcb(h);
                flag1 = 1;
            end
        end
        if(flag1 ~= 0)
            edges_ecc(i,j) = 1;
            disp('conn');
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
            disp('conn');
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
edges_ecc;
edges_ecc = edges_ecc - diag(diag(edges_ecc));
my_save2D('edges_matlab', edges_ecc, N_NEURONS, '%g ');