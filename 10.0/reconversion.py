import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as pltc
from math import pow
from math import sqrt
import sys

#fichier de reconversion. Moins optimise	 que le programme principal.

def out(image): #convertit le resultat final dans un fichier.
    i=0
    f=open('squelette_reconstruit.txt','w')
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
	f=open(fichier,'r')
	x=f.readline(0)
	firstline=f.readline().split() 
	x,y=firstline[0],firstline[1] 
	m = np.zeros((int(x),int(y)))
	liste=[]
	for line in f: 
		line = re.sub('\n','',line) 
		line=re.split(' ', line) 	
		liste=liste+[line]	
	for l in liste:
		m[int(l[0])][int(l[1])]=int(l[2])
	return(m)









#ouverture du fichier et preparation des variables.
image=matrice_f('squelette.txt')
x=(len(image))
y=(len(image[0]))
res = np.zeros((x,y))
args=sys.argv


#reconvertit l'image
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
                if(len(args)>2):
                	if ((bool(image[i-1][j]) +bool(image[i+1][j]) + bool(image[i][j-1]) + bool(image[i][j+1]) + bool(image[i+1][j+1]) + bool(image[i+1][j-1]) +bool(image[i-1][j+1]) + bool(image[i-1][j-1]))==1):
               	            if image[i][j]>1:				
                                for k in range(0,p):
                                    l=0
                                    while(sqrt((pow(k,2)+pow(l,2)))<sqrt(pow(p,2))-int(args[2])):					
                                        res[i-k][j-l]=2
                                        res[i-k][j+l]=2
                                        res[i+k][j-l]=2
                                        res[i+k][j+l]=2
                                        l=l+1



if (len(args)>1):
    if (args[1]=='-s'):
        for i in range (1,x):
            for j in range (1,y):
                if image[i][j]>0:
                    res[i][j]=1


plt.imshow(res, cmap=plt.cm.gray)
plt.show()

out(res)
