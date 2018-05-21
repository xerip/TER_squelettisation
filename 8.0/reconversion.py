import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
from math import pow
from math import sqrt
import sys

def out(image): #convertit le resultat final dans un fichier.
    i=0
    f=open('simpleout.txt','w')
    while i<len(image):
        j=0
        while j<len(image[0]):
            f.write(str(image[i,j]) + " ")
            if j==len(image[1])-1 :
                f.write("\n")
            j=j+1
        i=i+1
    f.close()

def matrice_f(fichier): #retourne une matrice selon le fichier donne, a utiliser pour lire un fichier convertit.
    Nbline = 0
    f=open(fichier,'r')
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


image=matrice_f('squelette.txt')
x=(len(image))
y=(len(image[0]))
res = np.zeros((x,y))
args=sys.argv
print(len(args))
print(args)
if(len(args)>1 and args[1]=='-c'):
	print("Reconversion avec cercle pour les extremites.\n")
else:
	print("Reconversion avec diagonale.\n")

for i in range (1,x):
	for j in range (1,y):
            if(image[i][j]>0):
                p=int(image[i][j])
                for k in range(0,p):
                    for l in range(0,p-k	):
                        res[i-k][j-l]=2
                        res[i-k][j+l]=2
                        res[i+k][j-l]=2
                        res[i+k][j+l]=2
                if(len(args)>1):
                    if(args[1]>0):
                        if ((bool(image[i-1][j]) +bool(image[i+1][j]) + bool(image[i][j-1]) + bool(image[i][j+1]) + bool(image[i+1][j+1]) + bool(image[i+1][j-1]) +bool(image[i-1][j+1]) + bool(image[i-1][j-1]))==1):
                            if image[i][j]>1:				
                                for k in range(0,p):
                                    l=0
                                    while(sqrt((pow(k+int(args[1]),2)+pow(l+int(args[1]),2)))<sqrt(pow(p,2))):					
                                        res[i-k][j-l]=2
                                        res[i-k][j+l]=2
                                        res[i+k][j-l]=2
                                        res[i+k][j+l]=2
                                        l=l+1



if (len(args)>2):
    if (args[2]=='-s'):
        for i in range (1,x):
            for j in range (1,y):
                if image[i][j]>0:
                    res[i][j]=1




plt.imshow(res, cmap=plt.cm.gray)
plt.show()


out(res)
