import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


# read the picture and calculate the histogram of it
img = cv2.imread('test.png',0)
histgramInitial = cv2.calcHist([img],[0],None,[256],[0,256])

# get the width and height of a picture respectively
M,N = len(img[0]),len(img)

# initialize the cumulative histogram
cumulgramInitial = np.zeros(256)

# compute the cumulative histogram by the histogram
for i in range(256):
  cumulgramInitial[i] = histgramInitial[i][0] + cumulgramInitial[i-1]

# copy the image as imgI
imgI = img


# get equalized picture using the equation
for i in range(N):
  for j in range(M):
    img[i,j] = int((255 * cumulgramInitial[ img[i,j] ] ) / (M*N) +0.5)

# get the histgram of the equalized image
histgramEqualize = cv2.calcHist([img],[0],None,[256],[0,256])

# display the initial image and equalized image and their histograms
plt.subplot(2,2,1)
plt.title('Initial Picture')
plt.imshow(cv2.imread('test.png'))

plt.subplot(2,2,2)
plt.title('Equalization Picture')
plt.gray()
plt.imshow(img)

plt.subplot(2,2,3)
plt.plot(histgramInitial ,'b')
plt.plot(histgramEqualize,'r')
plt.legend(('Initial','Equalized'), loc = 'upper right')
plt.xlim([0,256])
plt.title('Initial-Histogram vs Equalized-Histogram')
plt.ylabel('h(i)')

plt.show()