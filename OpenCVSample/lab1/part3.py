import numpy as np
import math
import cv2
from matplotlib import pyplot as plt
from matplotlib import image as mpimg


# part 3
'''
    read 2 images and compare the similarity of them
'''

# read 2 pictures
imgA = cv2.imread('test.png',0)
imgB = cv2.imread('test.png',0)
histgramA = cv2.calcHist([imgA],[0],None,[256],[0,256])
histgramB = cv2.calcHist([imgB],[0],None,[256],[0,256])


# normalize 2 pictures
for i in range(256):
  histgramA[i][0] = histgramA[i][0]/(M*N*1.0)
  histgramB[i][0] = histgramB[i][0]/(M*N*1.0)

#compute the Bhattacharya Coefficient
sumBC = 0
for i in range(256):
  sumBC += math.sqrt(histgramA[i][0] * histgramB[i][0])
print sumBC

