import numpy as ap
import cv2

# load an color image is grayscale
img = cv2.imread('100.png')
cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.namedWindow('image',cv2.WINDOW_NORMAL)

cv2.imwrite('tmp.png',img)




