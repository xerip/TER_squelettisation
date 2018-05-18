import re
import numpy as np
import matplotlib.pyplot as plt



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


image=matrice_f('simpleout.txt')
x=(len(image))
y=(len(image[0]))
res = np.zeros((x,y))



for i in range (1,x-1):
	for j in range (1,y-1):
		if image[i][j]==1:
			res[i][j]=1
		if image[i][j]==1 and (image[i-1][j] + image[i+1][j] + image[i][j-1] + image[i][j+1] + image[i+1][j+1] + image[i+1][j-1] + image[i-1][j+1] + image[i-1][j-1]==1 or 2):
			if image[i][j-1] or image[i-1][j-1] or image[i+1][j-1]:
				print("hello",i,j)				
				res[i][j-1] = res[i-1][j-1] = res[i+1][j-1]=1
				res[i-1][j] = res[i+1][j] =1
			if image[i][j+1] or image[i+1][j+1] or image[i-1][j+1]:
				print("HELLO",i,j)				
				res[i][j+1] = res[i+1][j+1] = res[i-1][j+1]=1
				res[i-1][j] = res[i+1][j]=1		
			if image[i-1][j-1] or image[i-1][j] or image[i-1][j+1]:
				print("Hello!",i,j)				
				res[i-1][j-1] = res[i-1][j] = res[i-1][j+1]=1
				res[i][j-1]=res[i][j+1]=1			
			if image[i+1][j-1] or image[i+1][j] or image[i+1][j+1]:
				print("Hell",i,j)					
				res[i+1][j-1] = res[i+1][j] = res[i+1][j+1]=1
				res[i][j-1]=res[i][j+1]=1		


out(res)
