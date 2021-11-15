import threading
import time
import random
import matplotlib.pyplot as plt
import numpy as np
import numpy.matlib
import math
import imageio
import itertools
import numpy.ma as ma


def zhoubian(i,j,d):  # get the neighbor
    if i==0 and j==0:
        return[(i,j+1),(i+1,j),(i,j)]
    if i==0 and j==d-1:
        return[(i,j-1),(i+1,j),(i,j)]
    if i==d-1 and j==d-1:
        return[(i,j-1),(i-1,j),(i,j)]
    if i==d-1 and j==0:
        return[(i,j+1),(i-1,j),(i,j)]
    if i==0 and j!=0 and j!=d-1:
        return[(i,j+1),(i+1,j),(i,j-1),(i,j)]

    if i!=0 and i!=d-1 and j==0:
        return[(i-1,j),(i,j+1),(i+1,j),(i,j)]

    if i==d-1 and j!=0 and j!=d-1:
        return[(i-1,j),(i,j+1),(i,j-1),(i,j)]
    if i!=0 and i!=d-1 and j==d-1:
        return[(i,j-1),(i+1,j),(i-1,j),(i,j)]

    if i!=0 and i!=d-1 and j!=0 and j!=d-1:
        return[(i-1,j),(i,j-1),(i,j+1),(i+1,j),(i,j)]


def takep(elem):
    return elem[-1]


def basicAgent1(mat,target,Belief,searchOrder):
    first=searchOrder[0]
    bool=True
    i,j=first
    if first==target[0]:
        ran=random.random()
        if ran>=mat[i,j]:
            return searchOrder
        pass
    yuXian=Belief[i,j]
    Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)   # renew the belief of current cell
    m = 0
    while m < 50:   # renew the belief of other cell
        n = 0
        while n < 50:
            if m!=i or n!=j:
                Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                pass
            n = n + 1
        m = m + 1
    while bool:
        za=[]
        m=0
        while m < 50:
            n = 0
            while n < 50:
                zb=(m,n)
                za.append((zb,Belief[m,n]))
                n = n + 1
            m = m + 1
        za.sort(key=takep,reverse=True)
        hh,he=za[0]
        cur=he
        zab=[]
        for zaa in za:      # same belief go shortest distance one
            hh,he=zaa
            m,n=hh
            if cur==he:
                s=abs(m-i)+abs(n-j)
                zab.append((hh,s))
                pass
            pass
        zab.sort(key=takep)
        hh,he=zab[0]
        i,j=hh
        searchOrder.append(hh)
        if hh==target[0]:  # if this cell has target
            ran=random.random()
            if ran>=mat[i,j]:
                return searchOrder
            pass
        yuXian=Belief[i,j]  # not find yet
        Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)
        m = 0
        while m < 50:
            n = 0
            while n < 50:
                if m!=i or n!=j:
                    Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                    pass
                n = n + 1
            m = m + 1
        pass


def basicAgent2(mat,target,Belief,searchOrder):
    first=searchOrder[0]
    bool=True
    i,j=first
    if first==target[0]:
        ran=random.random()
        if ran>=mat[i,j]:
            return searchOrder
        pass
    yuXian=Belief[i,j]
    Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)   # renew the belief of current cell
    m = 0
    while m < 50:   # renew the belief of other cell
        n = 0
        while n < 50:
            if m!=i or n!=j:
                Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                pass
            n = n + 1
        m = m + 1
    while bool:
        za=[]
        m=0
        while m < 50:
            n = 0
            while n < 50:
                zb=(m,n)
                za.append((zb,(1-mat[m,n])*Belief[m,n]))
                n = n + 1
            m = m + 1
        za.sort(key=takep,reverse=True)
        hh,he=za[0]
        cur=he
        zab=[]
        for zaa in za:   # same belief go shortest distance one
            hh,he=zaa
            m,n=hh
            if cur==he:
                s=abs(m-i)+abs(n-j)
                zab.append((hh,s))
                pass
            pass
        zab.sort(key=takep)
        hh,he=zab[0]
        i,j=hh
        searchOrder.append(hh)
        if hh==target[0]:   # if this cell has target
            ran=random.random()
            if ran>=mat[i,j]:
                return searchOrder
            pass
        yuXian=Belief[i,j]
        Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)
        m = 0
        while m < 50:
            n = 0
            while n < 50:
                if m!=i or n!=j:
                    Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                    pass
                n = n + 1
            m = m + 1
        pass


