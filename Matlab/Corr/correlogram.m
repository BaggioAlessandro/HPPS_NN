function correlogram(A,B)
%The function allows the plotting of a correlogram between two vectors, whose elements are contained in .txt or .csv files, used as input. To use this function, please digit:
%correlogram('nameFile1','nameFile2');
%where the input are two filenames contained in the workig directory. Please make sure the formatting of the files are numbers separated by "," and the decimal mark is "."
%The function will automatically save the correlogram in a .jpeg image in the working directory.
%To plot an autocorrelogram, simply repeat the same filename in both input fields.

data = dlmread('01.txt', ' ');

a=csvread(A); %reading file
a=a'; %Transpose because of the delimited(column) data
b=csvread(B);
b=b'; %Transpose because of the delimited(column) data

if(size(a,1)==1)
    a=a';
end
    
if(size(b,1)==1)
    b=b';
end
a = a + (1e-4 * 5)
b = b + (1e-4 * 5)
d=A(1:(length(A)-4)); %extracting filename
e=B(1:(length(B)-4));

fine=max(a(length(a),1),b(length(b),1));
temp=0:0.001:300; %creating a vector of the same size as the longest input vector

maxlags= 5;
t1_binned = histc(a(:,1), temp); %timestamps to binned
t2_binned = histc(b(:,1), temp);


t1_binnedBeta = data(1:300000); %timestamps to binned
t2_binnedBeta = data(300001:600000);
disp(length(t1_binned));
if t1_binned(2:300001) ~= t1_binnedBeta
    disp('lucaculo')
end
%making sure the two files are the same size, otherwise the 
if (size(t1_binned)~=size(t2_binned))
    disp('WARNING: the input vectors are not the same size. Correlation cannot be calculated, please zero-pad the shorter one');
end

xc = xcorr(t2_binned(1:fine*1000), t1_binned(1:fine*1000),maxlags); % actual crosscorrelation
disp(xc);


%smoothing: are we going to do it?
%xc = xc(round(length(xc)/2)-2000:round(length(xc)/2)+2000);

%for the AC at a shift of 0 we need to delete the peak because otherwise it's too big
if(size(a)==size(b))
    if (a==b)
        xc(201)=0; % maxlags+1=201
    end
end


%creating the two vectors for the plotting (from -30 to +30)
xx=-30:30;

%cubic spline interpolation
%p=spline(xx,xcb);
%x=linspace(-30,30,2001);

%plotting the interpolated function
