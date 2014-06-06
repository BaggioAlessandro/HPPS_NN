function corrbarre(A,B)
%The function allows the plotting of a correlogram between two vectors, whose elements are contained in .txt or .csv files, used as input. To use this function, please digit:
%correlogram('nameFile1','nameFile2');
%where the input are two filenames contained in the workig directory. Please make sure the formatting of the files are numbers separated by "," and the decimal mark is "."
%The function will automatically save the correlogram in a .jpeg image in the working directory.
%To plot an autocorrelogram, simply repeat the same filename in both input fields.


a=csvread(A); 
b=csvread(B);

if(size(a,1)==1)
    a=a';
end
    
if(size(b,1)==1)
    b=b';
end
    
d=A(1:(length(A)-4)); %extracting filename
e=B(1:(length(B)-4));

fine=max(a(length(a),1),b(length(b),1));
temp=0:0.0005:fine; %creating a vector of the same size as the longest input vector


maxlags= 200;
t1_binned = histc(a(:,1), temp); %timestamps to binned
t2_binned = histc(b(:,1), temp);

%making sure the two files are the same size, otherwise the 
if (size(t1_binned)~=size(t2_binned))
    disp('WARNING: the input vectors are not the same size. Correlation cannot be calculated, please zero-pad the shorter one');
end

xc = xcorr(t1_binned, t2_binned,maxlags,'coeff'); % actual crosscorrelation

%smoothing: are we doing it?
xc = xc(round(length(xc)/2)-200:round(length(xc)/2)+200);

%at a shift of 0 we need to delete the peak because otherwise
%it's too high
xc(201)=0;


%creating the two vectors for the plotting (from -30 to +30)
xx=-30:30;
%prendi l'intorno dello 0
xcb=xc(maxlags-29:maxlags+31);


%plotting the interpolated function
n=figure;
plot(xx,xcb);

bar(abs(xc));

%saving the jpeg file
filename=[d e];
print(n,'-djpeg',filename);


%Automatic recognition of peaks and troughs

%PEAKS: Assuming a normal distribution of the dataset, we are identifying
%the outliers which are higher than the 99.9th percentile of the gaussian curve. 

%calculating mean and standard deviation
n = 2*maxlags;
mean = sum(xc)/n; 
stdev = sqrt(sum((xc - mean).^2)/n);

flag1=0;flag2=0;massimo1=0;massimo2=0;

%if more than one value is higher than 99.9th percentile, identify the time
%shift in which there's the absolute maximum value 

%Peaks at positive time shifts
%3.09????     0.5????
for i=31:35
   if((xcb(i)>(mean+stdev*3.09)) && (xcb(i)>massimo1))
            massimo1=xcb(i);
            istante=xx(i)*0.5;
            flag1 = 1;
    end
end
if(flag1 ~= 0)
    fprintf('Peak at %f ms. An excitatory connection is present.\n', istante);
end
%Same for negative time shifts
for i=25:30
    if((xcb(i)>(mean+stdev*3.09)) && (xcb(i)>massimo2))
            massimo2=xcb(i);
            istante=xx(i)*0.5;
            flag2=1;
    end
end
if(flag2 ~= 0)
    fprintf('Peak at %f ms. An excitatory connection is present.\n', istante);
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
    fprintf('There is an inhibitory connection.\n');
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
    fprintf('There is an inhibitory connection.\n');
end
