import re
import numpy as np
import matplotlib.pyplot as plt

def matrice_f(fichier): #retourne une matrice selon le fichier donne
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

def matrice_min_int(m, n): #la matrice devient une matrice de 1 et de 0 selon un entier minimum
    i=0
    while i<len(m):
        j=0
        while j<len(m[i]):
            if m[i][j]>=n:
                m[i][j]=0
            else:
                m[i][j]=1
            j=j+1
        i=i+1
    return m
        
m=matrice_f('simpleout.txt')
m=matrice_min_int(m, 1)

plt.imshow(m, cmap=plt.cm.gray)
plt.show()





