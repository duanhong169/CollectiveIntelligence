'''
Created on 2013-3-19

@author: duanhong
'''

import time
import random
import math

people = [('Seymour', 'BOS'),
          ('Franny', 'DAL'),
          ('Zooey', 'CAK'),
          ('Buddy', 'ORD'),
          ('Les', 'OMA')]

destination = 'LGA'

flights = {}

for line in file('schedule.txt'):
    origin,dest,depart,arrive,price=line.strip().split(',')
    flights.setdefault((origin, dest), [])
    
    flights[(origin, dest)].append((depart, arrive, int(price)))
    
def getminutes(t):
    x = time.strptime(t, '%H:%M')
    return x[3]*60 + x[4]

