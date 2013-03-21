# -*- coding:utf-8 -*-
'''
Created on 2013-3-21

@author: duanhong
'''
import re
import math

def getwords(doc):
    splitter = re.compile('\\w*')
    words = [s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20]
    
    return dict([(w, 1) for w in words])