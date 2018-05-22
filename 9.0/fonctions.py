from skimage import io
import matplotlib.pyplot as plt
import numpy as np
import re
import sys
from collections import deque
import timeit
from copy import copy


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
    f=open('matrice_squelette.txt','w')
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


