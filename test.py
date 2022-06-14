import cv2
import numpy as np
import math as m
import sys
sys.setrecursionlimit(10**6)


img = cv2.imread(r"C:\Users\mahes\OneDrive\Desktop\OPEN CV WORKSHOP\anu.png")
cv2.imshow("original image",img)
img = cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
c=img
cv2.imshow("original gray image",img)
#print(img[0])
#p = img.shape
#print(p)
#rows,cols = img.shape
lis=[]
list2=[]
# for i in range(rows):
#     for j in range(cols):
#         k = x[i,j]
#         lis.append(k)
# print(len(lis))
codewords=[0,13,23,26,35,46,52,57,70,75,81,92,101,104,114,127]


def compute(osd):
    min=128
    diff=(m.inf)
    for element in codewords:
        d=abs(element-osd)
        if diff>d:
            diff=d
            min=element
    return min
    
def transform(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    osd=int(os2,2)
    res=compute(osd)
    res=convert7(res)
    #o1[4:],o2[5:]=res[0:5],res[5:]
    #print("type",type(o1),type(res))
    o1=o1[0:4]+res[0:4]  
    o2=o2[0:5]+res[4:]
    #print("cover bits",o1,o2)
    #print("decimal value",osd)
    return o1,o2


def convert7(a):
    val= bin(a).replace('0b','')
    x = val[::-1] #this reverses an array.
    while len(x) < 7:
        x += '0'
        val= x[::-1]
    return val
def convert(a):
    val= bin(a).replace('0b','')
    x = val[::-1] #this reverses an array.
    while len(x)<8:
        x += '0'
        val= x[::-1]
    return val
    
#print("output",img[0:1,0:1])
for i in range(0,512):
     for j in range(0,512,2):
        #print("values of i and j",i,j)
        #val = img[i:i+1,j:j+1]
        val2=img[i:i+1,j:j+2]
        o1=convert(val2[0][0])
        #print("sdcvdfvd",val2[0][0])
        o2=convert(val2[0][1])
        #print("output",o1,o2)
        c=transform(o1,o2)
        #print("original bits",o1,o2)
        #print("cover bits",c[0],c[1])
        c0=int(c[0],2)
        c1=int(c[1],2)
        img[i:i+1,j:j+2]=c0,c1
        #print("the transformed")
        #print(o1[4:8:1])
        #print(o2[5:])
cv2.imshow("c=transformed  image ",img)


#message embeding


def transform_bits(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    return os2
for i in range(0,500,28):
     for j in range(0,500,14):
        #print("values of i and j",i,j)
        #val = img[i:i+1,j:j+1]
        val2=img[i:i+1,j:j+14]
        #print("val2",val2)
        p=0
        list3=[]
        for k in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            '''print(o1)
            print(o2)'''
            p=p+1
            c1=transform_bits(o1,o2)
            list3.append(c1)
            #print("list3",list3) gives 7*7 block matrix
        #img[i:i+1,j:j+14]=   
            
        list2.append(list3)
                  #print(c1)

        
       
#print("list2 before flipping",list2[0])       
        
        
    

def indexGen(key,k):   #key generation
    if k==1:
       f1=(key%7)+1
       fk=f1
    else:
       fk=(indexGen(key,k-1)%7)+1
    return fk


B = [               # 3 × 7 HpT parity matrix of the (7, 4) Hamming code
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [1, 1, 1],
    [1, 0, 1]
            ] 


def mul(A):       #Y = R'×HT
    result = [[0,0,0]]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    v=[]
    for r in result:
        for t in r:
            t=t%2
            v.append(t)

    return v

#m=[[1,0,0]]   #message

import math
def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append((bin(i)[2:]))
  return m

print("''message'' in binary is ")
inre=input("enter the message")
li=toBinary(inre)
mi=""
for elem in li:
    mi=mi+elem
#print(mi)
print("mi",mi,len(mi))

z1=0
y1=3
key=int(input("enter key"))   
for b1 in range(len(list2)):  #no of 7*7 blocks in list2  len(list2)
    index=indexGen(key,b1+1)
    #print("key is:",index)
    for j in range(7):
        D=[]
        A=[]
        #print("index",index)
        elem=list2[b1][j]
        #print("elem before fliping",elem)
        for e in elem:
            A.append(int(e))
        #print("A before",A)
        A[index-1]=abs(int(elem[index-1])-1)
        #print("A after 1 bit flipping",A)
        y=mul([A])
        #print("y",y)
        if y1>len(mi):
            break
        m=mi[z1:y1]
        if len(m)<3:
            k1=3
            k1=k1-len(m)
            for i in range(k1):
                m=m+str(0)
    

        print("message",m)
        z1=z1+3
        y1=y1+3
        
        for e in range(3):
            
            D.append(y[e]^int(m[e]))
        
        #print("ddddddddd",D)
        if D!=[0,0,0]:
            for i in range(len(B)):
                if B[i]==D:
                   index=i+1
                   #print("index2",index)
                   A[index-1]=abs(int(elem[index-1])-1)
                   #print("A after 2nd but flipping",A)
                  #print("A after flipping",A)
                   q=6
                   v=0
                   for z in A:
                       v=v+(int(z)*(2**q))
                       q=q-1
                   a1=convert7(v)
                    
                   #print("a1",a1)
        #print("j b1 a1",i,b1,a1)
        list2[b1][j]=a1
                       
                   
        
       
#print("list2 after flipping",list2)
'''i=0
for e in range(len(list2)):
      
    i=i+1
    d=list2[e]
    #print("d",d)
    p=0
    for k in d:
        if(type(k)==type([])):
            print("i",i)
            j=6
            v=0
            for m in k:
                v=v+(int(m)*(2**j))
                j=j-1
            
            #print("d[j]=",d[p])
            d[p]=convert7(v)
            p=p+1
    #print("d after",d)'''


#print("after flippinpg list2",list2)
#j=[6,63,64,109,17,17,116]
#for e in range(7):
#    list2[6][e]=convert7(j[e])
#list2[0][0]=convert7(40)
#print("after flippinpgergrsehbr list2",list2)
#print("list2",list2)

lis7=[]
#print("length of list2",len(list2))
#print("list2",list2)
for i in range(0,500,28):
     k=0
     for j in range(0,500,14):
        #print("values of i and j",i,j)
        #val = img[i:i+1,j:j+1]4:
        val2=img[i:i+1,j:j+14]
        #print("original bits",img[i:i+1,j:j+14])
        p=0
        lis7=list2[i]
        #print("list7 length",lis7)        
        
        
        lis0=[]
        for l in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            p=p+1
            e=lis7[l]
            #print("type o1,e",type(o1),type(e))
            o3=o1[0:4]+e[0:4]
            o4=o2[0:5]+e[4:]
            o5=int(o3,2)
            o6=int(o4,2)
                
            lis0.append(o5)
            lis0.append(o6)
        k=k+1
        #print("lis0",lis0)
        img[i:i+1,j:j+14]=lis0
        #print("lis0",lis0)
            #img[i:i+1,j:j+14]=   

print("the embedded message",mi)
cv2.imshow("cover image with mesaage",img)



#message extraction phase starts from here 
print("message extraction phase starts from here ")
list2=[]
lis7=[]

def transform_bits(o1,o2):
    os1=o1[4:8:1]
    os2= os1 + o2[5:]
    return os2
for i in range(0,500,28):
     for j in range(0,500,14):
        #print("values of i and j",i,j)
        #val = img[i:i+1,j:j+1]
        val2=img[i:i+1,j:j+14]
        #print("val2",val2)
        p=0
        list3=[]
        for k in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            '''print(o1)
            print(o2)'''
            p=p+1
            c1=transform_bits(o1,o2)
            list3.append(c1)
            #print("list3",list3) gives 7*7 block matrix
        #img[i:i+1,j:j+14]=   
            
        list2.append(list3)
key=int(input("enter key the same key which is entered during embedding "))
print("list2[0] in embedding phase",list2[0])

for b1 in range(len(list2)):  #no of 7*7 blocks in list2  len(list2)
    index=indexGen(key,b1+1)
    #print("key is:",index)
    for j in range(7):
        D=[]
        A=[]
        #print("index",index)
        print("index in embedding phase",index)
        syn=B[index-1]
        elem=list2[b1][j]
        #print("elem before fliping",elem)
        for e in elem:
            A.append(int(e))
        #print("A before",A)
        A[index-1]=abs(int(elem[index-1])-1)
        #print("A after 1 bit flipping",A)
        Dif=mul([A])                #Rt× HT
        #print("y",y)
        for e in range(3):
            
            D.append(Dif[e]^syn[e])
        
        #print("ddddddddd",D)
        if D!=[0,0,0]:
            for i in range(len(B)):
                if B[i]==Dif:
                   index=i+1
                   #print("index2",index)
                   A[index-1]=abs(int(elem[index-1])-1)
                   #print("A after 2nd but flipping",A)
                  #print("A after flipping",A)
                   q=6
                   v=0
                   for z in A:
                       v=v+(int(z)*(2**q))
                       q=q-1
                   a1=convert7(v)
                    
                   print("a1",a1)
        #print("j b1 a1",i,b1,a1)
        list2[b1][j]=a1

#print("list2 after extracting message",list2[0])

#replacing original bits to image
for i in range(0,500,28):
     k=0
     for j in range(0,500,14):
        #print("values of i and j",i,j)
        #val = img[i:i+1,j:j+1]4:
        val2=img[i:i+1,j:j+14]
        #print("image before replacing",img[i:i+1,j:j+14])

        #print("original bits",img[i:i+1,j:j+14])
        p=0
        lis7=list2[i]
        #print("list7",lis7)
        #print("list7 length",lis7)        
        
        
        lis0=[]
        for l in range(7):
            o1=convert(val2[0][p])
            o2=convert(val2[0][p+1])
            p=p+1
            e=lis7[l]
            #print("type o1,e",type(o1),type(e))
            o3=o1[0:4]+e[0:4]
            o4=o2[0:5]+e[4:]
            o5=int(o3,2)
            o6=int(o4,2)
                
            lis0.append(o5)
            lis0.append(o6)
        k=k+1
        #print("lis0",lis0)
        img[i:i+1,j:j+14]=lis0
        #print("image after replacing",img[i:i+1,j:j+14])

#print(img.shape)
#print(img)
cv2.imshow("cover image",img)

cv2.waitKey(0)
