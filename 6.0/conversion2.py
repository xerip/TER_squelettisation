from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re


def convert_nb(image, inversion):
    i=0
    m = np.zeros((len(image),len(image[0])))
    while i<len(image):
        j=0
        while j<len(image[i]):
            k=0
            if (inversion==0):
                try:
                    n=len(image[i,j])
                    if len(image[i,j])==3: #image rgb normal
                        while k<3:
                            if image[i,j,k]==255:
                                if k==2:
                                    m[i,j]=0
                                k=k+1
                            else:
                                m[i,j]=1
                                k=3
                    elif len(image[i,j])==4: # image rgb avec transparence
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
                except TypeError:
                    if image[i,j]==0:
                        m[i,j]=1
                    else:
                        m[i,j]=0
            else:
                try:
                    n=len(image[i,j])
                    if len(image[i,j])==3: #image rgb normal
                        while k<3:
                            if image[i,j,k]==255:
                                if k==2:
                                    m[i,j]=1
                                k=k+1
                            else:
                                m[i,j]=0
                                k=3
                    elif len(image[i,j])==4: # image rgb avec transparence
                        if image[i,j,3]==0:
                            m[i,j]=1
                            k=3
                        else:
                            while k<3:
                                if image[i,j,k]==255:
                                    if k==2:
                                        m[i,j]=1
                                    k=k+1
                                else:
                                    m[i,j]=0
                                    k=3
                except TypeError:
                    if image[i,j]==0:
                        m[i,j]=0
                    else:
                        m[i,j]=1
            j=j+1
        i=i+1
    return m


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

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)

ax = axes.ravel()



image = io.imread("mba.pgm")
#print(len(image[0][0]))

ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)


image = convert_nb(image, 0)
ax[1].imshow(image, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('n&b', fontsize=20)

plt.show()

#out(image)
