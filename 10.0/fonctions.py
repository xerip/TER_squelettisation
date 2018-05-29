from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
from collections import deque


#calcule la pronfondeur de l'image
def profondeurs(image,x,y):
	prio= np.zeros((x,y),dtype=int)
	priohg=np.zeros((x,y),dtype=int)
	priobg=np.zeros((x,y),dtype=int)
	priohd=np.zeros((x,y),dtype=int)
	priobd=np.zeros((x,y),dtype=int)
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
	return (image,prio)
	

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



def out(image,x,y): #convertit le resultat final dans un fichier.
    i=0
    f=open('squelette.txt','w')
    f.write(str(x) + " " + str(y))
    f.write("\n")
    while i<len(image):
        j=0
        while j<len(image[0]):
		if image[i][j]>0:
           		f.write(str(i) + " " + str(j) + " " + str(int(image[i][j])))
	                f.write("\n")
       		j=j+1
        i=i+1
    f.close()




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
					if(b>=1):
						return 1
					else:
						return 0
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
					if(b>=1):
						return 1
					else:
						return 0
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
					if(b>=1):
						return 1
					else:
						return 0
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
					if(b>=1):
						return 1
					else:
						return 0
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


