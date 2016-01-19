#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

import codecs
import base64
import quopri
import datetime
import re
#import urllib

#from lxml import html
from xml.sax.saxutils import *
from HTMLParser import HTMLParser
from gmailapi import GmailApi

from bs4 import BeautifulSoup

'''
class out_link_parser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.dataList = []
        self.links = []
        self.linkurl = ''

#        self.data = ''

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs:
                self.linkurl = attrs['href']

    def handle_data(self, data):
        print data

        self.dataList.append(data)
        if self.linkurl:
            self.links.append(self.linkurl)
            self.linkurl = ''
'''

'''
    def reset(self):
        HTMLParser.reset(self)
        self.pages    = []
        self.text     = []                     # *****
        self.dataList     = []                     # *****
        self.links = []
        self.is_li    = False
        self.num_as   = 0
        self.close_a  = False
        self.close_li = False
        self.linkurl = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'li':
            self.is_li    = True
            self.close_a  = False
            self.close_li = False

        if tag == 'a' and self.is_li:
            if self.num_as < 7:
                self.num_as += 1
                self.close_a = False
            else:
                self.num_as = 0
                self.is_li = False
        if tag == 'a':
            attrs = dict(attrs)
            if 'href' in attrs:
                self.linkurl = attrs['href']

    def handle_endtag(self, tag):
         if tag == 'a':
             self.close_a  = True
         if tag == 'li':
             self.close_li = True
             self.num_as   = 0
             self.pages.append("".join(self.text))      # *****
             self.text = []                             # *****

    def handle_data(self, data):
        if self.is_li:
            if self.num_as == 2 and not self.close_li and not self.close_a:
                print "found data",  data
                self.text.append(data)              # *****
        if self.linkurl:
            self.links.append(self.linkurl)
            self.linkurl = ''

    def handle_charref(self, ref):
        self.handle_entityref("#" + ref)

    def handle_entityref(self, ref):
        self.handle_data(self.unescape("&%s;" % ref))

    def get_pages(self):
        return self.pages
'''


def analyze_html(reportHtml):
#    print "Inside analyze_html"

#    print reportHtml.encode("utf-8")
#    print reportHtml
#    print reportHtml.decode('utf-8')

    report = dict()

    soup = BeautifulSoup(reportHtml, "html.parser")

#    parser = out_link_parser()
#    parser.feed(reportHtml.decode('utf-8'))

#    dataList = parser.dataList
#    url = parser.links[0]
#    url = soup.a.link
    
    link = soup.find('a')
    
    url = link["href"]
    
    dataList = []
    
    for string in soup.strings:
#        print string
        dataList.append(string)
 
#    parser.close()

#    for data in dataList:
#        print data

#    print dataList

    myName = dataList[1]
    myFaction = dataList[3]
    myLevel = dataList[5]
    attackedPortal = dataList[7]
    address = dataList[9]

#    parsedLength = len(dataList)
#    print len(dataList)

    if "LINK" in dataList[9]:

#       print dataList
#        for data in dataList:
#            print data

        attackedType = "Link"
        linkedPortal = dataList[10].rstrip(": ")

        i = 12
        while "DAMAGE:" not in dataList[i]:
            i += 2
        else:
#            print dataList[i]
#            print i
            address = dataList[i-1]
            attacker = dataList[i+2]
            if "uncaptured" in dataList[i+8]:
                owner = ""
            else:
                owner = dataList[i+9]

    elif "Mod" in dataList[13]:
        attackedType = "ResonatorAndMod"
        linkedPortal = ""
        address = dataList[8]
        attacker = dataList[11]
        if "uncaptured" in dataList[20]:
            owner = ""
        else:
            owner = dataList[21]

    elif "Resonator" in dataList[10]:
        attackedType = "Resonator"
        linkedPortal = ""
        address = dataList[8]
        attacker = dataList[11]
        if "uncaptured" in dataList[17]:
            owner = ""
        else:
            owner = dataList[18]

    elif "Mod" in dataList[10]:
        attackedType = "Mod"
        linkedPortal = ""
        address = dataList[8]
        attacker = dataList[11]
        if "uncaptured" in dataList[17]:
            owner = ""
        else:
            owner = dataList[18]

    else:
        attackedType = ""
        linkedPortal = ""
        address = ""
        attacker = ""
        owner = ""

#        print dataList

    report["attackedType"] = attackedType
    report["myName"] = myName
    report["attacker"] = attacker
    report["myLevel"] = myLevel
    report["attackedPortal"] = attackedPortal
    report["owner"] = owner
    report["linkedPortal"] = linkedPortal
    report["address"] = address

    latAndLon = url.split('?')[1].split('&')[1].split('=')[1].split(",")
    report["latitude"] = latAndLon[0].encode("utf-8")
    report["longitude"] = latAndLon[1].encode("utf-8")

    return report

def analyze_mail(message):
#    print "inside analyze_mail"

    report = dict()


    for header in message["payload"]["headers"]:
        if header["name"] == "Subject":
            attackAgent = header["value"].split(" ")[6]
        if header["name"] == "Date":
            mailTime = datetime.datetime.strptime(header["value"], "%a, %d %b %Y %H:%M:%S +0000")

    for part in message["payload"]["parts"]:
        for bodyHeader in part["headers"]:
            if bodyHeader["value"] == "quoted-printable":
                reportHtml = base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
#                reportHtml = part["body"]["data"].encode("utf-8")

#    print reportHtml.encode("utf-8")

    report = analyze_html(reportHtml.replace("&#39;","'"))
#    report = analyze_html((reportHtml.replace("&#39;","'")).replace("&",""))
    report["time"] = mailTime.strftime("%Y/%m/%d %H:%M:%S")

#    print report

    return report

def print_csv(report):

    print u'"' + report["time"] + u'"' + u',' + u'"' + report["myName"] + u'"' + u"," + u'"' + report["myLevel"] + u'"' + u"," + u'"' + report["attackedType"] + u'"' + u"," + u'"' + report["attacker"] + u'"' + u"," + u'"' + report["attackedPortal"].replace('"', '""') + u'"' + u"," + u'"' + report["linkedPortal"].replace('"', '""') + u'"' + u"," + u'"' + report["owner"] + u'"' + u"," + u'"' + report["address"].replace('"', '""') + u'"' + u"," + u'"' + report["latitude"] + u'"' + u"," + u'"' + report["longitude"] + u'"'

def main():

    api = GmailApi()

    report = dict()

    user = "me"
#    qstring = "subject:Ingress Damage Report: Entities attacked by"
#    qstring = "subject:Ingress Damage Report: Entities attacked by after:2015/12/30 before:2015/12/31"
#    qstring = "International Lutheran Church subject:Ingress Damage Report: Entities attacked by after:2015/6/1"
#    qstring = "subject:Ingress Damage Report: Entities attacked by after:2016/1/17"
    qstring = "subject:Ingress Damage Report: Entities attacked by after:2015/12/1 before:2016/1/1"
#    qstring = "makige kankisen subject:Ingress Damage Report: Entities attacked by"
#    qstring = "Nakonaki subject:Ingress Damage Report: Entities attacked by"
    number = "100"
#    number = "1"
    token = ""

    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

    while 1:
#    for i in range(0,1):

        list = api.getMailList(user, qstring, number, token)

        messages = list.get('messages', [])

        if not messages:
            print 'No Messages found.'
        else:
            for message in messages:
#                print ""
#                print message['id']

                message = api.getMailBody(user, message['id'])
                report = analyze_mail(message)
                print_csv(report)

        token = list.get('nextPageToken')
        if not token:
            break

if __name__ == '__main__':
    main()
