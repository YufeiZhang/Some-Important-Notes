import numpy as np
import cv2
from matplotlib import pyplot as plt

# copy form:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html


MIN_MATCH_COUNT = 10

img1 = cv2.imread('im1.jpg',0)          # queryImage
img2 = cv2.imread('im2.jpg',0)          # trainImage

# Initiate SIFT detector
sift = cv2.SIFT()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1,None)
kp2, des2 = sift.detectAndCompute(img2,None)

FLANN_INDEX_KDTREE = 0
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des2,des1,k=2)

# store all the good matches as per Lowe's ratio test.
good = []
for m,n in matches:
    if m.distance < 0.7*n.distance:
        good.append(m)


''' I add this line to get the initial h1,h1,w1,w2 '''
h1, w1 = img1.shape[:2]
h2, w2 = img2.shape[:2]
''' The following parts are also copied from the internet '''



# copy form:
# http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html

if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp2[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp1[m.trainIdx].pt for m in good ]).reshape(-1,1,2)
    # change kp2 to kp1 and kp1 to kp 2
    
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,1.0)
    matchesMask = mask.ravel().tolist()

    h,w = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

else:
    print "Not enough matches are found - %d/%d" % (len(good),MIN_MATCH_COUNT)
    matchesMask = None


# add if matchesMask
if matchesMask:
    # copy form
    # https://eclass.srv.ualberta.ca/mod/assign/view.php?id=1405467
    # Initialize a matrix to include all the coordinates in the image, from (0, 0), (1, 0), ..., to (w-1, h-1)
    # In this way, you do not need loops to access every pixel
    c = np.zeros((3, h2*w2), dtype=np.int)
    for y in range(h2):
      c[:, y*w2:(y+1)*w2] = np.matrix([np.arange(w2), [y] * w2,  [1] * w2])

    # Calculate the new image coordinates. Note that the third row needs to be normalized to 1
    # M is the homography matrix
    new_c = M * np.matrix(c)
    new_c = np.around(np.divide(new_c, new_c[2]))

    # The new coordinates may have negative values. Perform translation if needed
    x_min = np.amin(new_c[0])
    y_min = np.amin(new_c[1])
    x_max = np.amax(new_c[0])
    y_max = np.amax(new_c[1])
    if x_min < 0:
      t_x = -x_min
    else:
      t_x = 0
    if y_min < 0:
      t_y = -y_min
    else:
      t_y = 0

    # Initialize the final images to include every pixel of the stitched images  
    new_w = np.maximum(x_max, w1) - np.minimum(x_min, 0) + 1
    new_h = np.maximum(y_max, h1) - np.minimum(y_min, 0) + 1
    new_img1 = np.zeros((new_h, new_w), dtype=np.uint8)
    new_img2 = np.zeros((new_h, new_w), dtype=np.uint8)

    # Assign the first image
    new_img1[t_y:t_y+h1, t_x:t_x+w1] = img1

    # Assign the second image based on the newly calculated coordinates
    for idx in range(c.shape[1]):
      x = c[0, idx]
      y = c[1, idx]
      x_c = new_c[0, idx]
      y_c = new_c[1, idx]
      new_img2[y_c + t_y, x_c + t_x] = img2[y, x]

    # The stitched image can be simply obtained by averaging the two final images
    new_img = (new_img1 + new_img2) / 2

    ''' add the following lines to show the image '''
    cv2.imshow("Stitched Image", new_img)
    cv2.waitKey()
    cv2.destrayAllWindows()
    ''' It is the end of the code '''
