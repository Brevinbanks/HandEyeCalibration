# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This File contains 3 functions, CheckerMapPlace, CheckerFramePlace, and CheckerVidFramePlace
# They all share similar functionalities and inputs. The outputs are pictures with relative placements of frames or checkerboard maps
# The Map function finds the corners of a checkerboard and plots them.
# The Frame place function finds the corner frame transformation relative to the camera and plots it on an image
# The Video Frame place functions like the Frame place, but does so with live video. The window is shown and a user
# Can press s to save the image in the 'CheckerImages' folder. Press q to quit
# input
#   img - the input cv.imread() file image to place a map or frame on (NOT USED FOR VIDEO)
#   CHECK_HEIGHT - Checkerboard height of number of internal corners (assumed 6)
#   CHECK_WIDTH - Checkerboard width of number of internal corners (assumed 9)
#   squaredim - inconsiquential since the calculation works without it, but for recording purposes you can input the width/height of the checker board square for the checkerboard dimensions
#   K - The Camera matrix if Fisheye camera (NOT USED FOR MAP)
#   D - The distortion coefficients Fisheye camera (NOT USED FOR MAP)
#   DIM - The camera image dimensions (NOT USED FOR MAP)
# output
#   NONE - See the output image of the functions of video
#   Ouputs images with the drawn frame or map in the Checkerimages folder. Frame and Video frame output the resultant frame transform as a numpy array in a #_VidFramed or #_Framed txt file in the same folder

import cv2 as cv
import numpy as np
import glob
from FishCal import FishCal
from FishUndistort import FishUndistort
from cvtransformdraw import *

