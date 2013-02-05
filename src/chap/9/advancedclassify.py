'''
Created on 2013-2-5

@author: duanhong
'''

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

from pylab import *
def plotagematches(rows):
    xdm,ydm=[r.data[0] for r in rows if r.match==1],[r.data[1] for r in rows if r.match==1]
    xdn,ydn=[r.data[0] for r in rows if r.match==0],[r.data[1] for r in rows if r.match==0]
    
    plot(xdm,ydm,'go')
    plot(xdn,ydn,'rx')
    
    show()
    
def lineartrain(rows):
    averages={}
    counts={}
    
    for row in rows:
        cl=row.match
        
        averages.setdefault(cl,[0.0]*(len(row.data)))
        counts.setdefault(cl,0)
        
        for i in range(len(row.data)):
            averages[cl][i]+=float(row.data[i])
            
        counts[cl]+=1
        
    for cl,avg in averages.items():
        for i in range(len(avg)):
            avg[i]/=counts[cl]
            
    return averages

def dotproduct(v1,v2):
    return sum([v1[i]*v2[i] for i in range(len(v1))])

def dpclassify(point,avgs):
    b=(dotproduct(avgs[1],avgs[1])-dotproduct(avgs[0],avgs[0]))/2
    y=dotproduct(point,avgs[0])-dotproduct(point,avgs[1])+b
    if y>0: return 0
    else: return 1
    
def yesno(v):
    if v=='yes': return 1
    elif v=='no': return -1
    else: return 0
    
def matchcount(interest1,interest2):
    l1=interest1.split(':')
    l2=interest2.split(':')
    x=0
    for v in l1:
        if v in l2: x+=1
    return x

#def milesdistance(a1,a2):
#    return 0

baidukey="b2fb7564a3286f30cae86464f7985e2e"
from xml.dom.minidom import parseString
from urllib import urlopen,quote_plus

loc_cache={}
def getlocation(address):
    if address in loc_cache: return loc_cache[address]
    data=urlopen('http://api.map.baidu.com/geocoder?address=%s&output=xml&key=%s' % (quote_plus(address),baidukey)).read()
    doc=parseString(data)
    lat=doc.getElementsByTagName('lat')[0].firstChild.nodeValue
    long=doc.getElementsByTagName('lng')[0].firstChild.nodeValue
    loc_cache[address]=(float(lat),float(long))
    return loc_cache[address]

def milesdistance(a1,a2):
    lat1,long1=getlocation(a1)
    lat2,long2=getlocation(a2)
    latdif=69.1*(lat2-lat1)
    longdif=53.0*(long2-long1)
    return (latdif**2+longdif**2)**.5

