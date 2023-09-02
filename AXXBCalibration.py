# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This function calculates the frame between the end effector and camera for N>3 
# camera to checkerboard and base to end effector frame pairs and uses the FindRx and FindTx methods
# to isolate the homogenous rotation and translation respectivley for calibration of the AX=XB problem
# Input
#   Base2EF - N*4x4 stacked homogeneous frame transforms from the base to end effector
#   Cam2Check - N*4x4 stacked homogeneous frame transforms from the camera to the calibration board/checkerboard
# Output
#   X - a 4x4 se3 matrix from the End Effector frame to the Camera frame
# *INCLUDES SUB FUNCTION unskewlogR
#       Takes the matrix log of a 3x3 rotation matrix and then unskews the result
#       Input
#           R - 3x3 rotation matrix
#       Output
#           alphabeta - 3x1 rotation vector result of an unskewed matrix log from a rotation matrix (axis angle notation)
import matplotlib.pyplot as plt
import numpy as np
import scipy as sc
from scipy import linalg
from Finv import Finv

def unskewlogR(R):
    # Find the matrix log of the rotation matrix
    omega = sc.linalg.logm(R)
    # Unskew the result into rotational axis angle
    alphabeta = np.array([[omega[2, 1]], [omega[0, 2]], [omega[1, 0]]])
    return alphabeta

def AXXBCalibration(Base2EF, Cam2Check):
    # Ensure the given matrix stacks are 3 Dimensional
    Base2EF = np.expand_dims(Base2EF, axis=0)
    Cam2Check = np.expand_dims(Cam2Check, axis=0)

    # grab the dimension of the matrix stacks
    [N, j, g] = np.shape(Base2EF)

     # Initialize empty arrays to slove AXXB problem
     # Approach uses E1^-1@E2@X =X@S1@S2^-1 where E1 and E2 are built of end effector to base transforms
     # S1 and S2 are buitl from camera to calibration frame transforms.
     # A = E1^-1@E2
     # B = @S1@S2^-1
    E = np.empty((1, 4, 4))
    S = np.empty((1, 4, 4))
    m = int(j/4) # grab every 4 sets of rows
    for k in range(m):
        # Ensure the given matrix stacks are 3 Dimensional
        Base2EF3d = np.expand_dims(
            Base2EF[0, (k)*4:(k)*4+4, :], axis=0)

        Cam2Check3d = np.expand_dims(
            Cam2Check[0, (k)*4:(k)*4+4, :], axis=0)
        if k == 0:
            E = Base2EF3d
            S = Cam2Check3d
        else:
            E = np.append(E, Base2EF3d, axis=0)
            S = np.append(S, Cam2Check3d, axis=0)

    # Initialize empty arrays to slove AXXB problem create A and B
    A = np.empty((1, 4, 4))
    B = np.empty((1, 4, 4))

    # Create the A's and B's
    for k in range(m-1):
        AIn = Finv(E[k, :, :])@E[k+1, :, :]
        BIn = S[k, :, :]@Finv(S[k+1, :, :])

        # Ensure the given matrix stacks are 3 Dimensional
        A3d = np.expand_dims(AIn, axis=0)
        B3d = np.expand_dims(BIn, axis=0)
        if k == 0:
            A = A3d
            B = B3d
        else:
            A = np.append(A, A3d, axis=0)
            B = np.append(B, B3d, axis=0)

    # Identify the axis of rotations
    [i, j, n] = np.shape(A)
    # Create alpha and beta, respective axis angle notation for axis of rotation for A and B
    alphas = np.zeros((3, i))
    betas = np.zeros((3, i))
    for k in range(i):
        alphas[0:3, k] = np.reshape(unskewlogR(A[k, 0:3, 0:3]), (3,))
        betas[0:3, k] = np.reshape(unskewlogR(B[k, 0:3, 0:3]), (3,))

    # Solve for the rotation matrix Rx, then using the result solve for the translation Tx
    Rx = FindRx(alphas, betas)
    Tx = FindTx(A[:, 0:3, 0:3], A[:, 0:3, 3], B[:, 0:3, 3], Rx)

    # Assign values to output homogenous transformation matrix X
    X = np.eye(4)
    X[0:3, 0:3] = Rx
    X[0, 3] = Tx[0]
    X[1, 3] = Tx[1]
    X[2, 3] = Tx[2]

    return X

# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# Finds the 3x3 rotation matrix of a AX=XB problem where
# Rx is the result of axis angle vectors alpha and beta,
# stacked, summed as the outer product of two vectors, and then
# the inverse square root of the transposed sum multiplied by the sum and then
# the result of such right multiplied by the transpose of the sum again.
# Input
#   alphas - axis angle axis for A vectors 3xN vectors
#   betas - axis angle axis for B vectors 3xN vectors
#  Output
#   Rx - the 3x3 homogenous rotation matrix solution to AX=XB
def FindRx(alphas, betas):
    M = np.zeros((3, 3))
    n, m = np.shape(alphas)

    for k in range(m):
        M = M + (np.outer(betas[:, k], alphas[:, k]))

    Rx = np.linalg.inv(sc.linalg.sqrtm(np.transpose(M)@M))@np.transpose(M)

    return Rx

# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# Finds the 3x1 translation vector of a AX=XB problem where
# Tx is the result of solving the least squares equation
# RATx + TA = RXTB+Tx
# Input
#   RA - 3x3xN rotation matrices of A
#   tA - 3xN translation vectors of A
#   RX - 3x3 rotation matrix from FindRx
#   tB - 3xN translation vectors of B
#  Output
#   tx - the 3x1 homogenous translation vector solution to AX=XB
def FindTx(RA, tA, tB, RX):

    I = np.eye(3)

    [n, j, m] = np.shape(RA)
    Left = np.zeros((3*n, 3))
    Right = np.zeros((3*n, 1))
    print('RA shape', np.shape(RA))
    for k in range(n):
        if k == 0:

            Left[0:3, 0:3] = I - RA[k, :, :]
            Right[0:3, 0] = tA[k, :] - RX@tB[k, :]

        else:

            Left[3*k:3*k+3, 0:3] = I - RA[k, :, :]
            Right[3*k:3*k+3, 0] = tA[k, :] - RX@tB[k, :]
  
    print('Left: ',Left)
    print('Right: ',Right)
    
    tx = np.linalg.pinv(Left)@Right
    
    return tx
