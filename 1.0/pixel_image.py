from skimage import io
import matplotlib.pyplot as plt
import numpy as np


image = io.imread("chevalnb.png")
image = image.astype(int)

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
    
out(image)


image = io.imread("chevalnb.png")
image = image.astype(int)
print(len(image))
print(len(image[1]))
print(image[150,200])
plt.imshow(image, cmap=plt.cm.gray)
plt.show()
"""
print(type(image[0,0]))
print(type(str(image[0,0])))
f=open('out.txt','w')
f.write("une chaine" + str(image[150,200]) + "\n")
f.close()
with open('out.txt', 'w') as f:
    print >> f, 'image:', image  # Python 2.x
    #print('Filename:', filename, file=f)  # Python 3.
"""
