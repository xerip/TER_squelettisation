import itertools
import re
import numpy as np
import matplotlib.pyplot as plt

def MakeSet(x):
     x.parent = x
     x.rank   = 0

def Union(x, y):
     xRoot = Find(x)
     yRoot = Find(y)
     if xRoot.rank > yRoot.rank:
         yRoot.parent = xRoot
     elif xRoot.rank < yRoot.rank:
         xRoot.parent = yRoot
     elif xRoot != yRoot: 
         yRoot.parent = xRoot
         xRoot.rank = xRoot.rank + 1

def Find(x):
     if x.parent == x:
        return x
     else:
        x.parent = Find(x.parent)
        return x.parent

class Node:
    def __init__ (self, label):
        self.label = label
    def __str__(self):
        return self.label

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

m=matrice_f('test.txt')
print(m)



"""
l = [Node(ch) for ch in "abcdefg"]
print "objects labels:\t\t\t", [str(i) for i in l]
[MakeSet(node) for node in l]
sets =  [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

Union(l[0],l[1])
sets = [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

Union(l[2],l[4])
sets = [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

Union(l[5],l[6])
sets = [str(Find(x)) for x in l]
print "set representatives:\t\t", sets
print "number of disjoint sets:\t", len([i for i in itertools.groupby(sets)])

for o in l:
    del o.parent
    
"""
"""
assert( Find(l[0]) != Find(l[2]) )
Union(l[0],l[2])        #joining first and third
assert( Find(l[0]) == Find(l[2]) )

assert( Find(l[0]) != Find(l[1]) )
assert( Find(l[2]) != Find(l[1]) )
Union(l[0],l[1])        #joining first and second
assert( Find(l[0]) == Find(l[1]) )
assert( Find(l[2]) == Find(l[1]) )
"""
