# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# These draw functions are for opencv imshow images read by cv.imread()
# The draw frame draws a homogeneous transformation matrix a the given corner with axis points
# The center cross function draws a crosshair in the center of the camera view
# input
#   img - the input cv.imread() file image to place the drawn functions on
#   corner - a  non-tuple preferably int 2x1 array for 2D positioning on the image window
#   axpoints - a non-tuple preferably in 2x3 array for 2D positioning axis on the image window 
#   DIM - The camera image dimensions
# output
#   img - updated cv.imread image pointer with drawings on top. use cv.imshow('img',img) to see the image
import cv2 as cv

def draw_frame(img, corner, axpoints):
    # Check if the imput values are ints for pixel placement
    if isinstance(corner,int)==False:
        corner = corner.astype(int)
    if isinstance(axpoints,int)==False:
        axpoints = axpoints.astype(int)
    #Draw the Axis
    img = cv.line(img, tuple(corner), tuple(axpoints[0].ravel()), (0,0,255), 2) # X
    img = cv.line(img, tuple(corner), tuple(axpoints[1].ravel()), (0,255,0), 2) # Y 
    img = cv.line(img, tuple(corner), tuple(axpoints[2].ravel()), (255,0,0), 2) # Z
    return img

def draw_center_cross(img,DIM=[320,240]):
    X = int(DIM[0]/2.0)
    Y = int(DIM[1]/2.0)
    img = cv.line(img, (X,Y-11), ((X,Y+11)), (0,0,0), 2) # Center
    img = cv.line(img, (X-11,Y), ((X+11,Y)), (0,0,0), 2) # Center
    img = cv.line(img, (X,Y-10), ((X,Y+10)), (150,255,0), 1) # Center
    img = cv.line(img, (X-10,Y), ((X+10,Y)), (150,255,0), 1) # Center
    return img