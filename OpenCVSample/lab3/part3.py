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
imgInit = cv2.imread('damaged_cameraman.bmp',0)
imgMask = cv2.imread('damage_mask.bmp',0)

# get the size of the picture
hight,width = len(imgInit),len(imgInit[0])

# copy the initial image and named 
newImage = imgInit


''' The restore function '''
def restroe(imgInit,Gaussian,imgMask):
  for h in range(hight):          # for each row of the image
    for w in range(width):        # for esch pixel of one row of the image
      if imgMask[h][w] == 255.0:
        # if not masked -> set Gaussian to the inital imga
        Gaussian[h][w] = imgInit[h][w]
      else:
        # if masked -> Gaussian is fine
        pass
  return Gaussian


''' The Main Function '''
def main(imgInit,newImage,iteration):
  for i in range(iteration):
    Gaussian = cv2.GaussianBlur(newImage,(3,3),0)
    newImage = restroe(imgInit,Gaussian,imgMask)
  return Gaussian


''' Call the main function '''
outputA = main(imgInit,imgInit,3)   # 3 times is not good enough
outputB = main(imgInit,imgInit,30)  # 30 times is good enough


''' Displayt the result '''
plt.subplot(131),plt.imshow(imgInit,cmap = 'gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(132),plt.imshow(outputA,cmap = 'gray'),plt.title('Gaussian 3 Times')
plt.xticks([]), plt.yticks([])

plt.subplot(133),plt.imshow(outputB,cmap = 'gray'),plt.title('Gaussian 30 Times')
plt.xticks([]), plt.yticks([])

plt.show()