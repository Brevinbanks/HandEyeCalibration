# Created 8/29/2023 By Brevin Banks
# Modified 8/29/2023 By Brevin Banks
# This function draws a frame using x,y, and z axis unit vectors at the
# given position in the orientation defined by an se3 rotation matrix
# Input
#   m - a 4x4 se3 matrix
#   numorlab - a string for a label next to the axis names
# Output
#   NONE - check the live figure
import numpy as np
from plotv3 import plotv3
import matplotlib.pyplot as plt

def plotf2(m,numorlab='',ax=None,veccollorx='r',veccollory='g',veccollorz='c'):
        
    numorlab = str(numorlab)

    [rows, cols] = np.shape(m)
    if ((rows != 4) or (cols != 4)):
        raise ValueError("A matrix with shape ("+str(rows)+","+str(cols)+") was given to plotf2. A 4x4 matrix is needed.")
    

    d = np.linalg.det(m[0:3,0:3])
    if (np.abs(d-1)>0.01):
        failstr1 = str(m[0,0])+" "+str(m[0,1])+" "+str(m[0,2])+"\n"
        failstr2 = str(m[1,0])+" "+str(m[1,1])+" "+str(m[1,2])+"\n"
        failstr3 = str(m[2,0])+" "+str(m[2,1])+" "+str(m[2,2])+"\n"
        print("Given Rotation Matrix: ")
        print(failstr1)
        print(failstr2)
        print(failstr3)
        raise ValueError('An improper rotation matrix was given to plotf2')
    

    # isolate the translation matrix
    zer=m[0:3,3]



    # Plot each axis with a 40 length from the origin x in red, y in green, z
    # in cyan
    plotv3(zer,zer+40*m[0:3,0],ax=ax,veccollor=veccollorx,line_width=2)
    plotv3(zer,zer+40*m[0:3,1],ax=ax,veccollor=veccollory,line_width=2)
    plotv3(zer,zer+40*m[0:3,2],ax=ax,veccollor=veccollorz,line_width=2)
    # Draw text next to the axis and a label if given
    ax.text(m[0,3]+m[0,0]*30,m[1,3]+m[1,0]*30,m[2,3]+m[2,0]*30," "+numorlab)
    ax.text(m[0,3]+m[0,1]*30,m[1,3]+m[1,1]*30,m[2,3]+m[2,1]*30," "+numorlab)
    ax.text(m[0,3]+m[0,2]*30,m[1,3]+m[1,2]*30,m[2,3]+m[2,2]*30," "+numorlab)




