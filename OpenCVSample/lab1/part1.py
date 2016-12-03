import numpy as np
import cv2
from matplotlib import pyplot as plt
import matplotlib.image as mpimg

img = cv2.imread('test.png',0)

histList = np.zeros(256)
h,w = len(img),len(img[0])  # h -> height; w -> width

for line in img:
  for episode in line:
    histList[episode] += 1


plt.subplot(1,3,1)
imgtwo=mpimg.imread('test.png')
plt.title('Original Picture')
plt.imshow(imgtwo)

plt.subplot(1,3,2)
histgram = cv2.calcHist([img],[0],None,[256],[0,256])
plt.plot(histgram)
plt.xlim([0,256])
plt.title('Histogram Using Build-in Function')
plt.ylabel('h(i)')

plt.subplot(1,3,3)
plt.plot(histList)
plt.title('Histogram Using My Method')
plt.ylabel('h(i)')

plt.show()



