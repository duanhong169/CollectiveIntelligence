#coding=gbk
'''
Created on 2013-2-20

@author: duanhong
'''
from numpy import *

class matchrow:
    def __init__(self,row,allnum=False):
        if allnum:
            self.data=[float(row[i]) for i in range(len(row)-1)]
        else:
            self.data=row[0:len(row)-1]
        self.match=int(row[len(row)-1])
    
def loadmatch(f,allnum=False):
    rows=[]
    for line in file(f):
        rows.append(matchrow(line.split(','),allnum))
    return rows

class unmatchrow:
    def __init__(self,row):
        self.data=row

def loadunmatch(f,allnum=False):
    rows=[]
    for line in file(f):
        rows.append(unmatchrow(line.split(',')))
    return rows

def dotproduct(v1,v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def veclength(v):
    return sum([p**2 for p in v])
    
def sex(s):
    if s==(u'男').encode('gbk'): return 1
    else: return 0

def yesno(v):
    if v==(u'是').encode('gbk'): return 1
    elif v==(u'否').encode('gbk'): return -1
    else: return 0

def level(s):
    if s==(u'高中').encode('gbk'): return 1
    elif s==(u'专科').encode('gbk'): return 2
    elif s==(u'本科').encode('gbk'): return 3
    elif s==(u'研究生').encode('gbk'): return 4
    else: return 0
    
def milesdistance(a1,a2):
    lat1,long1=float(a1.split(':')[0]),float(a1.split(':')[1])
    lat2,long2=float(a2.split(':')[0]),float(a2.split(':')[1])
    latdif=111.1*(lat2-lat1)
    longdif=85.2*(long2-long1)
    return (latdif**2+longdif**2)**.5

def loadnumerical():
    oldrows=loadmatch('matched-dataset.csv')
    newrows=[]
    for row in oldrows:
        d=row.data
        data=[float(d[0]),sex(d[1]),level(d[2]),yesno(d[3]),float(d[4]),float(d[6]),sex(d[7]),yesno(d[8]),float(d[9]),milesdistance(d[5],d[10]),row.match]
        newrows.append(matchrow(data))
    return newrows

def scaledata(rows):
    low=[999999999.0]*len(rows[0].data)
    high=[-999999999.0]*len(rows[0].data)
    
    for row in rows:
        d=row.data
        for i in range(len(d)):
            if d[i]<low[i]: low[i]=d[i]
            if d[i]>high[i]: high[i]=d[i]
            
    def scaleinput(d):
        return [(d[i]-low[i])/(high[i]-low[i]) for i in range(len(low))]
    
    newrows=[matchrow(scaleinput(row.data) + [row.match]) for row in rows]
    
    return newrows,scaleinput

def rbf(v1,v2,gamma=20):
    dv=[v1[i]-v2[i] for i in range(len(v1))]
    l=veclength(dv)
    return math.e**(-gamma*l)

def nlclassify(point,rows,offset,gamma=10):
    sum0=0.0
    sum1=0.0
    count0=0
    count1=0
    
    for row in rows:
        if row.match==0:
            sum0+=rbf(point,row.data,gamma)
            count0+=1
        else:
            sum1+=rbf(point,row.data,gamma)
            count1+=1
    y=(1.0/count0)*sum0-(1.0/count1)*sum1+offset
    
    if y>0: return 0
    else: return 1
    
def getoffset(rows,gamma=10):
    l0=[]
    l1=[]
    for row in rows:
        if row.match==0: l0.append(row.data)
        else: l1.append(row.data)
    sum0=sum(sum([rbf(v1,v2,gamma) for v1 in l0]) for v2 in l0)
    sum1=sum(sum([rbf(v1,v2,gamma) for v1 in l1]) for v2 in l1)
    
    return (1.0/(len(l1)**2))*sum1-(1.0/(len(l0)**2))*sum0

def testmethod():
    oldrows=loadunmatch('unmatched-dataset.csv')
    numericalset=loadnumerical()
    scaledset,scalef=scaledata(numericalset)
    ssoffset=getoffset(scaledset)
    matchedcount=0
    for row in oldrows:
        d=row.data
        data=[float(d[0]),sex(d[1]),level(d[2]),yesno(d[3]),float(d[4]),float(d[6]),sex(d[7]),yesno(d[8]),float(d[9]),milesdistance(d[5],d[10])]
        predict = nlclassify(scalef(data), scaledset, ssoffset)
        if predict==1:
            matchedcount+=1
            data=data+[predict]
            print data
    print 'total:%d, matched:%d' % (len(oldrows),matchedcount)