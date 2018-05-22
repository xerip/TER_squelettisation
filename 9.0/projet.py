from skimage import io
import matplotlib.pyplot as plt
import numpy as np

def out(image):
    i=0
    f=open('out.txt','w')
    while i<len(image):
        j=0
        while j<len(image[1]):
            f.write(str(image[i,j]) + " ")
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
prio=np.zeros((x,y),dtype=int)
priohg= np.zeros((x,y),dtype=int)
priohd= np.zeros((x,y),dtype=int)
print(prio)
for i in range (1,x):
	for j in range (1,y):
		if (image[i][j]==1 and (priohg[i-1][j]==0 or priohg[i][j-1]==0)):
			priohg[i][j]=1
		elif (image[i][j]==1 and (priohg[i-1][j]>0 and priohg[i][j-1]>0)):
			priohg[i][j]=min(priohg[i-1][j],priohg[i][j-1])+1
		if (image[i][y-j]==1 and (priohd[i-1][y-j]==0 or priohd[i][y-j+1]==0)):
			priohd[i][y-j]=1
		elif (image[i][y-j	]==1 and (priohd[i-1][y-j]>0 and priohd[i][y-j+1]>0)):
			priohd[i][y-j]=min(priohd[i-1][y-j],priohd[i][y-j+1])+1






for i in range (0,x):
	for j in range (0,y):
		prio[i][j]=min(priohg[i][j],priohd[i][j])
		print(priohg[i][j],priohd[i][j],min(priohg[i][j],priohd[i][j]))
print(prio)
out(prio)


#plt.imshow(image, cmap=plt.cm.gray)
#plt.show()
#with open('out.txt', 'w') as f:
#    print >> f, 'image:', image  # Python 2.x
#    print('Filename:', filename, file=f)  # Python 3.
