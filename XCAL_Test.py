
import numpy as np
from plotf2 import plotf2
import matplotlib.pyplot as plt
from FK_Revyn import FK_Revyn
from AXXBCalibration import AXXBCalibration
from se3Transforms import *



# The below CT values are the camera relative to the checkerboard frame frames from CheckerVidFramePlace.py

CT1=np.array([[ 9.97174277e-01, -6.30141743e-02,  4.08983632e-02, -1.23722844e+02],
 [ 6.88313795e-02,  9.84489411e-01, -1.61377942e-01, -8.71025851e+01],
 [-3.00949078e-02,  1.63737024e-01,  9.86044869e-01,  3.02398776e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT2=np.array([[ 8.25535904e-01, -5.55671460e-01,  9.85885401e-02, -4.59942799e+01],
 [ 5.63435755e-01,  8.21462769e-01, -8.79719784e-02, -1.21960262e+02],
 [-3.21032975e-02,  1.28172335e-01,  9.91232178e-01,  3.10290992e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT3=np.array([[ 4.72250912e-01, -8.79085685e-01,  6.47103912e-02,  7.95749028e+00],
 [ 8.76113636e-01,  4.76194220e-01,  7.52593016e-02, -1.02591514e+02],
 [-9.69740890e-02,  2.11523823e-02,  9.95062110e-01,  2.84591839e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT4=np.array([[-6.16563257e-02, -9.97987575e-01,  1.48087315e-02,  7.60208559e+01],
 [ 9.91803994e-01, -5.95972763e-02,  1.13017707e-01, -7.06530431e+01],
 [-1.11907707e-01,  2.16556156e-02,  9.93482612e-01,  2.95569742e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT5=np.array([[-6.21029481e-02, -9.97888443e-01, -1.90231131e-02,  5.94718471e+01],
 [ 9.94045498e-01, -6.35511671e-02,  8.85143879e-02, -7.62277457e+01],
 [-8.95364257e-02, -1.34128355e-02,  9.95893229e-01,  3.35444221e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT6=np.array([[-5.04442106e-01, -8.63237454e-01, -1.89541657e-02,  1.35528703e+02],
 [ 8.62633542e-01, -5.04798073e-01,  3.22843213e-02, -8.95018096e+01],
 [-3.74370617e-02, -6.49280913e-05,  9.99298985e-01,  3.18446409e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT7=np.array([[-9.91704232e-01,  5.98993528e-03, -1.28401081e-01,  9.9818273e+01],
 [ 6.20622202e-03, -9.95517397e-01, -9.43747619e-02,  0.08745779e+01],
 [-1.28390808e-01, -9.43887363e-02,  9.87221640e-01,  3.83271395e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT8=np.array([[-7.25146092e-01, -6.54101755e-01, -2.15206971e-01,  2.45268966e+01],
 [ 6.65048967e-01, -7.46296963e-01,  2.73991742e-02,  -1.579231906e+01],
 [-1.78530157e-01, -1.23254770e-01,  9.76184022e-01,  3.86559005e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT9=np.array([[ 9.38799693e-01, -2.76315014e-01,  2.05682156e-01, -2.23870881e+01],
 [ 3.02641383e-01,  9.46804032e-01, -1.09408950e-01, -10.66705820e+01],
 [-1.64509360e-01,  1.64961021e-01,  9.72483693e-01,  3.16851793e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT10=np.array([[ 9.81963023e-01,  1.43113001e-01,  1.23560878e-01, -11.88718481e+01],
 [-1.08208919e-01,  9.61281146e-01, -2.53435175e-01, -5.72620256e+01],
 [-1.55046611e-01,  2.35493581e-01,  9.59428643e-01,  2.51374574e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT11=np.array([[-4.95299761e-01, -8.53944290e-01, -1.59553431e-01,  7.98350022e+01],
 [ 8.50000059e-01, -5.14306326e-01,  1.13968870e-01, -5.39110895e+01],
 [-1.79382405e-01, -7.91716717e-02,  9.80588496e-01,  3.32309428e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT12=np.array([[-6.59246870e-01, -7.30974888e-01, -1.76264795e-01,  7.84898885e+01],
 [ 7.42432833e-01, -6.69919038e-01,  1.40397844e-03, -9.02508265e+01],
 [-1.19109415e-01, -1.29939202e-01,  9.84341786e-01,  3.81894381e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )
CT13=np.array([[-6.36029207e-01, -7.61573092e-01, -1.24391609e-01,  10.97429024e+01],
 [ 7.63106401e-01, -6.44690959e-01,  4.51905699e-02, -8.36495458e+01],
 [-1.14610068e-01, -6.61815111e-02,  9.91203581e-01,  3.51516462e+02],
 [ 0.00000000e+00,  0.00000000e+00,  0.00000000e+00,  1.00000000e+00]] )

# The below sets of angles are the angles of the Revyn arm for the above 13 camera frames captrued
A1 = np.array(np.deg2rad([25,-30,122,-19,88,90,0]))
A2 = np.array(np.deg2rad([18,-27,120,-19,82,60,0]))
A3 = np.array(np.deg2rad([15,-30,142,-19,53,40,0]))
A4 = np.array(np.deg2rad([0,2,100,0,58,0,0]))
A5 = np.array(np.deg2rad([0,10,70,0,80,0,0]))
A6 = np.array(np.deg2rad([0,8,78,5,85,-30,0]))
A7 = np.array(np.deg2rad([-15,-20,100,15,75,-90,0]))
A8 = np.array(np.deg2rad([-18,-30,115,15,60,-50,0]))
A9 = np.array(np.deg2rad([-60,-30,130,65,78,70,0]))
A10 = np.array(np.deg2rad([-15,-30,160,30,50,80,0]))
A11 = np.array(np.deg2rad([-25,-30,130,30,65,-40,0]))
A12 = np.array(np.deg2rad([-15,-30,110,10,85,-40,0]))
A13 = np.array(np.deg2rad([-15,-20,105,15,85,-40,0]))

# These ITFC frames are the checkerboard location relative to the camera frame
ITFC1 = np.linalg.inv(CT1) 
ITFC2 = np.linalg.inv(CT2) 
ITFC3 = np.linalg.inv(CT3) 
ITFC4 = np.linalg.inv(CT4) 
ITFC5 = np.linalg.inv(CT5) 
ITFC6 = np.linalg.inv(CT6) 
ITFC7 = np.linalg.inv(CT7) 
ITFC8 = np.linalg.inv(CT8) 
ITFC9 = np.linalg.inv(CT9) 
ITFC10= np.linalg.inv(CT10)
ITFC11= np.linalg.inv(CT11)
ITFC12= np.linalg.inv(CT12)
ITFC13= np.linalg.inv(CT13)


# These TFC frames are the camera location relative to the chckerboard frame simply renamed for clarity
TFC1 = (CT1) 
TFC2 = (CT2) 
TFC3 = (CT3) 
TFC4 = (CT4) 
TFC5 = (CT5) 
TFC6 = (CT6) 
TFC7 = (CT7) 
TFC8 = (CT8) 
TFC9 = (CT9) 
TFC10= (CT10)
TFC11= (CT11)
TFC12= (CT12)
TFC13= (CT13)

# These F frames are the pressumed location of the end effector for the 
F1 = FK_Revyn( A1,7)
F2 = FK_Revyn( A2,7)
F3 = FK_Revyn( A3,7)
F4 = FK_Revyn( A4,7)
F5 = FK_Revyn( A5,7)
F6 = FK_Revyn( A6,7)
F7 = FK_Revyn( A7,7)
F8 = FK_Revyn( A8,7)
F9 = FK_Revyn( A9,7)
F10 = FK_Revyn(A10,7)
F11 = FK_Revyn(A11,7)
F12 = FK_Revyn(A12,7)
F13 = FK_Revyn(A13,7)

# m is the base frame for reference
m = np.eye(4)

# setting figure properties
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.view_init(elev=20., azim=-35, roll=0)
ax.axis("scaled")
ax.set_xlim(-300, 300)
ax.set_ylim(-300, 300)
ax.set_zlim(-100, 500)
ax.set_xlabel('X (mm)')
ax.set_ylabel('Y (mm)')
ax.set_zlabel('Z (mm)')

# Stack F frames and TFC frames for solving AX=XB hand eye calibration problem
Fs= F1
Fs= np.concatenate((Fs,F2))
Fs= np.concatenate((Fs,F3))
Fs= np.concatenate((Fs,F4))
Fs= np.concatenate((Fs,F5))
Fs= np.concatenate((Fs,F6))
Fs= np.concatenate((Fs,F7))
Fs= np.concatenate((Fs,F8))
Fs= np.concatenate((Fs,F9))
Fs= np.concatenate((Fs,F10))
Fs= np.concatenate((Fs,F11))
Fs= np.concatenate((Fs,F12))
Fs= np.concatenate((Fs,F13))

Cs = TFC1
Cs = np.concatenate((Cs,TFC2))
Cs = np.concatenate((Cs,TFC3))
Cs = np.concatenate((Cs,TFC4))
Cs = np.concatenate((Cs,TFC5))
Cs = np.concatenate((Cs,TFC6))
Cs = np.concatenate((Cs,TFC7))
Cs = np.concatenate((Cs,TFC8))
Cs = np.concatenate((Cs,TFC9))
Cs = np.concatenate((Cs,TFC10))
Cs = np.concatenate((Cs,TFC11))
Cs = np.concatenate((Cs,TFC12))
Cs = np.concatenate((Cs,TFC13))

X = AXXBCalibration(Fs,Cs)

# Show the calibration result
print('X:\n ',X,'\n')




# Plot any frame for reference to see how good the calibration is
# Plot the base
plotf2(m, numorlab='Base', ax=ax)

# Calculate the real world postion of the checkerboard relative to the robot base
RealCheck = tranxse3(-512)@tranyse3(15)@tranzse3(460)@rotzse3(np.pi)@rotyse3(np.pi/2.0)
# plot the real world position of the checkerboard relative to the robot base
plotf2(RealCheck, numorlab='C', ax=ax,veccollorx=(255/255.0, 0, 102/255.0),veccollory=(0, 255/255.0, 162/255.0),veccollorz=(0, 195/255.0, 255/255.0))

# Uncomment any below line to see the assumed camera place relative to the location of the checkerboard
# plotf2(RealCheck@ITFC1, numorlab='C1', ax=ax)
# plotf2(RealCheck@ITFC2, numorlab='C2', ax=ax)
# plotf2(RealCheck@ITFC3, numorlab='C3', ax=ax)
# plotf2(RealCheck@ITFC4, numorlab='C4', ax=ax)
# plotf2(RealCheck@ITFC5, numorlab='C5', ax=ax)
# plotf2(RealCheck@ITFC6, numorlab='C6', ax=ax)
# plotf2(RealCheck@ITFC7, numorlab='C7', ax=ax)
# plotf2(RealCheck@ITFC8, numorlab='C8', ax=ax)
# plotf2(RealCheck@ITFC9, numorlab='C9', ax=ax)
# plotf2(RealCheck@ITFC10, numorlab='C10', ax=ax)
# plotf2(RealCheck@ITFC11, numorlab='C11', ax=ax)
# plotf2(RealCheck@ITFC12, numorlab='C12', ax=ax)
# plotf2(RealCheck@ITFC13, numorlab='C13', ax=ax)

# Uncomment any below line to see the assumed location of the EF of the Revyn arm
# plotf2(F1, numorlab='F1', ax=ax)
# plotf2(F2, numorlab='F2', ax=ax)
plotf2(F3, numorlab='F3', ax=ax)
# plotf2(F4, numorlab='F4', ax=ax)
# plotf2(F5, numorlab='F5', ax=ax)
# plotf2(F6, numorlab='F6', ax=ax)
# plotf2(F7, numorlab='F7', ax=ax)
# plotf2(F8, numorlab='F8', ax=ax)
# plotf2(F9, numorlab='F9', ax=ax)
# plotf2(F10, numorlab='F10', ax=ax)
# plotf2(F11, numorlab='F11', ax=ax)
# plotf2(F12, numorlab='F12', ax=ax)
# plotf2(F13, numorlab='F13', ax=ax)

# Uncomment any below line to see the assumed camera place relative to the robot base
# plotf2(F1@X, numorlab='X1', ax=ax)
# plotf2(F1@X@TFC1, numorlab='T1', ax=ax)
# plotf2(F2@X, numorlab='X2', ax=ax)
# plotf2(F2@X@TFC2, numorlab='T2', ax=ax)
plotf2(F3@X, numorlab='X3', ax=ax)
plotf2(F3@X@TFC3, numorlab='T3', ax=ax)
# plotf2(F4@X, numorlab='X4', ax=ax)
# plotf2(F4@X@TFC4, numorlab='T4', ax=ax)
# plotf2(F5@X, numorlab='X5', ax=ax)
# plotf2(F5@X@TFC5, numorlab='T5', ax=ax)
# plotf2(F6@X, numorlab='X6', ax=ax)
# plotf2(F6@X@TFC6, numorlab='T6', ax=ax)
# plotf2(F7@X, numorlab='X7', ax=ax)
# plotf2(F7@X@TFC7, numorlab='T7', ax=ax)
# plotf2(F8@X, numorlab='X8', ax=ax)
# plotf2(F8@X@TFC8, numorlab='T8', ax=ax)
# plotf2(F9@X, numorlab='X9', ax=ax)
# plotf2(F9@X@TFC9, numorlab='T9', ax=ax)
# plotf2(F10@X, numorlab='X10', ax=ax)
# plotf2(F10@X@TFC10, numorlab='T10', ax=ax)
# plotf2(F11@X, numorlab='X11', ax=ax)
# plotf2(F11@X@TFC11, numorlab='T11', ax=ax)
# plotf2(F12@X, numorlab='X12', ax=ax)
# plotf2(F12@X@TFC12, numorlab='T12', ax=ax)

# The below transforms are from the base back to the checkerboard with the AX=XB calculation route
FtCheck1 = F1@X@TFC1
FtCheck2 = F2@X@TFC2
FtCheck3 = F3@X@TFC3
FtCheck4 = F4@X@TFC4
FtCheck5 = F5@X@TFC5
FtCheck6 = F6@X@TFC6
FtCheck7 = F7@X@TFC7
FtCheck8 = F8@X@TFC8
FtCheck9 = F9@X@TFC9
FtCheck10 = F10@X@TFC10
FtCheck11 = F11@X@TFC11
FtCheck12 = F12@X@TFC12

# Error Checking
poserrx = FtCheck1[0,3]
poserrx = np.append(poserrx,FtCheck2[0,3])
poserrx = np.append(poserrx,FtCheck3[0,3])
poserrx = np.append(poserrx,FtCheck4[0,3])
poserrx = np.append(poserrx,FtCheck5[0,3])
poserrx = np.append(poserrx,FtCheck6[0,3])
poserrx = np.append(poserrx,FtCheck7[0,3])
poserrx = np.append(poserrx,FtCheck8[0,3])
poserrx = np.append(poserrx,FtCheck9[0,3])
poserrx = np.append(poserrx,FtCheck10[0,3])
poserrx = np.append(poserrx,FtCheck11[0,3])
poserrx = np.append(poserrx,FtCheck12[0,3])

poserry = FtCheck1[1,3]
poserry = np.append(poserry,FtCheck2[1,3])
poserry = np.append(poserry,FtCheck3[1,3])
poserry = np.append(poserry,FtCheck4[1,3])
poserry = np.append(poserry,FtCheck5[1,3])
poserry = np.append(poserry,FtCheck6[1,3])
poserry = np.append(poserry,FtCheck7[1,3])
poserry = np.append(poserry,FtCheck8[1,3])
poserry = np.append(poserry,FtCheck9[1,3])
poserry = np.append(poserry,FtCheck10[1,3])
poserry = np.append(poserry,FtCheck11[1,3])
poserry = np.append(poserry,FtCheck12[1,3])


poserrz = FtCheck1[2,3]
poserrz = np.append(poserrz,FtCheck2[2,3])
poserrz = np.append(poserrz,FtCheck3[2,3])
poserrz = np.append(poserrz,FtCheck4[2,3])
poserrz = np.append(poserrz,FtCheck5[2,3])
poserrz = np.append(poserrz,FtCheck6[2,3])
poserrz = np.append(poserrz,FtCheck7[2,3])
poserrz = np.append(poserrz,FtCheck8[2,3])
poserrz = np.append(poserrz,FtCheck9[2,3])
poserrz = np.append(poserrz,FtCheck10[2,3])
poserrz = np.append(poserrz,FtCheck11[2,3])
poserrz = np.append(poserrz,FtCheck12[2,3])


exmax = np.max(poserrx)
exmin= np.min(poserrx)

eymax = np.max(poserry)
eymin = np.min(poserry)

ezmax = np.max(poserrz)
ezmin = np.min(poserrz)

exav = np.mean(poserrx)
eyav = np.mean(poserry)
ezav = np.mean(poserrz)

exstd = np.std(poserrx)
eystd = np.std(poserry)
ezstd = np.std(poserrz)

exrng = np.ptp(poserrx)
eyrng = np.ptp(poserry)
ezrng = np.ptp(poserrz)
# all units are in mm
print('X: ', exmax, exmin, '\n', 'Y: ', eymax, eymin, '\n', 'Z: ', ezmax, ezmin)

print('X stats (avg+/-std): ',exav,'+/-',exstd)
print('Y stats (avg+/-std): ',eyav,'+/-',eystd)
print('Z stats (avg+/-std): ',ezav,'+/-',ezstd)
print('X range: ',exrng)
print('Y range: ',eyrng)
print('Z range: ',ezrng)

plt.show()



