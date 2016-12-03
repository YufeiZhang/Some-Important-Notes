import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('beatles.jpg',0)
plt.hist(img.ravel(),256,[0,256])
plt.xlim([0,256])
plt.show()