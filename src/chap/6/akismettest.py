# -*- coding:utf-8 -*-
'''
Created on 2013-3-23

@author: duanhong
'''
import akismet
defaultkey = "4b1289053d4d"
# must have a wordpress blog
pageurl = "http://myblog.com"

defaultagent = "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-us; rv:1.8.0.7) "
defaultagent += "Gecko/20060909 Firefox/1.5.0.7"

def isspam(comment, author, ipaddress, agent = defaultagent, apikey = defaultkey):
    try:
        valid = akismet.verify_key(apikey, pageurl)
        if valid:
            return akismet.comment_check(apikey, pageurl, ipaddress, agent, comment_content = comment,
                                         comment_author_email = author, comment_type = "comment")
        else:
            print 'Invalid key'
            return False
    except akismet.AkismetError, e:
        print e.response, e.statuscode
        return False