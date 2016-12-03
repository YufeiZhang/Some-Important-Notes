% Figure 1 shows I with overlaid bounding boxes for instances of T
% Figure 2 shows the result after antialiasing
close all;
clear all;
I = imread('I.jpg');
I = double(rgb2gray(I));
T = imread('T.jpg');
T = double(rgb2gray(T));
C = normxcorr2(T,I);
Points = C >=0.45; % 0.4 to 0.5
[y,x] = find(Points);

figure(1),imagesc(I),colormap(gray);
for i=1:length(x)
    rectangle('Position', [x(i)-size(T,2),y(i)-size(T,1),size(T,2),size(T,1)], 'EdgeColor', 'red' );
end

FI = fft2(I);
FT = fft2(T);

filt = fspecial('gaussian', [9 9], 2);
filtI = fft2(filt, size(I,1),size(I,2));
filtT = fft2(filt, size(T,1),size(T,2));

antiI = real(ifft2(FI.*filtI));
antiT = real(ifft2(FT.*filtT));

Co = normxcorr2(antiT,antiI);
Points = Co >= 0.86; 
[y,x] = find(Points);

figure(2),imagesc(I),colormap(gray);
for i=1:length(x)
    rectangle('Position', [x(i)-size(T,2),y(i)-size(T,1),size(T,2),size(T,1)], 'EdgeColor', 'green' );
end