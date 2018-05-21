from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
from collections import deque
import timeit
from copy import copy


#X/I=LIGNES  = 328
#Y/J=COLONNES = 400
#print(i+1,j*3+3)

#Ce programme utilise le fichier "cheval.nb"
#Pour utiliser une forme coloree sur fond blanc, utiliser le fichier conversion.py et decommentariser la ligne
#image = matrice_f("convert.txt") plus bas

#Evidemment tout est loin d'etre optimise.
#Utilisez le fichier "plot_min.py" pour afficher le resultat.



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
            else:
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
            j=j+1
        i=i+1
    return m



def out(image): #convertit le resultat final dans un fichier.
    i=0
    f=open('squelette.txt','w')
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

def simplification8d(i,j,d,pic):  #determine si un point est simple ou terminal.
	N=pic[i-1][j]
	S=pic[i+1][j]
	E=pic[i][j+1]
	O=pic[i][j-1]
	NE=pic[i-1][j+1]
	SE=pic[i+1][j+1]
	SO=pic[i+1][j-1]
	NO=pic[i-1][j-1]
	if (d=='N'):
		p=O + E + S
		t=NO+NE
		b=SO+SE
		if(p==3):
			return 1
 	 	elif (p+t+b<=1):
			return 0
		elif (p==1):
			if (b>1 and t>1):
				return 0
			elif (S==1):
				if(t>0):
					return 0
				else:
					return 1
			elif (O==0 and (NO or SO) or (E==0 and (NE or SE)	)):
				return 0
			else:

				return 1
			
		elif (p==2):
			if (S==0):
				return 0		
			else:
				if ((NO==1 and O==0) or (NE==1 and E==0)):
					return 0
				else:
					return 1
		elif (p==0 and b+t>1):
			return 0

	if (d=='E'):
		p=O + N + S
		t=NE+SE
		b=NO+SO
		if(p==3):
			return 1
		elif (p+t+b<=1):
			return 0
		elif (p==1):
			if (b>1 and t>1):
				return 0
			elif (O==1):
				if(t>0):
					return 0
				else:
					return 1
			elif (N==0 and (NE or NO) or (S==0 and (SE or SO))):
				return 0
			else:
				return 1
			
		elif (p==2):
			if (O==0):
				return 0		
			else:
				if ((NE==1 and N==0) or (SE==1 and S==0)):
					return 0
				else:
					return 1
		elif (p==0 and b+t>1):
			return 0		

	if (d=='S'):
		p=N + E + O
		t=SE+SO
		b=NE+NO
		if(p==3):
			return 1
		elif (p+t+b<=1):
			return 0
		elif (p==1):
			if (b>1 and t>1):
				return 0
			elif (N==1):
				if(t>0):
					return 0
				else:
					return 1
			elif (E==0 and (NE or SE) or (O==0 and (NO or SO))):
				return 0
			else:
				return 1
			
		elif (p==2):
			if (N==0):
				return 0		
			else:
				if ((SE==1 and E==0) or (SO==1 and O==0)):
					return 0
				else:
					return 1
		elif (p==0 and b+t>1):
			return 0

	if (d=='O'):
		p=N + S + E
		t=NO+SO
		b=NE+SE
		if(p==3):
			return 1
		elif (p+t+b<=1):
			return 0
		elif 	(p==1):
			if (b>1 and t>1):
				return 0
			elif (E==1):
				if(t>0):
					return 0
				else:
					return 1
			elif (N==0 and (NE or NO) or (S==0 and (SE or SO))):
				return 0
			else:
				return 1
			
		elif (p==2):
			if (E==0):
				return 0		
			else:
				if ((NO==1 and N==0) or (SO==1 and S==0)):
					return 0
				else:
					return 1
		elif (p==0 and b+t>1):
			return 0

