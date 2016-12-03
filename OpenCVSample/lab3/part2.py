from math import *
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image  as mpimg

'''
  Part II (20%) Median and Gaussian filters
  
  Here's an image corrupted with salt & pepper noise. 
  Apply a median filter to remove the noise. 
  Also, apply a Gaussian filter to the same noisy image. 
  Which filter was more successful?  (Median is better)
  You can use any OpenCV functions you like.
'''

# read an image as grayscale image
img = cv2.imread('noisy.jpg',0)

# the smaller filter size gives the better resulte
kernelSize = 3

# get the Caussian and Median filter respectively
Gaussian = cv2.GaussianBlur(img,(3,3),0)
Median = cv2.medianBlur(img,kernelSize)

# display the results
plt.subplot(131),plt.imshow(img,cmap = 'gray'),plt.title('Original Picture')
plt.xticks([]), plt.yticks([])

plt.subplot(132),plt.imshow(Gaussian,cmap = 'gray'),plt.title('Gaussian Filtering')
plt.xticks([]), plt.yticks([])

plt.subplot(133),plt.imshow(Median,cmap = 'gray'),plt.title('Median Filtering')
plt.xticks([]), plt.yticks([])

plt.show()

