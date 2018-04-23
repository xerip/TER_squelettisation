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
prio= np.zeros((x,y))
print(prio)
for i in range (0,x):
	for j in range (0,y):
		if (image[i][j]==1 and (prio[i-1][j]==0 or prio[i][j-1]==0)):
			prio[i][j]=1
		if (image[i][j]==1 and (prio[i-1][j]>0 and prio[i][j-1]>0)):
			prio[i][j]=min(prio[i-1][j],prio[i][j-1])+1
            
print(prio)
out(prio)


#plt.imshow(image, cmap=plt.cm.gray)
#plt.show()
#with open('out.txt', 'w') as f:
#    print >> f, 'image:', image  # Python 2.x
#    print('Filename:', filename, file=f)  # Python 3.