def valueU(mat,Belief,start):         # find utility(Bellman equation)
    Utility=np.matlib.zeros((50,50))
    Wh=np.matlib.zeros((50,50))
    i,j=start
    bool=True
    c=0
    m = 0
    while m < 50:
        n = 0
        while n < 50:
            Wh[m,n]=Belief[m,n]
            n = n + 1
        m = m + 1

    while c<20:
        W=Wh.copy()
        m = i-5
        if m<0:
            m=0
            pass
        if m+10>=50:
            m=39
            pass
        while m < i+5 and m<50 and m>=0:
            n = j-5
            if n<0:
                n=0
                pass
            if n+10>=50:
                n=39
                pass
            while n < j+5 and n<50 and n>=0:
                a = i-5
                if a<0:
                    a=0
                    pass
                if a+10>49:
                    a=39
                    pass
                while a < i+5 and a<50 and a>=0:
                    b = j-5
                    if b<0:
                        b=0
                        pass
                    if b+10>49:
                        b=39
                        pass
                    while b < j+5 and b<50 and b>=0:
                        s=abs(a-m)+abs(b-n)
                        Wh[m, n]=-0.5*s+0.5*(W[a, b])+Wh[m, n]
                        b = b + 1
                    a = a + 1
                s=abs(i-m)+abs(j-n)
                Wh[m, n]=Wh[m, n]/500+5000*Belief[m,n]
                n = n + 1
            m = m + 1
        m = 0
        bool=False
        while m < 50:
            n = 0
            while n < 50:
                if round(Wh[m, n])!=round(W[m, n]):
                    bool=True
                    pass
                n = n + 1
            m = m + 1
        if not bool:
            bool=True
            #print(Wh)
            #return Wh
            break
            pass
        #print(Wh)
        #print(Utility)
        c=c+1
        pass

    c=0
    while bool:
        U=Utility.copy()
        m = i-5
        if m<0:
            m=0
            pass
        if m+10>49:
            m=39
            pass
        while m < i+5 and m<50 and m>=0:
            n = j-5
            if n<0:
                n=0
                pass
            if n+10>49:
                n=39
                pass
            while n < j+5 and n<50 and n>=0:
                s=abs(i-m)+abs(j-n)
                Utility[m, n]=0.9*Utility[m, n]+0.1*Wh[m,n]-0.03*s
                n = n + 1
            m = m + 1
        m = 0
        bool=False
        while m < 50:
            n = 0
            while n < 50:
                if round(Utility[m, n])!=round(U[m, n]):
                    bool=True
                    pass
                n = n + 1
            m = m + 1
        if not bool:
            #print(Utility)
            return Utility
            pass
        #print(Utility)
        c=c+1
        pass


def improveAgent(mat,target,Belief,searchOrder):

    first=searchOrder[0]
    bool=True
    i,j=first
    if first==target[0]:
        ran=random.random()
        if ran>=mat[i,j]:
            return searchOrder
        pass
    yuXian=Belief[i,j]
    Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)    # renew the belief of current cell
    m = 0
    while m < 50:   # renew the belief of other cells
        n = 0
        while n < 50:
            if m!=i or n!=j:
                Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                pass
            n = n + 1
        m = m + 1

    Ut=valueU(mat,Belief,(i,j))         # get utility
    #print(Ut)
    while bool:
        za=[]
        m=0
        while m < 50:
            n = 0
            while n < 50:
                if m!=i or n!=j:
                    zb=(m,n)
                    za.append((zb,Ut[m,n]))
                n = n + 1
            m = m + 1
        za.sort(key=takep,reverse=True)
        hh,he=za[0]
        i,j=hh
        searchOrder.append(hh)
        if hh==target[0]:   # if this cell has target
            ran=random.random()
            if ran>=mat[i,j]:
                #print(Ut)
                #print(Belief)
                return searchOrder
            pass
        yuXian=Belief[i,j]
        Belief[i,j]=mat[i,j]*yuXian/((1-yuXian)+mat[i,j]*yuXian)
        m = 0
        while m < 50:
            n = 0
            while n < 50:
                if m!=i or n!=j:
                    Belief[m, n] = Belief[m, n]/((1-yuXian)+mat[i,j]*yuXian)
                    pass
                n = n + 1
            m = m + 1
        Ut=valueU(mat,Belief,(i,j))
        #print(hh)
        #print(Ut)
        #print(Belief)
        pass


def maze():   # Generate our maze 50*50
    m = np.matlib.rand(50,50)
    i=0
    while i<50:
        j=0
        while j<50:
            if m[i,j]>=0.75:
                m[i,j]=0.9
                pass
            elif m[i,j]>=0.5:
                m[i,j]=0.7
                pass
            elif m[i,j]>=0.25:
                m[i,j]=0.3
                pass
            else:
                m[i,j]=0.1
            j=j+1
        i=i+1
        pass
    plt.matshow(m, cmap=plt.cm.Greens)
    plt.show()
    return m


def dist(w):  # get the distance
    i=0
    dis=0
    while i<len(w)-1:
        qian=w[i]
        i=i+1
        hou=w[i]
        m,n=qian
        a,b=hou
        dis=dis+abs(a-m)+abs(b-n)
        pass
    return dis


if __name__ == "__main__":
    #o=0
    #w=0
    #while o<50:

    #    w=w+len(wo)
    #    o=o+1
    #    pass
    mat=maze()
    random_list = list(itertools.product(range(0, 50), range(0, 50)))
    target = random.sample(random_list,1)
    print(target)
    i,j=target[0]
    print(mat[i,j])
    Belief=np.matlib.zeros((50,50))
    i = 0
    while i < 50:
        j = 0
        while j < 50:
            Belief[i, j] = 0.0004
            j = j + 1
        i = i + 1
    searchOrder = random.sample(random_list,1)  # get the initial position
    newor=searchOrder.copy()
    newor2=searchOrder.copy()
    print(searchOrder)
    wo=improveAgent(mat,target,Belief,searchOrder)
    print(len(wo)+dist(wo))
    print(wo)
    # wo=basicAgent2(mat,target,Belief,newor2)s
    # print(len(wo)+dist(wo))
    # print(wo)
    # wo=basicAgent1(mat,target,Belief,newor)
    #zhe = np.matlib.zeros((50,50))
    #for zb in wo:
    #    m,n=zb
    #    zhe[m,n]=0.7
    #    pass
    #zhe=ma.masked_array(zhe, zhe<0.5)
    #i,j=target[0]
    #m,n=searchOrder[0]
    #plt.text(x=j, y=i, s='T')
    #plt.text(x=n, y=m, s='S')
    #plt.imshow(mat,interpolation='nearest',cmap=plt.cm.Greens)
    #plt.imshow(zhe,interpolation='nearest',cmap=plt.cm.Reds_r)
    #plt.show()
    # print(len(wo)+dist(wo))
    # print(wo)
    #print(w)
    print("Done.")
