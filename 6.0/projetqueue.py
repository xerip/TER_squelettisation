from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import deque
from numba import jit


#X/I=LIGNES  = 328
#Y/J=COLONNES = 400
#print(i+1,j*3+3)

#Ce programme utilise le fichier "cheval.nb"
#Pour utiliser une forme coloree sur fond blanc, utiliser le fichier conversion.py et decommentariser la ligne
#image = matrice_f("convert.txt") plus bas

#Evidemment tout est loin d'etre optimise.
#Utilisez le fichier "plot_min.py" pour afficher le resultat.

@jit
def out(image): #convertit le resultat final dans un fichier.
    i=0
    f=open('simpleout.txt','w')
    while i<len(image):
        j=0
        while j<len(image[0]):
            f.write(str(image[i,j]).zfill(2) + " ")
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

@jit
def simplification(i,j,d,pic):  #determine si un point est simple ou terminal.
	if (d=='N'):
		p=pic[i][j-1] + pic[i][j+1] + pic[i+1][j]
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i+1][j-1]+pic[i+1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (pic[i+1][j] == 0):
				return 0
			elif ((pic[i][j-1] and pic[i+1][j-1]) or (pic[i+1][j+1] and pic[i][j+1])):
				return 1
			else:
				return 0
	if (d=='E'):
		p=pic[i][j-1] + pic[i-1][j] + pic[i+1][j]
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j-1]+pic[i+1][j-1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (pic[i][j-1] == 0):
				return 0
			elif ((pic[i-1][j-1] and pic[i-1][j]) or (pic[i+1][j-1] and pic[i+1][j])):
				return 1
			else:
				return 0
	if (d=='S'):
		p=pic[i-1][j] + pic[i][j+1] + pic[i][j-1]
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j-1]+pic[i-1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (pic[i-1][j] == 0):
				return 0
			elif ((pic[i-1][j-1] and pic[i][j-1]) or (pic[i-1][j+1] and pic[i][j+1])):
				return 1
			else:
				return 0
	if (d=='O'):
		p=pic[i-1][j] + pic[i+1][j] + pic[i][j+1]
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j+1]+pic[i+1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (pic[i][j+1] == 0):
				return 0
			elif ((pic[i+1][j+1] and pic[i+1][j]) or (pic[i-1][j+1] and pic[i-1][j])):
				return 1
			else:
				return 0




image = io.imread("chevalnb.png")
image = image.astype(int)
image = matrice_f("convert.txt")
x=(len(image))
y=(len(image[0]))
print("Dimensions:",x,y)
#definitions des table utilisees pour la priorites.
prio= np.zeros((x,y),dtype=int)
priohg=np.zeros((x,y),dtype=int)
priobg=np.zeros((x,y),dtype=int)
priohd=np.zeros((x,y),dtype=int)
priobd=np.zeros((x,y),dtype=int)
simple=[]

front=deque()
#Calcul de profondeur par chaque extremite.
@jit
def prior():
    for i in range (1,x-1):
        for j in range (1,y-1):
            #bas droite
            if (image[i][j]==1 and (priobd[i-1][j]==0 or priobd[i][j-1]==0)):
                priobd[i][j]=1
            elif (image[i][j]==1 and (priobd[i-1][j]>0 and priobd[i][j-1]>0)):
                priobd[i][j]=min(priobd[i-1][j],priobd[i][j-1])+1
            #haut droite
            if (image[x-i][j]==1 and (priohd[x-i+1][j]==0 or priohd[x-i][j-1]==0)):
                priohd[x-i][j]=1
            elif (image[x-i][j]==1 and (priohd[x-i+1][j]>0 and priohd[x-i][j-1]>0)):
                priohd[x-i][j]=min(priohd[x-i+1][j],priohd[x-i][j-1])+1
            #bas gauche
            if (image[i][y-j]==1 and (priobg[i-1][y-j]==0 or priobg[i][y-j+1]==0)):
                priobg[i][y-j]=1
            elif (image[i][y-j]==1 and (priobg[i-1][y-j]>0 and priobg[i][y-j+1]>0)):
                priobg[i][y-j]=min(priobg[i-1][y-j],priobg[i][y-j+1])+1
            #haut gauche
            if (image[x-i][y-j]==1 and (priohg[x-i+1][y-j]==0 or priohg[x-i][y-j+1]==0)):
                priohg[x-i][y-j]=1
            elif (image[x-i][y-j]==1 and (priohg[x-i+1][y-j]>0 and priohg[x-i][y-j+1]>0)):
                priohg[x-i][y-j]=min(priohg[x-i+1][y-j],priohg[x-i][y-j+1])+1

    for i in range (0,x):
        for j in range (0,y):
            prio[i][j]=min(priohg[i][j],priobg[i][j],priohd[i][j],priobd[i][j])

    priomax=prio.max()
    #print(priomax)
    megaliste=[]
    frontN=[]
    frontE=[]
    frontS=[]
    frontO=[]
    front=[]
    listecompteur=np.zeros(priomax+1,dtype=int)
    #squelettisation, par priorite.
    #Par ordre N E S O, determine les forntiere puis les supprime en fin de passe.

    for i in range(1,x-1):
        for j in range (1,y-1):
            if(prio[i][j]>0):
                listecompteur[prio[i][j]]=listecompteur[prio[i][j]]+1
                pos=0
                for g in range(1,prio[i][j]):
                    pos=pos+listecompteur[g]
                megaliste.insert(pos,(i,j))
        
    megaliste.reverse()
    #print(len(megaliste))
    for pr in range (1,priomax):
        for g in range(0,listecompteur[pr]-1):
            p=megaliste.pop()
            if image[p[0]-1][p[1]]==0:
                    frontN.extend((p[0],p[1]))
            if image[p[0]][p[1]+1]==0:
                    frontE.extend((p[0],p[1]))
            if image[p[0]+1][p[1]]==0:
                    frontS.extend((p[0],p[1]))
            if image[p[0]][p[1]-1]==0:
                    frontO.extend((p[0],p[1]))
        frontN.reverse()
        frontE.reverse()
        frontS.reverse()
        frontO.reverse()
        for g in range(0,len(frontN)/2):
            p=frontN.pop()
            q=frontN.pop()
            if image[p][q]==1:
                if simplification(p,q,"N",image):
                    front.extend((p,q))
        front.reverse()
        for g in range(0,len(front)/2):
            image[front.pop()][front.pop()]=0
        for g in range(0,len(frontE)/2):
            p=frontE.pop()
            q=frontE.pop()
            if image[p][q]==1:
                if simplification(p,q,"E",image):
                    front.extend((p,q))
        front.reverse()
        for g in range(0,len(front)/2):
            image[front.pop()][front.pop()]=0

        for g in range(0,len(frontS)/2):
            p=frontS.pop()
            q=frontS.pop()
            if image[p][q]==1:
                if simplification(p,q,"S",image):
                    front.extend((p,q))
        front.reverse()
        for g in range(0,len(front)/2):
            image[front.pop()][front.pop()]=0
        for g in range(0,len(frontO)/2):
            p=frontO.pop()
            q=frontO.pop()
            if image[p][q]==1:
                if simplification(p,q,"O",image):
                    front.extend((p,q))
        front.reverse()
        for g in range(0,len(front)/2):
            image[front.pop()][front.pop()]=0

prior()
out(image)

