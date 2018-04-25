from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re




#X/I=LIGNES  = 328
#Y/J=COLONNES = 400
#print(i+1,j*3+3)

#Ce programme utilise le fichier "cheval.nb"
#Pour utiliser une forme coloree sur fond blanc, utiliser le fichier conversion.py et decommentariser la ligne
#image = matrice_f("convert.txt") plus bas

#Evidemment tout est loin d'etre optimise.
#Utilisez le fichier "plot_min.py" pour afficher le resultat.

def out(image):
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

def simplification(i,j,d,pic):
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
#image = matrice_f("convert.txt")
x=(len(image))
y=(len(image[0]))
print(x,y)
prio= np.zeros((x,y),dtype=int)
priohg=np.zeros((x,y),dtype=int)
priobg=np.zeros((x,y),dtype=int)
priohd=np.zeros((x,y),dtype=int)
priobd=np.zeros((x,y),dtype=int)
simple=[]
front=[]
print(prio)
for i in range (1,x-1):
	for j in range (1,y-1):
		#A CHANGER: CHAQUE BOUCLE FAIT SA DIAGONALE OPPOSEE!
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

print(prio)
print(prio.max())
for pr in range (1,prio.max()):
	for i in range (1,x-1):
		for j in range (1,y-1):
			if(prio[i][j]==pr and image[i-1][j]==0 and simplification(i,j,"N",image)==1):
				front.extend([i,j])
	front.reverse()
	for g in range(0,len(front)/2):
		image[front.pop()][front.pop()]=0
	for i in range (1,x-1):
		for j in range (1,y-1):
			if(prio[i][j]==pr and image[i][j+1]==0 and simplification(i,j,"E",image)==1):
				front.extend([i,j])
	front.reverse()
	for g in range(0,len(front)/2):
		image[front.pop()][front.pop()]=0
	for i in range (1,x-1):
		for j in range (1,y-1):
			if(prio[i][j]==pr and image[i+1][j]==0 and simplification(i,j,"S",image)==1):
				front.extend([i,j])
	front.reverse()
	for g in range(0,len(front)/2):
		image[front.pop()][front.pop()]=0
	for i in range (1,x-1):
		for j in range (1,y-1):
			if(prio[i][j]==pr and image[i][j-1]==0 and simplification(i,j,"O",image)==1):
				front.extend([i,j])
	front.reverse()
	for g in range(0,len(front)/2):
		image[front.pop()][front.pop()]=0


out(image)

