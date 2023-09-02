# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function draws a vector between two 3x1 vectors in 3D space in a
# live figure
# Input
#   Vec1 - a 3x1 vector from (0,0) the origin to the point you want the
#   drawn vector to start
#   Vec2 - a 3x1 vector from (0,0) the origin to the point you want the
#   drawn vector to end
#   veccollor - a shorthand or color of string
#   line_width - thickness of the desired vector line
#   xlowlim,ylowlim,zlowlim - lower axis figure limits
#   xuplim,yuplim,zuplim - upper axis figure limits
# Output
#   NONE - check the live figure
import numpy as np
import matplotlib.pyplot as plt

def plotv3(Vec1, Vec2, veccollor='k',line_width=1,ax=None,xlowlim=None,xuplim=None,ylowlim=None,yuplim=None,zlowlim =None,zuplim=None):
    
    # Reshape the vectors to make them columns
    Vec1 = np.reshape(Vec1,(3,1))
    Vec2 = np.reshape(Vec2,(3,1))

    # check argument dimension
    [rows, cols] = np.shape(Vec1)
    if ((rows != 3) or (cols != 1)):
        print('Vector Recieved: ', Vec1)
        raise ValueError('plotv3 did not recieve a 3x1 vector for the first vector.')
    

    # check argument dimension
    [rows, cols] = np.shape(Vec2)
    if ((rows != 3) or (cols != 1)):
        print('Vector Recieved: ',Vec2)
        raise ValueError('plotv3 did not recieve a 3x1 vector for the second vector.')


    # Plot a sin curve using the x and y axes.
    x = np.array([Vec1[0],Vec2[0]])
    y = np.array([Vec1[1],Vec2[1]])
    z = np.array([Vec1[2],Vec2[2]])
    ax.plot(x, y, z, zdir='z',color=veccollor,linewidth=line_width)


