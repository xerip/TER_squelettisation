from numba import autojit
from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re

@autojit
def convert_nb(image):
    i=0
    m = np.zeros((len(image),len(image[0])))
    while i<len(image):
        j=0
        while j<len(image[i]):
            k=0
            if len(image[i,j])==3:
                while k<3:
                    if image[i,j,k]==255:
                        if k==2:
                            m[i,j]=0
                        k=k+1
                    else:
                        m[i,j]=1
                        k=3
            elif len(image[i,j])==4:
                if image[i,j,3]==0:
                    m[i,j]=0
                    k=3
                else:
                    while k<3:
                        if image[i,j,k]==255:
                            if k==2:
                                m[i,j]=0 
                            k=k+1
                        else:
                            m[i,j]=1
                            k=3
            j=j+1
        i=i+1
    return m

@autojit
def out(image):
    i=0
    f=open('convert.txt','w')
    while i<len(image):
        j=0
        while j<len(image[0]):
            f.write(str(int(image[i,j])) + " ")
            if j==len(image[1])-1 :
                f.write("\n")
            j=j+1
        i=i+1
    f.close()

    
image = io.imread("zero.jpg")
image = convert_nb(image)
#plt.imshow(image, cmap=plt.cm.gray)
#plt.show()
out(image)
