# HandEyeCalibration

These files are used to calibrate a camera and robot to understand its surroundings through computer vision. This project utilizes opencv and python with a webcam attached to the Revyn Arm.
Hand Eye Calibration is an AX=XB problem We solve for X here using a least squares solution after capturing a number of frames where we successfully can measure the transforms of the Revyn Arm Base to the end effector and the camera to the calibration checkerboard frame.

CheckerImages - Folder of output images from any of the of functions in CheckerFramePlace.py
images - Folder for input calibration images for the fisheye lens of the webcam
other - Folder for other unused images

# AXXBCalibration.py
This file solves the AX=XB problem given 2 sets of 4*Nx4 stacked homogeneous transformations that coincide with the robot end effector relative to the base and the camera relative to the calibration checkerboard. N>3
It returns X, a homogeneous transform that defines the transformation between the end effector and the camera

# CheckerFramePlace.py
A set of 3 functions, Map, Frame, and Video frame, that take input images with a clearly visible checkerboard and either maps the inner corners of the checkerboard, places a frame on the checkerboard, or places a frame on a checkerboard captured in a live image respectivley.

# FK_Revyn.py
A python translation of the forward kinematics FK_Revyn.m file from the Revyn arm control project. See https://github.com/Brevinbanks/RevynArm

# Finv.py
A function that takes the inverse of an SE3 transformation matrix

# FishCal.py
Given calibration images in the 'images' folder or other user defined folder, the function will calibrate the camera extrinsic properties for a fisheye lens camera where a checkerboard is clearly visible in the given calibration images

# FishUndistort.py
Generates an undistorted image for the given fisheye distorted image using the calibration from FishCal.py

# OpenCam.py
Opens a live video stream from the select camera in cv.VideoCapture and allows the user to save images that could be used for calibration.

# XCAL_Test.py
A script that contains the execution of the Hand Eye Calibration for the Revyn Arm. The Revyn Arm was moved to 13 locations with a camera at the end effector and the resultant frame for the camera was captured using the CheckerFramePlace.py Frame function. The location of the end effector was calculated using FK_Revyn.py given the joint angles used to achieve the respective 13 locations. The results are plotted and the X transform is printed along with some error statistics

# cvtransformdraw.py
Draws different items on a given cv.imread() pointer image. When displayed with cv.imshow() the objects are drawn on the image. There is the option to draw a homogenous frame transform relative to the camera, or draw a crosshair in the center of the camera image.

# plotf2.py and plotv3.py 
A python translation of the frame and vector plotting .m files from the Revyn arm control project. See https://github.com/Brevinbanks/RevynArm

# se3Transforms.py
A python translation of the se3 transforms (translation and rotation) .m fucntions from the Revyn arm control project. See https://github.com/Brevinbanks/RevynArm





