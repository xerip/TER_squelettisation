import re

"""
f=open('coordonnees.txt','r')
liste=[]
for line in f :
    line = re.sub('\n','',line) 
    line=re.split(' ', line)
    liste=liste+[line]
    print(line[0])

print(liste)
"""

f=open('coordonnees.txt','r')

firstline=f.readline().split()
x,y=firstline[0],firstline[1]
print(x,y)

"""
for line in f :
    x,y,z=re.sub('\n','',line).split()
    print(x,y,z)

"""
