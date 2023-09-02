import numpy as np


# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 rotation matrix about x given an angle phi
# Input
#   phi - angle in radians of desired rotation
# Output
#   Tf - a 4x4 se3 matrix of a rotation about the x axis

def rotxse3(phi):

    Tf = np.array([[1.0, 0, 0, 0],
                   [0, np.cos(phi), -np.sin(phi), 0],
                   [0, np.sin(phi), np.cos(phi),  0],
                   [0, 0, 0, 1]])
    
    return Tf


# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 rotation matrix about y given an angle theta
# Input
#   theta - angle in radians of desired rotation
# Output
#   Tf - a 4x4 se3 matrix of a rotation about the y axis

def rotyse3(theta):

    Tf = np.array([[np.cos(theta), 0, np.sin(theta), 0],
                   [0, 1.0, 0, 0],
                   [-np.sin(theta), 0, np.cos(theta), 0],
                   [0, 0, 0, 1]])
    
    return Tf


# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 rotation matrix about z given an angle psi
# Input
#   psi - angle in radians of desired rotation
# Output
#   Tf - a 4x4 se3 matrix of a rotation about the z axis

def rotzse3(psi):

    Tf = np.array([[np.cos(psi), -np.sin(psi), 0, 0], 
                   [np.sin(psi), np.cos(psi), 0, 0],
                   [0, 0, 1.0, 0],
                   [0, 0, 0, 1]])
    
    return Tf

# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 translation transformation matrix 
# along x given a distance alpha
# Input
#   alpha - desired distance to translate in x
# Output
#   Tf - a 4x4 se3 matrix of a translation

def tranxse3(alpha):

    Tf = np.array([[1, 0, 0, alpha],
                   [ 0, 1, 0, 0],
                   [0, 0, 1,  0],
                   [0, 0, 0, 1]])
    
    return Tf


# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 translation transformation matrix 
# along y given a distance alpha
# Input
#   alpha - desired distance to translate in y
# Output
#   Tf - a 4x4 se3 matrix of a translation

def tranyse3(beta):

    Tf = np.array([[1, 0, 0, 0],
                   [ 0, 1, 0, beta],
                   [0, 0, 1,  0],
                   [0, 0, 0, 1]])
    
    return Tf


# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 translation transformation matrix 
# along z given a distance alpha
# Input
#   alpha - desired distance to translate in z
# Output
#   Tf - a 4x4 se3 matrix of a translation

def tranzse3(gamma):

    Tf = np.array([[1, 0, 0, 0],
                   [ 0, 1, 0, 0],
                   [0, 0, 1,  gamma],
                   [0, 0, 0, 1]])
    
    return Tf

# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function calculates a 4x4 se3 homogenous transformation matrix
# given a 3x3 Rotation matrix and 3x1 translation vector
# Input
#   R - 3x3 Rotation matrix
#   T - 3x1 translation vector
# Output
#   F - a 4x4 se3 matrix 
def frame_maker(R,T):
    F = np.eye(4)
    F[0:3,0:3] = R
    F[0:3,3] = T
    return F