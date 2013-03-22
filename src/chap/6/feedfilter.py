# -*- coding:utf-8 -*-
'''
Created on 2013-3-22

@author: duanhong
'''
import feedparser
import re

def read(feed, classifier):
    f = feedparser.parse(feed)
    for entry in f['entries']:
        print 
        print '-----'
        print 'Title:    ' + entry['title'].encode('utf-8')
        print 'Publisher:    ' + entry['publisher'].encode('utf-8')
        print 
        print entry['summary'].encode('utf-8')
        
        fulltext = '%s\n%s\n%s' % (entry['title'], entry['publisher'], entry['summary'])
        print 'Guess: ' + str(classifier.classify(fulltext))
        
        c1 = raw_input('Enter category: ')
        classifier.train(fulltext, c1);