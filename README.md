# HandEyeCalibration

These files are used to calibrate a camera and robot to understand its surroundings through computer vision. This project utilizes opencv and python with a webcam attached to the Revyn Arm.
Hand Eye Calibration is an AX=XB problem We solve for X here using a least squares solution after capturing a number of frames where we successfully can measure the transforms of the Revyn Arm Base to the end effector and the camera to the calibration checkerboard frame.
