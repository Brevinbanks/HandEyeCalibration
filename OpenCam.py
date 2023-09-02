# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This function opens the camera on VideoCapture(n) for computer camera n. The window is shown and a user
# Can press s to save the image in the 'images' folder with filnames 'play_..._pic.png'. Press q to quit
# the script.

import cv2 as cv
import numpy as np
import glob

# Opend the video capture
cap = cv.VideoCapture(0)
# Ensure the video is available
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Define the codec and create VideoWriter object
fourcc = cv.VideoWriter_fourcc(*'XVID')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    cv.imshow('frame', frame)
    if cv.waitKey(1)==ord('s'):
        print('Image Taken ')
        imagesinfolder = glob.glob('images/play_*_pic.png')
        imcount =[]
        iternum = 0
        if len(imagesinfolder)!=0:
            for i in imagesinfolder:
                imagesinfolder[iternum] = imagesinfolder[iternum].replace('images\\play_','')
                imagesinfolder[iternum] = imagesinfolder[iternum].replace('_pic.png','')
                imcount.append(int(imagesinfolder[iternum]))
                iternum = iternum+1
            fname = np.max(imcount)+1
        else:
            fname = 1
        cv.imwrite('images/play_'+str(fname)+'_pic.png', frame)
        
    if cv.waitKey(1) == ord('q'):
        break
# Release everything if job is finished
cap.release()
out.release()
cv.destroyAllWindows()