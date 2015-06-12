#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

import codecs
import base64
import quopri
import datetime
#import HTMLParser

from HTMLParser import HTMLParser
from gmailapi import GmailApi

#from attackreportparser import AttackReportParser
#from out_link_parser import AttackReportParser

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
    print "Inside analyze_html"

    report = dict()

    mailData = []

#    parser = AttackReportParser()
    parser = out_link_parser()
#    parser = HTMLParser()
    parser.feed(reportHtml.decode('utf-8'))

    print parser.dataList
    print parser.links

    parser.close()


#    print parser.strings

#    myName = parser.strings[1]
#    myFaction = parser.strings[3]
#    myLevel = parser.strings[5]
#    attackedPortal = parser.strings[7]
#    attackedTime = onechord.strftime("%Y/%m/%d %H:%M:%S")

#    parsedLength = len(parser.strings)
#    print parsedLength

    return report

def analyze_mail(message):
#    print "inside analyze_mail"

    for header in message["payload"]["headers"]:
        if header["name"] == "Subject":
            attackAgent = header["value"].split(" ")[6]
        if header["name"] == "Date":
            mailTime = datetime.datetime.strptime(header["value"], "%a, %d %b %Y %H:%M:%S +0000")
#    print ""
    for part in message["payload"]["parts"]:
        for bodyHeader in part["headers"]:
    #                    if bodyHeader["value"] == "base64":
    #                        print "Orignal base64"
    #                        print part["body"]["data"]
    #                        print "now base64 decoding"
    #                        print base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
            if bodyHeader["value"] == "quoted-printable":
                reportHtml = base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))


    report = analyze_html(reportHtml)



def main():

    api = GmailApi()

    user = "me"
#    qstring = "subject:Ingress Damage Report: Entities attacked by"
#    qstring = "subject:Ingress Damage Report: Entities attacked by after:2014/10/1 before:2014/10/2"
    qstring = "subject:Ingress Damage Report: Entities attacked by after:2015/6/1"
    number = "1"
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