def simplification4d(i,j,d,pic):  #determine si un point est simple ou terminal.
	N=pic[i-1][j]
	E=pic[i][j+1]
	S=pic[i+1][j]
	O=pic[i][j-1]	
	if (d=='N'):
		p=O + E + S
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i+1][j-1]+pic[i+1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (S == 0):
				return 0
			elif ((O and pic[i+1][j-1]) or (pic[i+1][j+1] and E)):
				return 1
			else:
				return 0
	if (d=='E'):
		p=O + N + S
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j-1]+pic[i+1][j-1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (O == 0):
				return 0
			elif ((pic[i-1][j-1] and N) or (pic[i+1][j-1] and S)):
				return 1
			else:
				return 0
	if (d=='S'):
		p=N + E + O
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j-1]+pic[i-1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (N == 0):
				return 0
			elif ((pic[i-1][j-1] and O) or (pic[i-1][j+1] and E)):
				return 1
			else:
				return 0
	if (d=='O'):
		p=N + S + E
		if (p<=1):
			return 0
		elif (p==3):
			if (pic[i-1][j+1]+pic[i+1][j+1]==2):
				return 1
			else:
				return 0
		elif (p==2):
			if (E == 0):
				return 0
			elif ((pic[i+1][j+1] and S) or (pic[i-1][j+1] and N)):
				return 1
			else:
				return 0

def matrice_min_int(m, n): #la matrice devient une matrice de 1 et de 0 selon un entier minimum
			   #pourra etre utilisee dans le futur pour afficher les profondeurs du squelettes.
    i=0
    while i<len(m):
        j=0
        while j<len(m[i]):
            if m[i][j]>=n:
                m[i][j]=m[i][j]
		#m[i][j]=1
            else:
                m[i][j]=0
            j=j+1
        i=i+1
    return m



if (len(sys.argv)<4):
	print("Erreur: Veuillez entrez trois parametre:L'adresse du fichier,l'option '-4d' ou '-8d' et '-s','-p' ou '-sp' enfin ajoutez '-inv' pour inverser l'image.")
	sys.exit()



inv=0
args=sys.argv
image = io.imread(args[1])
if (len(sys.argv)==5):
	print(args[4])
	if (args[4]=="-inv"):
		inv=1
image = convert_nb(image,inv)
orig=copy(image)

fig,axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),
                         sharex=True, sharey=True)
ax = axes.ravel()        

ax[0].imshow(orig, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)

print("Image definie")
x=(len(image))
y=(len(image[0]))
print("Dimensions:",x,y)
for i in range(0,x):
	image[i][0]=0
	image[i][y-1]=0
for i in range(0,y):
	image[0][i]=0
	image[x-1][i]=0
#definitions des table utilisees pour la priorites.
prio= np.zeros((x,y),dtype=int)
priohg=np.zeros((x,y),dtype=int)
priobg=np.zeros((x,y),dtype=int)
priohd=np.zeros((x,y),dtype=int)
priobd=np.zeros((x,y),dtype=int)
simple=[]

front=deque()
#Calcul de profondeur par chaque extremite.
for i in range (1,x):
	for j in range (1,y):
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
print("profondeur calculee :")
print(priomax)
frontN=deque()
frontE=deque()
frontS=deque()
frontO=deque()
front=deque()
megaliste=[]
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

if(args[3]=="-p"):
	ax[1].imshow(prio)
	ax[1].axis('off')
	ax[1].set_title('profondeur', fontsize=20)
	plt.show()
	sys.exit()

megaliste.reverse()
print(len(megaliste))
if (args[2]=="-4d"):
	simplification=simplification4d
else:
	simplification=simplification8d
for pr in range (1,priomax+1):
	for g in range(0,listecompteur[pr]):
		p=megaliste.pop()
		if image[p[0]-1][p[1]]==0:
				frontN.extend((p[0],p[1]))
		if image[p[0]][p[1]+1]==0:
				frontE.extend((p[0],p[1]))
		if image[p[0]+1][p[1]]==0:
				frontS.extend((p[0],p[1]))
		if image[p[0]][p[1]-1]==0:
				frontO.extend((p[0],p[1]))




	for g in range(0,len(frontN)/2):
		p=frontN.popleft()
		q=frontN.popleft()
		if image[p][q]==1:
			if simplification(p,q,"N",image):
				front.extend((p,q))
	for g in range(0,len(front)/2):
		image[front.popleft()][front.popleft()]=0
	for g in range(0,len(frontE)/2):
		p=frontE.popleft()
		q=frontE.popleft()
		if image[p][q]==1:
			if simplification(p,q,"E",image):
				front.extend((p,q))
	for g in range(0,len(front)/2):
		image[front.popleft()][front.popleft()]=0
	for g in range(0,len(frontS)/2):
		p=frontS.popleft()
		q=frontS.popleft()
		if image[p][q]==1:
			if simplification(p,q,"S",image):
				front.extend((p,q))
	for g in range(0,len(front)/2):
		image[front.popleft()][front.popleft()]=0
	for g in range(0,len(frontO)/2):
		p=frontO.popleft()
		q=frontO.popleft()
		if image[p][q]==1:
			if simplification(p,q,"O",image):
				front.extend((p,q))
	for g in range(0,len(front)/2):
		image[front.popleft()][front.popleft()]=0







if (args[3]=="-ps"):
	for i in range(0,x):
		for j in range(0,y):
			if image[i][j]:
				image[i][j]=prio[i][j]
	out(image)


ax[1].imshow(image, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('squelette', fontsize=20)
plt.show()




