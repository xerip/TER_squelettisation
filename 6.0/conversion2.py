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

def nofloat_f(fichier): #retourne une matrice selon le fichier donne, a utiliser pour lire un fichier convertit.
    Nbline = 0
    f=open(fichier,'r+')
    for line in f:
        Nbline += 1
    Nbcol = len(re.split(' ', line))-1
    print ("Nombre de lignes : "+str(Nbline))
    print ("Nombre de colonnes : "+str(Nbcol))
    m = np.zeros((Nbline,Nbcol))
    f.seek(0)
    i=0
    for line in f:
        j=0
        line = re.split(' ', line)      #on liste chaque ligne par rapport au separateur ' '
        while j<len(line)-1:
            m[i][j]=line[j]
            j=j+1
        i=i+1
    f.close()
    return m
    
image = io.imread("mbapaint.png")
image = convert_nb(image)
#plt.imshow(image, cmap=plt.cm.gray)
#plt.show()
out(image)
