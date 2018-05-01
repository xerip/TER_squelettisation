from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re

def convert_nb(image):
    i=0
    m = np.zeros((len(image),len(image[0])))
    while i<len(image):
        j=0
        while j<len(image[i]):
            k=0
            while k<len(image[i,j]):
                if len(image[i,j])==3:
                    if image[i,j,k]==0:
                        if k==len((image[i,j]))-1:
                            m[i,j]=0
                        k=k+1
                    else:
                        m[i,j]=1
                        k=len(image[i,j])
                else:
                    if image[i,j,k]==0:
                        if k==len((image[i,j]))-1:
                            m[i,j]=0
                        k=k+1
                    else:
                        if image[i,j,3]>0:
                            m[i,j]=1
                            k=len(image[i,j])
                        else:
                            m[i,j]=0
                            k=len(image[i,j])
            j=j+1
        i=i+1
    return m


image = io.imread("zero.png")
image = convert_nb(image)
plt.imshow(image, cmap=plt.cm.gray)
plt.show()

