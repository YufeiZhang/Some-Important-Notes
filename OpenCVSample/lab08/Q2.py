import cv2    
import cv2.cv as cv # here
import numpy as np

''' open the images '''
img = cv2.imread('coins.jpg',0)
img = cv2.medianBlur(img,5)
imgCoins = cv2.imread('coins.jpg')

''' using the buildin function '''
circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,30, param1=70,param2=30,minRadius=10,maxRadius=70)

circles = np.uint16(np.around(circles))

for i in circles[0,:]:
    ''' draw the outer circle using the buildin function'''
    cv2.circle(imgCoins,(i[0],i[1]),i[2],(0,255,0),2)
    
    ''' draw the center of the circle using the buildin function'''
    cv2.circle(imgCoins,(i[0],i[1]),2,(0,0,255),3)

''' show the image '''
cv2.imshow('Detected Circles',imgCoins)
cv2.waitKey(0)
cv2.destroyAllWindows()