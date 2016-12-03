import numpy as np
import cv2
from matplotlib import pyplot as plt

''' copy from part1 '''
''' get the data of the grayscale image '''
imgOld = cv2.imread('PeppersBayerGray.bmp',0)     # read the picture\\
img = np.array (imgOld, dtype='int64')            # to fix the overflow error
imgRGB = cv2.imread('PeppersBayerGray.bmp')
height = len(img)    # 384
width  = len(img[0]) # 512

''' create 3 masks '''
imgG = np.zeros((height, width),np.float32)
imgR = np.zeros((height, width),np.float32)
imgB = np.zeros((height, width),np.float32)


''' get green mask '''
for h in range(height):
  for w in range(width):
    
    if h%2 == 0: # line 0,2,4, ... , 382
      if w == width-1: # col = 511
        if h == 0: imgG[h][w] = (img[h][w-1] + img[h+1][w]) /2
        else:      imgG[h][w] = (img[h-1][w] + img[h+1][w]) /2
    
      else: # col != 511
        if w%2 == 1: # w = 1,3,5 ... , 509
          if h == 0: imgG[h][w] = (img[h][w-1] + img[h][w+1]) /2
          else:      imgG[h][w] = ((img[h][w-1]+img[h][w+1])/2+(img[h-1][w]+img[h+1][w])/2) /2

    else: # line 1,3,5, ... , 383
      if w == 0: # col = 0
        if h == height-1: imgG[h][w] = (img[h][w+1] + img[h-1][w]) /2
        else:             imgG[h][w] = (img[h-1][w] + img[h+1][w]) /2
      
      else: # col != 0
        if w%2 == 0: # w = 1,3,5 ... , 509
          if h == height-1: imgG[h][w] = (img[h][w-1] + img[h][w+1]) /2
          else:             imgG[h][w] = ((img[h][w-1]+img[h][w+1])/2 + (img[h-1][w]+img[h+1][w])/2)/2


''' get red mask '''
for h in range(height):
  for w in range(width):
    
    if h%2 == 0:
      if w%2 == 0:
        if w == 0: imgR[h][w] = img[h][w+1]
        else: imgR[h][w] = (img[h][w+1]+img[h][w-1])/2

    else:
      if w%2 == 0:
        if w == 0:
          if h != 383: imgR[h][w] = (img[h-1][w+1] + img[h+1][w+1])/2
          else: imgR[h][w] = img[h-1][w+1]
        else:
          if h != 383: imgR[h][w] = (img[h-1][w+1]+img[h+1][w+1]+img[h-1][w-1]+img[h+1][w-1])/4
          else: imgR[h][w] = (img[h-1][w+1]+img[h-1][w-1])/2

      else:
        if h != 383: imgR[h][w] = (img[h-1][w]+img[h+1][w])/2
        else: imgR[h][w] = img[h-1][w]


''' get blue mask '''
for h in range(height):
  for w in range(width):
    
    if h%2 == 1:
      if w%2 == 1:
        if w == width-1: imgB[h][w] = img[h][w-1]
        else: imgB[h][w] = (img[h][w+1]+img[h][w-1])/2
  
    else:
      if w%2 == 1:
        if w == width-1:
          if h != 0: imgB[h][w] = (img[h-1][w-1] + img[h+1][w-1])/2
          else: imgB[h][w] = img[h+1][w-1]
        else:
          if h != 0: imgB[h][w] = (img[h-1][w+1]+img[h+1][w+1]+img[h-1][w-1]+img[h+1][w-1])/4
          else: imgB[h][w] = (img[h+1][w+1]+img[h+1][w-1])/2
    
      else:
        if h != 0: imgB[h][w] = (img[h-1][w]+img[h+1][w])/2
        else: imgB[h][w] = img[h+1][w]



''' Start of Part 2 '''
DR = imgR-imgG
DB = imgB-imgG

MR = cv2.medianBlur(DR,3)
MB = cv2.medianBlur(DB,3)

IRR = MR + imgG
IBB = MB + imgG

irrMax = np.amax(IRR)
irrMin = np.amin(IRR)

ibbMax = np.amax(IBB)
ibbMin = np.amin(IBB)

IRR = 255*(IRR-irrMin)/(irrMax-irrMin)
IBB = 255*(IBB-ibbMin)/(ibbMax-ibbMin)


''' get the output '''
for h in range(height):
  for w in range(width):
    imgRGB[h][w][0] = IBB[h][w]
    imgRGB[h][w][1] = imgG[h][w]
    imgRGB[h][w][2] = IRR[h][w]

cv2.imshow("RGBImage", imgRGB)
cv2.waitKey()


