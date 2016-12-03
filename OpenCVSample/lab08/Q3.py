import cv2
import numpy as np
from matplotlib import pyplot as plt

''' I read the image and convert is to grayscale image'''
imgPart1  = cv2.imread('redbloodcell.jpg',0)

''' Get the size of the image '''
imageShape = imgPart1.shape
hight,weight = imageShape[0],imageShape[1]

''' Using the build-in function to get the darkest part of the image '''
imgB = imgPart1
retB,thB = cv2.threshold(imgB,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


''' change the grayscale of the image '''
''' Black to white and white to black, the gray part did not change '''
imgW = imgB * (thB/255) + (255-thB)

''' Using the build-in function to get the brightest part of the image '''
retW,thW = cv2.threshold(imgW,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)



''' Get the result of the first part '''
''' I set 100 as gray '''
''' I the value is less than 100 as black and greater than 100 as white'''
for i in range (hight):
  for j in range (weight):
    
    if thB[i,j] < 100:   # if the c
      imgPart1[i,j] = 0 # black
    
    elif thW[i,j] > 100:
      imgPart1[i,j] = 255 # white
    
    else:
      imgPart1[i,j] = 100 # gray



'''                          The Code for Q3 Part 2                          '''
img  = cv2.imread('redbloodcell.jpg')

''' Using the buildin function '''
Z = img.reshape((-1,3))

''' Convert to np.float32. Otherwise, it will overflow. '''
Z = np.float32(Z)

''' Define criteria, number of clusters(K) and apply kmeans() '''
# copy form
# http://docs.opencv.org/trunk/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
K = 3
ret,label,center=cv2.kmeans(Z,K,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

''' Convert back into uint8, and make original image using buildin function '''
center = np.uint8(center)
res = center[label.flatten()]
res2 = res.reshape((img.shape))






''' Plot the results with both part1 and part2'''
cv2.imshow('Q3 Part1',imgPart1)
cv2.waitKey(0)

cv2.imshow('Q3 Part2',res2)
cv2.waitKey(0)

