import numpy as np
import cv2 as cv
import os
import glob
import yaml


x = 8
y = 6

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_COUNT, 10000, 1e-9)

objp = np.zeros((y*x,3), np.float32)
objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

path = "01_data/"
print('image found :',len(os.listdir(path)))

images = glob.glob(path+'*.jpeg')

f = 0

for fname in images:
    print(fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (x,y), None)
    #print(ret,corners)
    print(ret)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (5,5), (-1,-1), criteria)
        imgpoints.append(corners)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (x,y), corners2, ret)
        f+=1
        cv.imshow('board', img)
        cv.waitKey(0)   
print('Number of images used for calliberation:',f)

#caliberation metrics
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

print(ret)
caliberation_data = {'camera matrix':np.asarray(mtx).tolist(), 'dist_coeff':np.asarray(dist).tolist()}
print("intrinsic matrix:\n",mtx)
print("distortion matrix:\n",dist)