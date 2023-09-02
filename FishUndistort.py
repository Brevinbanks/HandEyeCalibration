# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This function uses the calibration K, D, and DIM extrinisic camera paramters
# of a fisheye lens camera to undistort its images
# input
#   img - the distorted image for undistorting, should be the same dimension as the calibration images
#   K - The Camera matrix
#   D - The distortion coefficients
#   DIM - The camera image dimensions   
# output
#   undistored_img - the undistorted version of the input image 
import cv2 as cv
import numpy as np
from FishCal import FishCal

def FishUndistort(img, K=None,D=None,DIM=None):

    if K==None or D==None or DIM==None:
        print('None or not enough camera parameters were given for FishEye Undistortion. Recalibrating all paramerters...')
        K,D,DIM = FishCal()

    # Image undistortion parameter initialization
    balance=1 
    # Image dimension checks for generating new K's. We initialize them here
    dim2=None
    dim3=None

    dim1 = img.shape[:2][::-1]  #grab the dimensions from the given image for undistortion
    assert dim1[0]/dim1[1] == DIM[0]/DIM[1], "Images for undistortion need to be the same dimension as the calibration images"
    if not dim2:
        dim2 = dim1
    if not dim3:
        dim3 = dim1
    scaled_K = K * dim1[0] / DIM[0]  # Scale K to the image dimensions
    scaled_K[2][2] = 1.0  # Final value in camera matrix is 1
    # The K needs to be rescaled if the fisheye lens also causes scaling distortion. The following will generate a new and final K if the image is heavily distorted
    new_K = cv.fisheye.estimateNewCameraMatrixForUndistortRectify(scaled_K, D, dim2, np.eye(3), balance=balance)
    # Build undistortion maps
    map1, map2 = cv.fisheye.initUndistortRectifyMap(scaled_K, D, np.eye(3), new_K, dim3, cv.CV_16SC2)
    # Undistor the image with the maps
    undistorted_img = cv.remap(img, map1, map2, interpolation=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT)

    return undistorted_img

