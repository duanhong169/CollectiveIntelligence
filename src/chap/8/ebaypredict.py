'''
Created on 2013-2-5

@author: duanhong
'''

import httplib
from xml.dom.minidom import parse, parseString, Node

devKey = '7289a1b6-29da-4124-bd12-d652a1e46fac'
appKey = 'HongDuan-ace9-417a-920e-9fe7a93c4377'
certKey = 'bc0aaf0b-9987-4ef2-bb15-1d8afebe6c05'
userToken = 'AgAAAA**AQAAAA**aAAAAA**p/sQUQ**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6AFlYahDpOBpAidj6x9nY+seQ**Br0BAA**AAMAAA**R+dU6fB26J1GfJ6+56KJT52fH45EqYtP4tXcdogz/OpD8OX1IqG2cN+ZxW4VGkWc2e9ab5JtVA/qHvHnA1SdyXGcfLeMusAz+0pdysj/DSnoxCWdlmRdAIdv56p/gnGFON3h402xF8QuIr4BARfOd/Gct+cS0PAj9tWmbnSYTwo4kw16FFnCtWRvZb8+lLyGEgaOXsISJssou1d3XbgvB6BHHD9FeH06FZAB7D4zwlPVgitEeqMlbb9ESoLycuTjMYk5LkVt9RiTrU5msGQBAcFh73rCCJnFHo+eB0+zb7fEw1XEfhLiHmD8RIfey9dkyz08WFfVLFXspd+JuKFdtutQWpu+QNOBHOJc6aZdh4ya+hK7b7TP6KBmTtaxMbR4iwUkRNcbkEtUgzceLkF8xGVhkOTMTVuvqFB3Q+Gj1/WZ9h9AOBUXCyys8af0VvKGRxavtMzgZb6uZJX7zANY/IHUQOysF2F6OZFjSVi6m6ai1/s76c7NjUo6Bs2sVRYQ9zN4TFbbojsI2VbovtxrIx+odgA3OXfzZDEsodVUWmDrHAm8Q/7yRvUVzLrE9fOmIYWgY6sTCUkA8tOWkhCLdGLgggEugsi7aqKmwdtm4ytQb41AtQL7jsuU2bKqLAeF/NmEzWRmCgAaBqfoIwB83D4Xx8G4NgH1TiacTyV57mdMhruLxo8OQwotDQXoakWymnVBpmW1AWCcOgcWpr0kDO5WD9DwURubkQxVYhZ2YbQ20iwxURPk1gCkmHG8VMiL'
serverUrl = 'api.ebay.com'

def getHeaders(apicall,siteID="0",compatabilityLevel = "433"):
    headers = {"X-EBAY-API-COMPATIBILITY-LEVEL": compatabilityLevel,
             "X-EBAY-API-DEV-NAME": devKey,
             "X-EBAY-API-APP-NAME": appKey,
             "X-EBAY-API-CERT-NAME": certKey,
             "X-EBAY-API-CALL-NAME": apicall,
             "X-EBAY-API-SITEID": siteID,
             "Content-Type": "text/xml"}
    return headers

def sendRequest(apicall,xmlparameters):
    connection = httplib.HTTPSConnection(serverUrl)
    connection.request("POST", '/ws/api.dll', xmlparameters, getHeaders(apicall))
    response = connection.getresponse()
    if response.status != 200:
        print "Error sending request:" + response.reason
    else:
        data = response.read()
        connection.close()
    return data

def getSingleValue(node,tag):
    nl=node.getElementsByTagName(tag)
    if len(nl)>0:
        tagNode=nl[0]
        if tagNode.hasChildNodes():
            return tagNode.firstChild.nodeValue
    return '-1'

def doSearch(query,categoryID=None,page=1):
    xml = "<?xml version='1.0' encoding='utf-8'?>"+\
        "<GetSearchResultsRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>" + \
        "<Pagination>"+\
            "<EntriesPerPage>200</EntriesPerPage>"+\
            "<PageNumber>"+str(page)+"</PageNumber>"+\
        "</Pagination>"+\
        "<Query>" + query + "</Query>"
    if categoryID!=None:
        xml+="<CategoryID>"+str(categoryID)+"</CategoryID>"
    xml+="</GetSearchResultsRequest>"
    
    data=sendRequest('GetSearchResults',xml)
    response = parseString(data)
    itemNodes = response.getElementsByTagName('Item')
    results = []
    for item in itemNodes:
        itemId=getSingleValue(item,'ItemID')
        itemTitle=getSingleValue(item,'Title')
        itemPrice=getSingleValue(item,'CurrentPrice')
        itemEnds=getSingleValue(item,'EndItem')
        results.append((itemId,itemTitle,itemPrice,itemEnds))
    return results

def getCategory(query='',parentID=None,siteID='0'):
    lquery=query.lower()
    xml = "<?xml version='1.0' encoding='utf-8'?>" + \
        "<GetCategoriesRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">" + \
        "<RequetsCredentials><eBayAuthToken>" + \
        userToken + \
        "</eBayAuthToken></RequesterCredentials>" + \
        "<DetailLevel>ReturnAll</DetailLevel>" + \
        "<ViewAllNodes>true</ViewAllNodes>" + \
        "<CategorySiteID>"+siteID+"</CategorySiteID>"
    if parentID==None:
        xml+="<LevelLimit>1</LevelLimit>"
    else:
        xml+="<CategoryParent>"+str(parentID)+"</CategoryParent>"
    xml += "</GetCategoriesRequest>"
    data=sendRequest('GetCategories',xml)
    categoryList=parseString(data)
    catNodes=categoryList.getElementsByTagName('Category')
    for node in catNodes:
        catid=getSingleValue(node,'CategoryID')
        name=getSingleValue(node,'CategoryName')
        if name.lower().find(lquery)!=-1:
            print catid,name
            
def getItem(itemID):
    xml = "<?xml version='1.0' encoding='utf-8'?>"+\
        "<GetItemRequest xmlns=\"urn:ebay:apis:eBLBaseComponents\">"+\
        "<RequesterCredentials><eBayAuthToken>" +\
        userToken +\
        "</eBayAuthToken></RequesterCredentials>" + \
        "<ItemID>" + str(itemID) + "</ItemID>"+\
        "<DetailLevel>ItemReturnAttributes</DetailLevel>"+\
        "</GetItemRequest>"
    data=sendRequest('GetItem',xml)
    result={}
    response=parseString(data)
    result['title']=getSingleValue(response,'Title')
    sellingStatusNode = response.getElementsByTagName('SellingStatus')[0];
    result['price']=getSingleValue(sellingStatusNode,'CurrentPrice')
    result['bids']=getSingleValue(sellingStatusNode,'BidCount')
    seller = response.getElementsByTagName('Seller')
    result['feedback'] = getSingleValue(seller[0],'FeedbackScore')

    attributeSet=response.getElementsByTagName('Attribute');
    attributes={}
    for att in attributeSet:
        attID=att.attributes.getNamedItem('attributeID').nodeValue
        attValue=getSingleValue(att,'ValueLiteral')
        attributes[attID]=attValue
        result['attributes']=attributes
    return result

def makeLaptopDataset():
    searchResults=doSearch('laptop',categoryID=51148)
    result=[]
    for r in searchResults:
        item=getItem(r[0])
        att=item['attributes']
        try:
            data=(float(att['12']),float(att['26444']),
                  float(att['26446']),float(att['25710']),
                  float(item['feedback'])
                  )
            entry={'input':data,'result':float(item['price'])}
            result.append(entry)
        except:
            print item['title']+' failed'
    return result