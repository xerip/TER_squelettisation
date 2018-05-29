from fonctions import *

from mpl_toolkits.mplot3d import Axes3D


#toutes les fonctions du programme sont dans le fichier fonctions.py
#Utiliser le programme "reconversion.py" pour reconstituer une image si le squelette a deja ete calcule (fichier matrice_squelette.txt)


#par simplification memorielle cette fonction est inclue dans le fichier principal.
def squelettisation(dir):
	if dir=="N":
		for g in range(0,len(frontN)/2):
			p=frontN.popleft()
			q=frontN.popleft()
			if image[p][q]==1:
				if simplification(p,q,"N",image):
					front.extend((p,q))
		for g in range(0,len(front)/2):
			image[front.popleft()][front.popleft()]=0
	if dir=="E":
		for g in range(0,len(frontE)/2):
			p=frontE.popleft()
			q=frontE.popleft()
			if image[p][q]==1:
				if simplification(p,q,"E",image):
					front.extend((p,q))
		for g in range(0,len(front)/2):
			image[front.popleft()][front.popleft()]=0
	if dir=="S":
		for g in range(0,len(frontS)/2):
			p=frontS.popleft()
			q=frontS.popleft()
			if image[p][q]==1:
				if simplification(p,q,"S",image):
					front.extend((p,q))
		for g in range(0,len(front)/2):
			image[front.popleft()][front.popleft()]=0
	if dir=="O":
		for g in range(0,len(frontO)/2):
			p=frontO.popleft()
			q=frontO.popleft()
			if image[p][q]==1:
				if simplification(p,q,"O",image):
					front.extend((p,q))
		for g in range(0,len(front)/2):
			image[front.popleft()][front.popleft()]=0



####Debut Main #####

#recuperation du fichier et message d'aide.

if (len(sys.argv)<2):
	print("Erreur: Veuillez entrez en premier l'addresse du fichier.\n Options:\
	\n'-4d' ou '-8d' pour le degre de simplifiction (8d par defaut).\
	\n'-s','-p' ou  pour afficher le squelette ou la profondeur, ne rien mettre pour avoir le squelette avec la profondeur (et le fichier pour reconvertir)\
	\n ajoutez '-inv' pour inverser la transposition de l'image (par defaut blanc sur fond noir,sinon couleur sur fond blanc/transparent.)\
	\n Enfin, vous pouvez configurer l'ordre de cardinalite en ajoutant les 4 initiales des points cardinaux en un seul mot.\
	\nExemple:'NOES' for Nord-Ouest-Est-Sud.")
	sys.exit()



#transformation de l'image et definitions de valeurs.
inv=0
args=sys.argv
image = io.imread(args[1])
for i in range (2,len(sys.argv)):
	if (args[i]=="-inv"):
		inv=1
image = convert_nb(image,inv)

#preparation de l'affichage final.
fig,axes = plt.subplots(nrows=1, ncols=2, figsize=(8, 4),sharex=True, sharey=True)
ax = axes.ravel()        
ax[0].imshow(image, cmap=plt.cm.gray)
ax[0].axis('off')
ax[0].set_title('original', fontsize=20)


x=(len(image))
y=(len(image[0]))
print("Image definie, Dimensions:",x,y)


#securite pour corriger les erreurs sur les bors des images.
for i in range(0,x):
	image[i][0]=0
	image[i][y-1]=0
for i in range(0,y):
	image[0][i]=0
	image[x-1][i]=0


#calcul de la profondeur:
image,prio=profondeurs(image,x,y)
priomax=prio.max()
print("profondeur calculee:",priomax)

for k in range (2,len(sys.argv)):
	if(args[k]=="-p"):
		flag=0
		ax[1].imshow(prio)
		ax[1].axis('off')
		ax[1].set_title('profondeur', fontsize=20)
		surf = ax.plot_surface(prio,cmap=cm.coolwarm,linewidth=0,antialiased=False)
		plt.show()
		sys.exit()


front=deque()
frontN = deque()
frontE = deque()
frontS = deque()
frontO = deque()
front=deque()

megaliste=[]
listecompteur=np.zeros(priomax+1,dtype=int)

for i in range(1,x-1):
	for j in range (1,y-1):
		if(prio[i][j]>0):
			listecompteur[prio[i][j]]=listecompteur[prio[i][j]]+1
			pos=0
			for g in range(1,prio[i][j]):
				pos=pos+listecompteur[g]
			megaliste.insert(pos,(i,j))




megaliste.reverse()
print("Nombre de pixels de la forme: ",len(megaliste),"squelettisation en cours..."	)

#determine si la simplification est 4d ou 8d.
simplification=simplification8d
for i in range (2,len(sys.argv)):
	if (args[i]=="-4d"):
		simplification=simplification4d


#squelettisation, par priorite.
#Par ordre N E S O par defaut, determine les forntiere puis les supprime en fin de passe.


direc=["N","E","S","O"]

for i in range (2,len(sys.argv)):
	if (args[i][0]=="N" or args[i][0]=="S" or args[i][0]=="E" or args[i][0]=="O"):
		if len(args[i])==4:
			direc[0]=args[i][0]
			direc[1]=args[i][1]
			direc[2]=args[i][2]
			direc[3]=args[i][3]
			print("Direction de squelettisation:",direc)

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

	
	squelettisation(direc[0])
	squelettisation(direc[1])
	squelettisation(direc[2])
	squelettisation(direc[3])







ax[1].imshow(image, cmap=plt.cm.gray)
ax[1].axis('off')
ax[1].set_title('squelette', fontsize=20)

for i in range(0,x):
	for j in range(0,y):
		if image[i][j]:
			image[i][j]=prio[i][j]

#sauvegarde le squelette.
out(image,x,y)

for k in range (2,len(sys.argv)):
	if(args[k]=="-ps"):
		ax[1].imshow(image, cmap=plt.cm.gray)

#affichage
plt.show()

