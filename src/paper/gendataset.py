#coding=utf-8
from random import random,randint

def genmentordataset(num=500):
    out=file('mentor-dataset.csv','w')
    minlat,minlng,maxlat,maxlng = 30.553744,104.017809,30.717208,104.237754
    for i in range(num):
        out.write(str(randint(22,40)))
        out.write(',')
        sex = random()
        if sex>0.5:
            out.write('��')
        else:
            out.write('Ů')
        out.write(',')
        xueli = randint(1,10)
        if xueli==10:
            out.write('����')
        elif xueli>=7:
            out.write('��ר')
        elif xueli>=3:
            out.write('����')
        elif xueli>=1:
            out.write('�о���')
        out.write(',')
        tohouse = random()
        if tohouse>0.5:
            out.write('��')
        else:
            out.write('��')
        out.write(',')
        rating = randint(3,5)
        out.write(str(rating))
        out.write(',')
        lat = minlat + random()*(maxlat-minlat)
        lng = minlng + random()*(maxlng-minlng)
        out.write('%f:%f' % (lat,lng))
        out.write('\n')
    out.close()
    
def genmenteedataset(num=1000):
    out=file('mentee-dataset.csv','w')
    minlat,minlng,maxlat,maxlng = 30.553744,104.017809,30.717208,104.237754
    for i in range(num):
        out.write(str(randint(10,18)))
        out.write(',')
        sex = random()
        if sex>0.5:
            out.write('��')
        else:
            out.write('Ů')
        out.write(',')
        xueli = randint(1,10)
        if xueli==10:
            out.write('δ��ѧ')
        elif xueli>=7:
            out.write('����')
        elif xueli>=4:
            out.write('����')
        elif xueli>=1:
            out.write('Сѧ')
        out.write(',')
        tohouse = random()
        if tohouse>0.5:
            out.write('��')
        else:
            out.write('��')
        out.write(',')
        rating = randint(3,5)
        out.write(str(rating))
        out.write(',')
        lat = minlat + random()*(maxlat-minlat)
        lng = minlng + random()*(maxlng-minlng)
        out.write('%f:%f' % (lat,lng))
        out.write('\n')
    out.close()

def genmatchdataset(num=2154):
    matchdataset = file('match-dataset.csv','w')
    mentorlist=[line for line in file('mentor-dataset.csv')]
    menteelist=[line for line in file('mentee-dataset.csv')]
    i = 0
    while i <= num:
        for mentee in menteelist:
            if i > num: break
            matchdataset.write(mentorlist[randint(0,len(mentorlist)-1)].strip('\n'))
            matchdataset.write(',')
            matchdataset.write(mentee)
            i += 1
    matchdataset.close()
    
def addmilesdistance():
    tempmatchdataset = file('tempmatch-dataset.csv','w')
    oldrows=[line for line in file('match-dataset.csv')]
    for row in oldrows:
        lat1,long1=float(row.split(',')[5].split(':')[0]),float(row.split(',')[5].split(':')[1])
        lat2,long2=float(row.split(',')[11].split(':')[0]),float(row.split(',')[11].split(':')[1])
        latdif=111.1*(lat2-lat1)
        longdif=85.2*(long2-long1)
        newrow = row.strip('\n')+',���%f' % (latdif**2+longdif**2)**.5 + '����\n'
        tempmatchdataset.write(newrow)
    tempmatchdataset.close()