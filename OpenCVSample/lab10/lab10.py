import os
import sys
import cv2
import numpy as np
import math
import time




def readTrackingData(filename):
    if not os.path.isfile(filename):
        print "Tracking data file not found:\n ", filename
        sys.exit()

    data_file = open(filename, 'r')
    lines = data_file.readlines()
    no_of_lines = len(lines)
    data_array = np.zeros((no_of_lines, 8))
    line_id = 0
    for line in lines:
        words = line.split()
        if len(words) != 8:
            msg = "Invalid formatting on line %d" % line_id + " in file %s" % filename + ":\n%s" % line
            raise SyntaxError(msg)
        coordinates = []
        for word in words:
            coordinates.append(float(word))
        data_array[line_id, :] = coordinates
        line_id += 1
    data_file.close()
    return data_array


def writeCorners(file_id, corners):
    # write the given corners to the file
    corner_str = ''
    for i in xrange(4):
        corner_str = corner_str + '{:5.2f}\t{:5.2f}\t'.format(corners[0, i], corners[1, i])
    file_id.write(corner_str + '\n')


def drawRegion(img, corners, color, thickness=1):
    # draw the bounding box specified by the given corners
    for i in xrange(4):
        p1 = (int(corners[0, i]), int(corners[1, i]))
        p2 = (int(corners[0, (i + 1) % 4]), int(corners[1, (i + 1) % 4]))
        cv2.line(img, p1, p2, color, thickness)


def initTracker(img, corners):
    # initialize your tracker with the first frame from the sequence and
    # the corresponding corners from the ground truth
    # this function does not return anythinm
    global tlX,tlY,trX,trY,brX,brY,blX,blY
    global frame,p0,old_gray,lk_params,allX,allY
    global hist,histP3
    
    currentCorners,frame = corners,img
    
    tlX = int(currentCorners[0][0]) # left top x change
    tlY = int(currentCorners[1][0]) # left top y change
    
    trX = int(currentCorners[0][1]) # right top x change
    trY = int(currentCorners[1][1]) # right top y change
    
    brX = int(currentCorners[0][2]) # right bottom x change
    brY = int(currentCorners[1][2]) # right bottom y change
    
    blX = int(currentCorners[0][3]) # left bottom x change
    blY = int(currentCorners[1][3]) # left bottom y change
    

    
    ''' Using the Flow '''
    ''' The following code are copied from:
        https://github.com/abidrahmank/OpenCV2-Python-Tutorials/blob/master/source/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.rst
    '''
    # params for ShiTomasi corner detection
    feature_params = dict( maxCorners = 100,
                      qualityLevel = 0.3,
                      minDistance = 3,
                      blockSize = 3)

    # Parameters for lucas kanade optical flow
    lk_params = dict( winSize  = (15,15),
                     maxLevel = 2,
                     criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

    # Take first frame and find corners in it
    old_frame = img
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    

    ''' change the point valuse to our own '''
    p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **feature_params)

    for i in range(len(p0)):
      if p0[i][0][0] < tlX or p0[i][0][0] > trX:
        p0[i][0][0] = (tlX+trX+brX+blX)//4
      if p0[i][0][1] < tlY or p0[i][0][1] > trY:
        p0[i][0][1] = (tlY+trY+brY+blY)//4

    p0[0][0][0] = tlX
    p0[0][0][1] = tlY
    p0[1][0][0] = trX
    p0[1][0][1] = trY
    p0[2][0][0] = brX
    p0[2][0][1] = brY
    p0[3][0][0] = blX
    p0[3][0][1] = blY

    # Create a mask image for drawing purposes
    mask = np.zeros_like(old_frame)
    pass

