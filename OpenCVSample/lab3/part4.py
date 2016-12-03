from math import *
import numpy as np
import cv2
from matplotlib import pyplot as plt
from matplotlib import image  as mpimg


'''
  Part III (60%) An application of filtering in OpenCV: Simple image inpainting.
  
  Write a program in OpenCV+Python to accomplish a simple image inpainting.
  This example and demo were shown in the lecture.
  
  You are given a damaged image and a mask image with damaged pixels.
  
  It is an iterative algorithm. 
  At every iteration, your program
    (a) blurs the entire damaged image with a Gaussian smoothing filter;
    (b) with help of the mask image, restores only the undamaged pixels. 
    (C) Repeat these two steps (a) and (b) a few times until all damaged pixels are infilled.
'''


# read the dammaged picture and the mask
damageImage = cv2.imread('damaged_cameraman.bmp',0)

# get the size of the picture
hight,width = len(damageImage),len(damageImage[0])

# copy the initial image and named 
newImage = damageImage


''' The restore function '''
def restroe(damageImage,Gaussian):
  for h in range(hight):          # for each row of the image
    for w in range(width):        # for esch pixel of one row of the image
      if 240 <= damageImage[h][w] <= 255.0:
        pass
      else:
        Gaussian[h][w] = damageImage[h][w]
  return Gaussian


''' The Main Function '''
def main(damageImage,newImage,iteration):
  for i in range(iteration):
    Gaussian = cv2.GaussianBlur(newImage,(3,3),0)
    newImage = restroe(damageImage,Gaussian)
  return Gaussian


''' Call the main function '''
outputA = main(damageImage,damageImage,10)   # 10 times is not good enough
outputB = main(damageImage,damageImage,40)   # 30 times is good enough


''' Displayt the result '''
plt.subplot(131),plt.imshow(damageImage,cmap = 'gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(132),plt.imshow(outputA,cmap = 'gray'),plt.title('Gaussian 10 Times')
plt.xticks([]), plt.yticks([])

plt.subplot(133),plt.imshow(outputB,cmap = 'gray'),plt.title('Gaussian 40 Times')
plt.xticks([]), plt.yticks([])

plt.show()