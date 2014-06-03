function correlogram(A,B)
%The function allows the plotting of a correlogram between two vectors, whose elements are contained in .txt or .csv files, used as input. To use this function, please digit:
%correlogram('nameFile1','nameFile2');
%where the input are two filenames contained in the workig directory. Please make sure the formatting of the files are numbers separated by "," and the decimal mark is "."
%The function will automatically save the correlogram in a .jpeg image in the working directory.
%To plot an autocorrelogram, simply repeat the same filename in both input fields.


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
    
d=A(1:(length(A)-4)); %extracting filename
e=B(1:(length(B)-4));

fine=max(a(length(a),1),b(length(b),1));
temp=0:0.001:fine; %creating a vector of the same size as the longest input vector


maxlags= 200;
t1_binned = histc(a(:,1), temp); %timestamps to binned
t2_binned = histc(b(:,1), temp);

%making sure the two files are the same size, otherwise the 
if (size(t1_binned)~=size(t2_binned))
    disp('WARNING: the input vectors are not the same size. Correlation cannot be calculated, please zero-pad the shorter one');
end

xc = xcorr(t1_binned, t2_binned,maxlags); % actual crosscorrelation

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
xcb=xc(200-29:200+31);

%cubic spline interpolation
%p=spline(xx,xcb);
%x=linspace(-30,30,2001);

%plotting the interpolated function
n=figure;
plot(xx,xcb);

%saving the jpeg file
filename=[d e];
print(n,'-djpeg',filename);



%unused code, discard



%temp=temp';

%v1= zeros(length(temp),1);
%i=1;

%while ((round(a(i,2)*10)<=length(temp)) && i<length(a))
%    v1(round(a(i,2)*10))=1;
%    i=i+1;
%end


%v2= zeros(length(temp),1);
%i=1;

%while (round(b(i,2)*10)<=length(temp) && i<length(b))
%    v2(round(b(i,2)*10))=1;
%    i=i+1;
%end

%ris=xcorr(v1,v2);

%ris(floor(length(ris)/2)-floor(length(ris)/100):floor(length(ris)/2)+floor(length(ris)/100))=zeros(2*floor(length(ris)/100)+1,1);


%v=[];

%for i=1:40
%    l=floor(length(ris)/40);
%    v(i)=mean(ris(1+l*(i-1):l*i));
%end

%v(20)=0;

%figure;
%bar(v);


return
