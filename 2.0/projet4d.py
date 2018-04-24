from skimage import io
import matplotlib.pyplot as plt
import numpy as np

def out(image):
    i=0
    f=open('out.txt','w')
    while i<len(image):
        j=0
        while j<len(image[1]):
            f.write(str(image[i,j]).zfill(2) + " ")
            if j==len(image[1])-1 :
                f.write("\n")
            j=j+1
        i=i+1
    f.close()

image = io.imread("chevalnb.png")
image = image.astype(int)
x=(len(image))
y=(len(image[0]))
print(x,y)
prio= np.zeros((x,y),dtype=int)
priohg=np.zeros((x,y),dtype=int)
priobg=np.zeros((x,y),dtype=int)
priohd=np.zeros((x,y),dtype=int)
priobd=np.zeros((x,y),dtype=int)
print(prio)
for i in range (2,x-2):
	for j in range (2,y-2):
		#haut gauche
		if (image[i][j]==1 and (priohg[i-1][j]==0 or priohg[i][j-1]==0)):
			priohg[i][j]=1
		elif (image[i][j]==1 and (priohg[i-1][j]>0 and priohg[i][j-1]>0)):
			priohg[i][j]=min(priohg[i-1][j],priohg[i][j-1])+1
		#bas gauche
		if (image[x-i][j]==1 and (priobg[x-i+1][j]==0 or priobg[x-i][j-1]==0)):
			priobg[x-i][j]=1
		elif (image[x-i][j]==1 and (priobg[x-i+1][j]>0 and priobg[x-i][j-1]>0)):
			priobg[x-i][j]=min(priobg[x-i+1][j],priobg[x-i][j-1])+1
		#haut droite
		if (image[i][y-j]==1 and (priohd[i-1][y-j]==0 or priohd[i][y-j+1]==0)):
			priohd[i][y-j]=1
		elif (image[i][y-j]==1 and (priohd[i-1][y-j]>0 and priohd[i][y-j+1]>0)):
			priohd[i][y-j]=min(priohd[i-1][y-j],priohd[i][y-j+1])+1
		#bas droite
		if (image[x-i][y-j]==1 and (priobd[x-i+1][y-j]==0 or priobd[x-i][y-j+1]==0)):
			priobd[x-i][y-j]=1
		elif (image[x-i][y-j]==1 and (priobd[x-i+1][y-j]>0 and priobd[x-i][y-j+1]>0)):
			priobd[x-i][y-j]=min(priobd[x-i+1][y-j],priobd[x-i][y-j+1])+1

for i in range (0,x):
	for j in range (0,y):
		prio[i][j]=min(priohg[i][j],priobg[i][j],priohd[i][j],priobd[i][j])
		#print(priohg[i][j],priobg[i][j],priohd[i][j],priobd[i][j],min(priohg[i][j],priobg[i][j],priohd[i][j],priobd[i][j]))
print(prio)
out(prio)


#plt.imshow(image, cmap=plt.cm.gray)
#plt.show()
#with open('out.txt', 'w') as f:
#    print >> f, 'image:', image  # Python 2.x
#    print('Filename:', filename, file=f)  # Python 3.
