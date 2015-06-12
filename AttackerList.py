#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

import codecs
import base64
import quopri
import datetime

#from lxml import html
from xml.sax.saxutils import *
from HTMLParser import HTMLParser
from gmailapi import GmailApi

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
        self.dataList.append(data)
        if self.linkurl:
            self.links.append(self.linkurl)
            self.linkurl = ''


def analyze_html(reportHtml):
#    print "Inside analyze_html"

    report = dict()


    parser = out_link_parser()
    parser.feed(reportHtml.decode('utf-8'))

    dataList = parser.dataList
    url = parser.links[0]

    parser.close()

#    print dataList

    myName = dataList[1]
    myFaction = dataList[3]
    myLevel = dataList[5]
    attackedPortal = dataList[7]
    address = dataList[9]

    parsedLength = len(dataList)

    if "LINK" in dataList[9]:
        attackedType = "Link"
        linkedPortal = dataList[12]
        address = dataList[13]
        attacker = dataList[14]
        if "uncaptured" in dataList[parsedLength-1]:
            owner = ""
        else:
            owner = dataList[parsedLength-1]

    elif "Resonator" in dataList[15]:
        attackedType = "Resonator and Mod"
        linkedPortal = ""
        address = dataList[10]
        attacker = dataList[16]
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

        print dataList

    report["attackedType"] = attackedType
    report["myName"] = myName
    report["attacker"] = attacker
    report["myLevel"] = myLevel
    report["attackedPortal"] = attackedPortal
    report["owner"] = owner
    report["linkedPortal"] = linkedPortal
    report["address"] = address

    latAndLon = url.split('?')[1].split('&')[1].split('=')[1].split(",")
    report["latitude"] = latAndLon[0]
    report["longitude"] = latAndLon[1]

    return report

def analyze_mail(message):
#    print "inside analyze_mail"

    for header in message["payload"]["headers"]:
        if header["name"] == "Subject":
            attackAgent = header["value"].split(" ")[6]
        if header["name"] == "Date":
            mailTime = datetime.datetime.strptime(header["value"], "%a, %d %b %Y %H:%M:%S +0000")

    for part in message["payload"]["parts"]:
        for bodyHeader in part["headers"]:
            if bodyHeader["value"] == "quoted-printable":
                reportHtml = base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))

#    report = analyze_html(html.escape(reportHtml))
#    report = analyze_html(escape(reportHtml, {"'": '&lsquo;'}))
#    report = analyze_html(escape(reportHtml))
    report = analyze_html(reportHtml.replace("&#39;","'"))

#    print reportHtml.replace("&#39;","¥'").decode('utf-8')

    print mailTime.strftime("%Y/%m/%d %H:%M:%S"),
    print ',',

    print report["attackedType"],
    print ',',
    print report["myName"],
    print ',',
    print report["attacker"],
    print ',',
    print report["myLevel"],
    print ',',
    print report["attackedPortal"],
    print ',',
    print report["owner"],
    print ',',
    print report["linkedPortal"],
    print ',',
    print report["address"],
    print ',',
    print report["latitude"],
    print ',',
    print report["longitude"],
    print ','



def main():

    api = GmailApi()

    user = "me"
#    qstring = "subject:Ingress Damage Report: Entities attacked by"
#    qstring = "subject:Ingress Damage Report: Entities attacked by after:2014/10/1 before:2014/10/2"
#    qstring = "International Lutheran Church subject:Ingress Damage Report: Entities attacked by after:2015/6/1"
    qstring = "subject:Ingress Damage Report: Entities attacked by after:2015/6/1"
    number = "100"
#    number = "1"
    token = ""

    sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

#    while 1:
    for i in range(0,1):

        list = api.getMailList(user, qstring, number, token)

        messages = list.get('messages', [])

        if not messages:
            print 'No Messages found.'
        else:
            for message in messages:
#                print ""
#                print message['id']

                message = api.getMailBody(user, message['id'])
                analyze_mail(message)

        token = list.get('nextPageToken')
        if not token:
            break

if __name__ == '__main__':
    main()
