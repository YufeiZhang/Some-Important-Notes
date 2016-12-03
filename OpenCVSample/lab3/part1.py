import cv2
import numpy as np
from matplotlib import pyplot as plt

'''
Part I (20%) Computing a Laplace filter in opencv/python.

  Create a 3-by-3 matrix that has positive 8 at the center and -1 elsewhere.
  Open a grayscale image (any image of your choice). 
  Filter the grayscale image with the 3-by-3 matrix. 
  Display the result. Add the input image to the filtered image. 
'''

# read a file as grayscale image
img = cv2.imread('test.jpg',0)

# set the kernel of  laplasion
kernel = np.matrix('-1.0 -1.0 -1.0; -1.0 8.0 -1.0; -1 -1 -1')

# calculate the laplasion image
laplase = cv2.filter2D(img,-1,kernel)

# display the initial and Laplasion image
plt.subplot(121),plt.imshow(img,cmap = 'gray'),plt.title('Original')
plt.xticks([]), plt.yticks([])

plt.subplot(122),plt.imshow(laplase,cmap = 'gray'),plt.title('Absolute Laplace')
plt.xticks([]), plt.yticks([])

plt.show()