def updateTracker(img):
    # update your tracker with the current image and return the current corners
    # at present it simply returns the actual corners with an offset so that
    # a valid value is returned for the code to run without errors
    # this is only for demonstration purpose and your code must NOT use actual corners in any way
    global tlX,tlY,trX,trY,brX,brY,blX,blY,term_crit,currentCorners
    global frame,p0,old_gray,lk_params,allX,allY
    global hist,histP3
    
    ''' The following code are copied from:
        https://github.com/abidrahmank/OpenCV2-Python-Tutorials/blob/master/source/py_tutorials/py_video/py_lucas_kanade/py_lucas_kanade.rst
    '''
    
    frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # calculate optical flow
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    
    # Select good points
    good_new = p1[st==1]
    good_old = p0[st==1]
    
    
    allX,allY = [],[]
    allOldX,allOldY = [],[]
    
    ''' I edit the code from here '''
    # draw the tracks
    for i,(new,old) in enumerate(zip(good_new,good_old)):
      X,Y = new.ravel()
      allX.append(X)
      allY.append(Y)
    

    # Now update the previous frame and previous points
    old_gray = frame_gray.copy()
    p0 = good_new.reshape(-1,1,2)
    
    x5 = np.mean(allX)
    y5 = np.mean(allY)
    
    x1,y1,x2,y2,x3,y3,x4,y4 = allX[0],allY[0],allX[1],allY[1],allX[2],allY[2],allX[3],allY[3]
    '''
    if abs((abs(x3-x1)**2+(y1-y3)**2) - (a3-a1)**2+(b1-b3)**2)) > abs((x2-x4)**2+(y2-y4)**2) - (a2-a4)**2+(b2-b4)**2)):
      sqrt(abs((x2-x4)**2+(y2-y4)**2) - (a2-a4)**2+(b2-b4)**2))/)
      
    '''

    if (abs(abs(x1-x5)-abs(x3-x5))>1): x3 = 2*x5-x1
    if (abs(abs(y1-y5)-abs(y3-y5))>1): y3 = 2*y5-y1
    if (abs(abs(x4-x5)-abs(x2-x5))>1): x2 = 2*x5-x4
    if (abs(abs(y4-y5)-abs(y2-y5))>1): y2 = 2*y5-y4
    if (abs(abs(x4-x5)-abs(x2-x5))>1): x4 = 2*x5-x2
    if (abs(abs(y4-y5)-abs(y2-y5))>1): y4 = 2*y5-y2

    if ((x1-x3)**2+(y1-y3)**2) - ((x2-x4)**2+(y2-y4)**2) > 900:
      x2 = x3
      y2 = y1
      x4 = x1
      y4 = y3
  
    currentCorners = [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
    ''' Don't modify the code below here '''
    currentCorners = np.array(currentCorners).T
    
    return currentCorners


if __name__ == '__main__':
    sequences = ['bookI', 'bookII', 'bookIII', 'bus', 'cereal']
    seq_id = 0

    if len(sys.argv) > 1:
        seq_id = int(sys.argv[1])

    if seq_id >= len(sequences):
        print 'Invalid dataset_id: ', seq_id
        sys.exit()

    seq_name = sequences[seq_id]
    print 'seq_id: ', seq_id
    print 'seq_name: ', seq_name


    src_fname = seq_name + '/img%03d.jpg'
    ground_truth_fname = seq_name + '.txt'
    result_fname = seq_name + '_res.txt'

    result_file = open(result_fname, 'w')

    cap = cv2.VideoCapture()
    if not cap.open(src_fname):
        print 'The video file ', src_fname, ' could not be opened'
        sys.exit()

    # thickness of the bounding box lines drawn on the image
    thickness = 2
    # ground truth location drawn in green
    ground_truth_color = (0, 255, 0)
    # tracker location drawn in red
    result_color = (0, 0, 255)

    # read the ground truth
    ground_truth = readTrackingData(ground_truth_fname)
    no_of_frames = ground_truth.shape[0]


    print 'no_of_frames: ', no_of_frames

    ret, init_img = cap.read()
    if not ret:
        print "Initial frame could not be read"
        sys.exit(0)

    # extract the true corners in the first frame and place them into a 2x4 array
    init_corners = [ground_truth[0, 0:2].tolist(),
                    ground_truth[0, 2:4].tolist(),
                    ground_truth[0, 4:6].tolist(),
                    ground_truth[0, 6:8].tolist()]
    init_corners = np.array(init_corners).T
    # write the initial corners to the result file
    writeCorners(result_file, init_corners)

    # initialize tracker with the first frame and the initial corners
    initTracker(init_img, init_corners)

    # window for displaying the tracking result
    window_name = 'Tracking Result'
    cv2.namedWindow(window_name)

    # lists for accumulating the tracking error and fps for all the frames
    tracking_errors = []
    tracking_fps = []

    for frame_id in xrange(1, no_of_frames):
        ret, src_img = cap.read()
        if not ret:
            print "Frame ", i, " could not be read"
            break
        actual_corners = [ground_truth[frame_id, 0:2].tolist(),
                          ground_truth[frame_id, 2:4].tolist(),
                          ground_truth[frame_id, 4:6].tolist(),
                          ground_truth[frame_id, 6:8].tolist()]
        actual_corners = np.array(actual_corners).T

        start_time = time.clock()
        # update the tracker with the current frame
        tracker_corners = updateTracker(src_img)
        end_time = time.clock()

        # write the current tracker location to the result text file
        writeCorners(result_file, tracker_corners)

        # compute the tracking fps
        current_fps = 1.0 / (end_time - start_time)
        tracking_fps.append(current_fps)

        # compute the tracking error
        current_error = math.sqrt(np.sum(np.square(actual_corners - tracker_corners)) / 4)
        tracking_errors.append(current_error)

        # draw the ground truth location
        drawRegion(src_img, actual_corners, ground_truth_color, thickness)
        # draw the tracker location
        drawRegion(src_img, tracker_corners, result_color, thickness)
        # write statistics (error and fps) to the image
        cv2.putText(src_img, "{:5.2f} {:5.2f}".format(current_fps, current_error), (5, 15), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 255, 255))
        # display the image
        cv2.imshow(window_name, src_img)

        if cv2.waitKey(1) == 27:
            break
            # print 'curr_error: ', curr_error

    mean_error = np.mean(tracking_errors)
    mean_fps = np.mean(tracking_fps)

    print 'mean_error: ', mean_error
    print 'mean_fps: ', mean_fps

    result_file.close()
