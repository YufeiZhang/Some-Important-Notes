import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('100.png')

blur = cv2.blur(img,(5,5))
#blur = cv2.GaussianBlur(img,(5,5),0)
#median = cv2.medianBlur(img,5)
cv2.imshow('image',blur)

cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()