def CheckerMapPlace(img,CHECK_HEIGHT=6,CHECK_WIDTH = 9,squaredim=20):
    # Assign the Checkerboard pattern
    patternSize = (CHECK_HEIGHT,CHECK_WIDTH)
    # Gray scale the image as the segmentation step
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Estabilish SubPix function checkerboard corners refinement criteria, use default EPS and Iter, then assign minimum 30 tries for refinement error of 0.1
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Create the array of checkerboard object points. A 3x36 set of 3D real world points to define the checkerboard. I assume the squares are 20mm wide in my case
    objp = np.zeros((CHECK_HEIGHT * CHECK_WIDTH, 3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECK_HEIGHT, 0:CHECK_WIDTH].T.reshape(-1,2)*squaredim # multiplty by the square real world dimension to get the right size and width.
    objpoints = [] # initialize real world point array
    imgpoints = [] # initialize 2D checkerboard point array
    # Find the Checkerboard corners
    ret, corners = cv.findChessboardCorners(gray_image, (CHECK_HEIGHT,CHECK_WIDTH), None)
    # If found, add object points, image points (after refining them)
    if ret == True:
        # Add the 3D points to the array of found corner images
        objpoints.append(objp)
        # Refine the corners
        corners2 = cv.cornerSubPix(gray_image,corners, (11,11), (-1,-1), criteria)
        # Add the 2D points to the array of found corner images
        imgpoints.append(corners2)
        # Draw and display the corners on the given image
        cv.drawChessboardCorners(img, (CHECK_HEIGHT,CHECK_WIDTH), corners2, ret)
        # Show the image and allow the user to save or exit
        cv.imshow('Mapped Checkerboard Image', img)
        k = cv.waitKey(0) & 0xFF
        if k == ord('s'):
            # Saving method. Check if files already in the default folder, add to the larges numbered _Mapped.png file
            imagesinfolder = glob.glob('CheckerImages/*_Mapped.png')
            imcount =[]
            iternum = 0
            if len(imagesinfolder)!=0:
                for i in imagesinfolder:
                    imagesinfolder[iternum] = imagesinfolder[iternum].replace('CheckerImages\\','')
                    imagesinfolder[iternum] = imagesinfolder[iternum].replace('_Mapped.png','')
                    imcount.append(int(imagesinfolder[iternum]))
                    iternum = iternum+1
                fname = np.max(imcount)+1
            else:
                fname = 1
            cv.imwrite('CheckerImages/'+str(fname)+'_Mapped.png', img)
    cv.destroyAllWindows()


def CheckerFramePlace(img,CHECK_HEIGHT=6,CHECK_WIDTH=9,squaredim=20, CalNormorFish = False, K=None,D=None,DIM=None):
    # Assign the Checkerboard pattern
    patternSize = (CHECK_HEIGHT,CHECK_WIDTH)
    # Gray scale the image as the segmentation step
    gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Estabilish SubPix function checkerboard corners refinement criteria, use default EPS and Iter, then assign minimum 30 tries for refinement error of 0.1
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Create the array of checkerboard object points. A 3x36 set of 3D real world points to define the checkerboard. I assume the squares are 20mm wide in my case
    objp = np.zeros((CHECK_HEIGHT * CHECK_WIDTH, 3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECK_HEIGHT, 0:CHECK_WIDTH].T.reshape(-1,2)*squaredim # multiplty by the square real world dimension to get the right size and width.
    axis = np.float32([[1,0,0], [0,1,0], [0,0,1]]).reshape(-1,3)*30 # Define the axis direction for frame display
    objpoints = [] # initialize real world point array
    imgpoints = [] # initialize 2D checkerboard point array


    #Obtain camera parameters. If the user sets this to False, then the script will use normal calibration of the camera to determine
    # the camera matrix and distortion coefficients. If true, then the script will assume the camera is fisheye and use the fisheye calibration
    if CalNormorFish==False:
        # Find the Checkerboard corners
        ret, corners = cv.findChessboardCorners(gray_image, (CHECK_HEIGHT,CHECK_WIDTH), None)
        # Add the 3D points to the array of found corner images
        objpoints.append(objp)
        # Refine the results
        corners_refined = cv.cornerSubPix(gray_image,corners,(11,11),(-1,-1),criteria)
        # Add the 2D points to the array of found corner images
        imgpoints.append(corners_refined)
        # Calibrate the camera
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray_image.shape[::-1], None, None)
        DIM = gray_image.shape[::-1]
    else:
        # Check if the user has already given fisheye camera parameters or not. If not solve for them
        if K==None or D==None or DIM==None:
            mtx, dist, DIM = FishCal(CHECK_HEIGHT,CHECK_WIDTH,'images',squaredim)
        else:
            mtx = K
            dist = D


    # Find the Checkerboard corners
    ret, corners = cv.findChessboardCorners(gray_image, (CHECK_HEIGHT,CHECK_WIDTH), None)
    if ret == True:
        # Refine the pixel location of the found corners
        corners_refined = cv.cornerSubPix(gray_image,corners,(11,11),(-1,-1),criteria)
        
        if CalNormorFish==True:
            # For the Fisheye case undistort the corner points
            undistorted = cv.fisheye.undistortPoints(corners_refined, mtx,dist)
            # With the points undistorted, the matrix and distortion coefficients used in the PnP solve will be the identity and zeros since there is no difference between ground truth and the image presumably
            KI = np.eye(3)
            DI=np.zeros((1,5))
            # Find the rotation and translation vectors using the Solve PNP Ransac method. This will converge to one absolute solution omitting outliers
            ret,rvecs, tvecs,inliners = cv.solvePnPRansac(objp, undistorted, KI, DI)
            # Align the checkerboard conrner frame location into a 1D array
            Check_frame_corner = corners_refined[0].ravel()
            # turn the rotational axis angle vector into a 3x3 rotation matrix
            rotm, jac = cv.Rodrigues(rvecs)
            # Find the identity roational axis angle vector from the identity matrix. I = eye(3)
            zrvec,zjac = cv.Rodrigues(np.eye(3))
            # project 3D points of the checkerboard frame to the 2D image plane
            Check_imgpts, jac = cv.fisheye.projectPoints(axis.reshape(-1,1,3),rvecs,tvecs, mtx, dist)
            # project 3D points of the camera frame onto the image plane. Essentially just where the camera calls home. It's not exactly the center of the image.
            centercamcorner, jacc = cv.fisheye.projectPoints(axis.reshape(-1,1,3)*0,rvecs,tvecs*0,mtx,dist)
            centeraxispoints, jacc = cv.fisheye.projectPoints(axis.reshape(-1,1,3),zrvec,tvecs*0,mtx,dist)
            # Draw the checkerboard corner frame relative to the camera
            img = draw_frame(img,Check_frame_corner,Check_imgpts)
            # Draw the camera frame across the image and correct x and y orientations
            centeraxispoints[0,0,0]=-centeraxispoints[0,0,0]
            centeraxispoints[1,0,1]=-centeraxispoints[1,0,1]
            img = draw_frame(img,centercamcorner[0].ravel(),centeraxispoints)
            # Place a center Crosshair
            img = draw_center_cross(img,DIM)
        else:
            # Find the rotation and translation vectors using the Solve PNP Ransac method. This will converge to one absolute solution omitting outliers
            ret,rvecs, tvecs,inliners = cv.solvePnPRansac(objp, corners_refined, mtx, dist)
            # Align the checkerboard conrner frame location into a 1D array
            Check_frame_corner = corners_refined[0].ravel()
            # turn the rotational axis angle vector into a 3x3 rotation matrix
            rotm, jac = cv.Rodrigues(rvecs)
            # Find the identity roational axis angle vector from the identity matrix. I = eye(3)
            zrvec,zjac = cv.Rodrigues(np.eye(3))
            # project 3D points of the checkerboard frame to the 2D image plane
            Check_imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
            # project 3D points of the camera frame onto the image plane. Essentially just where the camera calls home. It's not exactly the center of the image.
            centercamcorner, jacc = cv.projectPoints(axis*0,rvecs,tvecs*0,mtx,dist)
            centeraxispoints, jacc = cv.projectPoints(axis,zrvec,tvecs*0+1,mtx,dist)
            # Draw the checkerboard corner frame relative to the camera
            img = draw_frame(img,Check_frame_corner,Check_imgpts)
            # Draw the camera frame across the image
            img = draw_frame(img,centercamcorner[0].ravel(),centeraxispoints)
            # Place a center Crosshair
            img = draw_center_cross(img,DIM)
            



        # Format the output transformation
        np_rodrigues = np.asarray(rvecs[:,:],np.float64)
        rmat = cv.Rodrigues(np_rodrigues)[0]
        camera_position = -np.matrix(rmat).T @ np.matrix(tvecs)

        Camwrtcord = np.eye(4)
        Camwrtcord[0:3,0:3] = np.matrix(rmat).T
        Camwrtcord[0:3,3] = camera_position[:].ravel()

        


    # Show the image and give the choice to save
    cv.imshow('img', img)
    if ret == True:
        print('Resultant Transform from Camera to Checkerboard: \n', np.linalg.inv(Camwrtcord),'\n\n')
        k = cv.waitKey(0) & 0xFF
        if k==ord('s'):
            print('Image Saved \n\n')
            print("Transform from Checkerboard to Camera(" + str(Camwrtcord.tolist()) + ")")


            # Saving method. Check if files already in the default folder, add to the larges numbered _Mapped.png file
            imagesinfolder = glob.glob('CheckerImages/*_Framed.png')
            imcount =[]
            iternum = 0
            if len(imagesinfolder)!=0:
                for i in imagesinfolder:
                    imagesinfolder[iternum] = imagesinfolder[iternum].replace('CheckerImages\\','')
                    imagesinfolder[iternum] = imagesinfolder[iternum].replace('_Framed.png','')
                    imcount.append(int(imagesinfolder[iternum]))
                    iternum = iternum+1
                fname = np.max(imcount)+1
            else:
                fname = 1

            cv.imwrite('CheckerImages/'+str(fname)+'_Framed.png', img)
            with open('CheckerImages/'+str(fname)+'_Framed.txt', 'w') as f:
                    line = 'np.array('+str(Camwrtcord.tolist())+')'
                    f.write(line)
                    f.write('\n')
    else:
        print('Could not resolve transform. Quitting')

    cv.destroyAllWindows()



def CheckerVidFramePlace(CHECK_HEIGHT=6,CHECK_WIDTH=9,squaredim=20, CalNormorFish = False, K=None,D=None,DIM=None):
    # Assign the Checkerboard pattern
    patternSize = (CHECK_HEIGHT,CHECK_WIDTH)
    # Gray scale the image as the segmentation step
    # Estabilish SubPix function checkerboard corners refinement criteria, use default EPS and Iter, then assign minimum 30 tries for refinement error of 0.1
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # Create the array of checkerboard object points. A 3x36 set of 3D real world points to define the checkerboard. I assume the squares are 20mm wide in my case
    objp = np.zeros((CHECK_HEIGHT * CHECK_WIDTH, 3), np.float32)
    objp[:,:2] = np.mgrid[0:CHECK_HEIGHT, 0:CHECK_WIDTH].T.reshape(-1,2)*squaredim # multiplty by the square real world dimension to get the right size and width.
    axis = np.float32([[1,0,0], [0,1,0], [0,0,1]]).reshape(-1,3)*30 # Define the axis direction for frame display
    objpoints = [] # initialize real world point array
    imgpoints = [] # initialize 2D checkerboard point array

  

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Define the codec and create VideoWriter object
    fourcc = cv.VideoWriter_fourcc(*'XVID')
    needs_cal = True
    out = cv.VideoWriter('video.avi', fourcc, 20.0, (640,  480))
    counter = 1
    while cap.isOpened():
        ret, img = cap.read()
        if not ret:
            print("Can't receive img (stream end?). Exiting ...")
            break
        # Segment the image by gray scaling it
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

        # Only for first iteration
        #Obtain camera parameters. If the user sets this to False, then the script will use normal calibration of the camera to determine
        # the camera matrix and distortion coefficients. If true, then the script will assume the camera is fisheye and use the fisheye calibration
        if needs_cal==True:
            if CalNormorFish==False:
                # Find the Checkerboard corners
                ret, corners = cv.findChessboardCorners(gray_image, (CHECK_HEIGHT,CHECK_WIDTH), None)
                # Add the 3D points to the array of found corner images
                objpoints.append(objp)
                # Refine the results
                corners_refined = cv.cornerSubPix(gray_image,corners,(11,11),(-1,-1),criteria)
                # Add the 2D points to the array of found corner images
                imgpoints.append(corners_refined)
                # Calibrate the camera
                ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray_image.shape[::-1], None, None)
                DIM = gray_image.shape[::-1]
            else:
                # Check if the user has already given fisheye camera parameters or not. If not solve for them
                if K==None or D==None or DIM==None:
                    mtx, dist, DIM = FishCal(CHECK_HEIGHT,CHECK_WIDTH,'images',squaredim)
                else:
                    mtx = K
                    dist = D
            needs_cal=False



        # Find the Checkerboard corners
        ret, corners = cv.findChessboardCorners(gray_image, (CHECK_HEIGHT,CHECK_WIDTH), None)
        if ret == True:
            # Refine the pixel location of the found corners
            corners_refined = cv.cornerSubPix(gray_image,corners,(11,11),(-1,-1),criteria)
            
            if CalNormorFish==True:
                # For the Fisheye case undistort the corner points
                undistorted = cv.fisheye.undistortPoints(corners_refined, mtx,dist)
                # With the points undistorted, the matrix and distortion coefficients used in the PnP solve will be the identity and zeros since there is no difference between ground truth and the image presumably
                KI = np.eye(3)
                DI=np.zeros((1,5))
                # Find the rotation and translation vectors using the Solve PNP Ransac method. This will converge to one absolute solution omitting outliers
                ret,rvecs, tvecs,inliners = cv.solvePnPRansac(objp, undistorted, KI, DI)
                # Align the checkerboard conrner frame location into a 1D array
                Check_frame_corner = corners_refined[0].ravel()
                # turn the rotational axis angle vector into a 3x3 rotation matrix
                rotm, jac = cv.Rodrigues(rvecs)
                # Find the identity roational axis angle vector from the identity matrix. I = eye(3)
                zrvec,zjac = cv.Rodrigues(np.eye(3))
                # project 3D points of the checkerboard frame to the 2D image plane
                Check_imgpts, jac = cv.fisheye.projectPoints(axis.reshape(-1,1,3),rvecs,tvecs, mtx, dist)
                # project 3D points of the camera frame onto the image plane. Essentially just where the camera calls home. It's not exactly the center of the image.
                centercamcorner, jacc = cv.fisheye.projectPoints(axis.reshape(-1,1,3)*0,rvecs,tvecs*0,mtx,dist)
                centeraxispoints, jacc = cv.fisheye.projectPoints(axis.reshape(-1,1,3),zrvec,tvecs*0,mtx,dist)
                # Draw the checkerboard corner frame relative to the camera
                img = draw_frame(img,Check_frame_corner,Check_imgpts)
                # Draw the camera frame across the image and correct x and y orientations
                centeraxispoints[0,0,0]=-centeraxispoints[0,0,0]
                centeraxispoints[1,0,1]=-centeraxispoints[1,0,1]
                img = draw_frame(img,centercamcorner[0].ravel(),centeraxispoints)
                # Place a center Crosshair
                img = draw_center_cross(img,DIM)
            else:
                # Find the rotation and translation vectors using the Solve PNP Ransac method. This will converge to one absolute solution omitting outliers
                ret,rvecs, tvecs,inliners = cv.solvePnPRansac(objp, corners_refined, mtx, dist)
                # Align the checkerboard conrner frame location into a 1D array
                Check_frame_corner = corners_refined[0].ravel()
                # turn the rotational axis angle vector into a 3x3 rotation matrix
                rotm, jac = cv.Rodrigues(rvecs)
                # Find the identity roational axis angle vector from the identity matrix. I = eye(3)
                zrvec,zjac = cv.Rodrigues(np.eye(3))
                # project 3D points of the checkerboard frame to the 2D image plane
                Check_imgpts, jac = cv.projectPoints(axis, rvecs, tvecs, mtx, dist)
                # project 3D points of the camera frame onto the image plane. Essentially just where the camera calls home. It's not exactly the center of the image.
                centercamcorner, jacc = cv.projectPoints(axis*0,rvecs,tvecs*0,mtx,dist)
                centeraxispoints, jacc = cv.projectPoints(axis,zrvec,tvecs*0+1,mtx,dist)
                # Draw the checkerboard corner frame relative to the camera
                img = draw_frame(img,Check_frame_corner,Check_imgpts)
                # Draw the camera frame across the image
                img = draw_frame(img,centercamcorner[0].ravel(),centeraxispoints)
                # Place a center Crosshair
                img = draw_center_cross(img,DIM)
                



            # Format the output transformation
            np_rodrigues = np.asarray(rvecs[:,:],np.float64)
            rmat = cv.Rodrigues(np_rodrigues)[0]
            camera_position = -np.matrix(rmat).T @ np.matrix(tvecs)

            Camwrtcord = np.eye(4)
            Camwrtcord[0:3,0:3] = np.matrix(rmat).T
            Camwrtcord[0:3,3] = camera_position[:].ravel()

        


        # Show the image and give the choice to save
        cv.imshow('img', img)
        if ret == True:
            if cv.waitKey(1)==ord('s'):
                print('Image Saved \n\n')
                print("Transform from Checkerboard to Camera(" + str(Camwrtcord.tolist()) + ")")


                # Saving method. Check if files already in the default folder, add to the larges numbered _Mapped.png file
                imagesinfolder = glob.glob('CheckerImages/*_VidFramed.png')
                imcount =[]
                iternum = 0
                if len(imagesinfolder)!=0:
                    for i in imagesinfolder:
                        imagesinfolder[iternum] = imagesinfolder[iternum].replace('CheckerImages\\','')
                        imagesinfolder[iternum] = imagesinfolder[iternum].replace('_VidFramed.png','')
                        imcount.append(int(imagesinfolder[iternum]))
                        iternum = iternum+1
                    fname = np.max(imcount)+1
                else:
                    fname = 1

                cv.imwrite('CheckerImages/'+str(fname)+'_VidFramed.png', img)
                with open('CheckerImages/'+str(fname)+'_VidFramed.txt', 'w') as f:
                        line = 'np.array('+str(Camwrtcord.tolist())+')'
                        f.write(line)
                        f.write('\n')

        if cv.waitKey(1) == ord('q'):
            break
    # Release everything if job is finished
    cap.release()
    out.release()
    cv.destroyAllWindows()





# Example use cases
# CheckerMapPlace(cv.imread("images/cal_1_pic.png", cv.IMREAD_COLOR), CHECK_HEIGHT=6,CHECK_WIDTH=9,squaredim=20)
# CheckerFramePlace(cv.imread("images/cal_1_pic.png", cv.IMREAD_COLOR),CHECK_HEIGHT=6,CHECK_WIDTH=9,squaredim=20, CalNormorFish = True, K=None,D=None,DIM=None)
# CheckerVidFramePlace(CHECK_HEIGHT=6,CHECK_WIDTH=9,squaredim=20, CalNormorFish = True, K=None,D=None,DIM=None)

















