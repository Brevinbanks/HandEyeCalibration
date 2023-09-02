# Created 9/1/2023 By Brevin Banks
# Modified 9/1/2023 By Brevin Banks
# This function takes and inverts a given homogeneous se3 matrix
# input
#   input_matrix-take in a 4x4 homogeneous transformation matrix 
# output
#   inv_mat - the inverted form of the given se3 matrix
import numpy as np

def Finv(se3_mat):
    inv_mat = np.zeros((4, 4))
    # Establish the R and p values in order to determine the inverse matrix
    R = se3_mat[0:3, 0:3]
    p = se3_mat[0:3, 3]
    # find transpose of R, transpose is equal to inverted 3x3 rotation
    # matrix
    R_t = np.transpose(R)
    p_inv = -R_t@p
    # Place inverted Rotation and position elements in the matrix
    inv_mat[0:3, 0:3] = R_t
    inv_mat[0:3, 3] = p_inv
    inv_mat[3, 3] = 1.0
    return inv_mat