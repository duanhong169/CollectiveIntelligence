'''
Created on 2013-3-20

@author: duanhong
'''

import random
import math

dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

prefs = [('Toby', ('Bacchus', 'Hercules')),
         ('Steve', ('Zeus', 'Pluto')),
         ('Andrea', ('Athena', 'Zeus')),
         ('Sarah', ('Zeus', 'Pluto')),
         ('Dave', ('Athena', 'Bacchus')), 
         ('Jeff', ('Hercules', 'Pluto')), 
         ('Fred', ('Pluto', 'Athena')), 
         ('Suzie', ('Bacchus', 'Hercules')), 
         ('Laura', ('Bacchus', 'Hercules')), 
         ('James', ('Hercules', 'Athena'))]

domain = [(0, (len(dorms)*2)-i-1) for i in range(0, len(dorms)*2)]

def printsolution(vec):
    slots = []
    for i in range(len(dorms)): slots += [i,i]
    
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        print prefs[i][0], dorm
        del slots[x]