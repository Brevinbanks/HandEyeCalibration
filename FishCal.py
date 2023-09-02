# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This function calibrates a set of images in a folder given for images taken
# with a fisheye lens camera and returns extrinisc camera properties to undistort
# the image content
# input
#   CHECK_HEIGHT - Checkerboard height of number of internal corners (assumed 6)
#   CHECK_WIDTH - Checkerboard width of number of internal corners (assumed 9)
#   foldername - folder where the images are stored within the same workspace as this python file. (assumed 'images')
#   checksquarewidth - inconsiquential since the calculation works without it, but for recording purposes you can input the width/height of the checker board square for the checkerboard dimensions
# output
#   K - The Camera matrix
#   D - The distortion coefficients
#   DIM - The camera image dimensions
import cv2
print('\nFisheye Lens Calibration. Using cv2 version: ', cv2.__version__,'\n\n')
assert int(cv2.__version__[0]) >= 3, 'The fisheye module requires opencv version >= 3.0.0'
import glob
import numpy as np

def FishCal(CHECK_HEIGHT = 6, CHECK_WIDTH = 9,foldername='images',checksquarewidth=20.0):
    # Define Checkerboard dimensions
    CHECKERBOARD = (CHECK_HEIGHT,CHECK_WIDTH)
    # Estabilish SubPix function checkerboard corners refinement criteria, use default EPS and Iter, then assign minimum 30 tries for refinement error of 0.1
    criteria = (cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
    # Define fishey calibration flags for computing extrinsic camera properties
    calibration_flags = cv2.fisheye.CALIB_RECOMPUTE_EXTRINSIC+cv2.fisheye.CALIB_CHECK_COND+cv2.fisheye.CALIB_FIX_SKEW
    # Create the array of checkerboard object points. A 3x36 set of 3D real world points to define the checkerboard. I assume the squares are 20mm wide in my case
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)*checksquarewidth # multiplty by 20mm to get the right size and width. (if not included it shouldn't really affect the calibration)
    Dim_of_image = 0 # initialize the image dimension
    objpoints = [] # initialize real world point array
    imgpoints = [] # initialize 2D checkerboard point array
    images = glob.glob(foldername+'/*.png') # there should be a folder with only calibration images called images. All images in there should be png format and feature a clear image of a checkerboard or in differently named folder given to the function
    counter = 0 # Used to count loop iterations for debugging
    for frame in images:
        img = cv2.imread(frame) # Read in the image frame
        # Ensure the image is the same shape as other images, if this is the first image initialize the assumed shape of all images by referencing this first one
        if Dim_of_image == 0:
            Dim_of_image = img.shape[:2] # grab the image shape
        else:
            assert Dim_of_image == img.shape[:2], "\nThe calibration images need to be the same dimension.\n"    
        
        # Image segmentation is performed here by turning the image gray
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the corners of the checkerboard in the calibration image
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)
        # If the corners are found then add the assumed 3D points to the array of object points, refine the pixel result in the found 2D points, and then add the 2D points the image points array
        if ret == True:
            objpoints.append(objp)
            cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),criteria)
            imgpoints.append(corners)
            Num_of_cal_img = len(objpoints)
        # If there is a failure, print the failure on number frame
        else: 
            print('Failure processing image number: ',counter,' for image named: ',images[counter],'\n')
        counter = counter+1
    # Solve the K and D camera extrinsic properties
    K = np.zeros((3, 3))
    D = np.zeros((4, 1))
    rvecs = [np.zeros((1, 1, 3), dtype=np.float64) for k in range(Num_of_cal_img)]
    tvecs = [np.zeros((1, 1, 3), dtype=np.float64) for k in range(Num_of_cal_img)]
    rms, _, _, _, _ = cv2.fisheye.calibrate(objpoints,imgpoints,gray.shape[::-1],K,D,rvecs,tvecs,calibration_flags,(cv2.TERM_CRITERIA_EPS+cv2.TERM_CRITERIA_MAX_ITER, 30, 1e-6))
    # print the results of the calibration
    print("There were " + str(Num_of_cal_img) + " images used for fisheye calibration")
    print('Calibration Results: DIM(Dimension of images) K(Camera Matrix)  D(Distortion Coefficients)')
    print("DIM=" + str(Dim_of_image[::-1]))
    print("K=np.array(" + str(K.tolist()) + ")")
    print("D=np.array(" + str(D.tolist()) + ")")

    return K, D, Dim_of_image[::-1]
