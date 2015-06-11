#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

import codecs
import base64
import quopri
import datetime

from gmailapi import GmailApi
from attackreportparser import AttackReportParser

def analyze_html(reportHtml):
    print "Inside analyze_html"

    parser = AttackReportParser()
    parser.feed(reportHtml.decode('utf-8'))
    parser.close()

    print parser.strings

    myName = parser.strings[1]
    myFaction = parser.strings[3]
    myLevel = parser.strings[5]
    attackedPortal = parser.strings[7]
#    attackedTime = onechord.strftime("%Y/%m/%d %H:%M:%S")

    parsedLength = len(parser.strings)
    print parsedLength

    if "LINK" in parser.strings[9]:
        attackedType = "Link"
        linkedPortal = parser.strings[12]
        address = parser.strings[13]
        attacker = parser.strings[14]
        if "uncaptured" in parser.strings[parsedLength-1]:
            owner = ""
        else:
            owner = parser.strings[parsedLength-1]

    elif "Resonator" in parser.strings[15]:
        attackedType = "Resonator and Mod"
        address = parser.strings[10]
        attacker = parser.strings[16]
        if "uncaptured" in parser.strings[20]:
            owner = ""
        else:
            owner = parser.strings[21]

    elif "Resonator" in parser.strings[10]:
        attackedType = "Resonator"
        address = parser.strings[8]
        attacker = parser.strings[11]
        if "uncaptured" in parser.strings[17]:
            owner = ""
        else:
            owner = parser.strings[18]

    elif "Mod" in parser.strings[10]:
        attackedType = "Mod"
        address = parser.strings[8]
        attacker = parser.strings[11]
        if "uncaptured" in parser.strings[17]:
            owner = ""
        else:
            owner = parser.strings[18]

    print attackedType
    print myName
    print attacker
    print myLevel
    print attackedPortal
    print owner




def main():

    api = GmailApi()

    user = "me"
#    qstring = "subject:Ingress Damage Report: Entities attacked by"
#    qstring = "subject:Ingress Damage Report: Entities attacked by after:2014/10/1 before:2014/10/2"
    qstring = "subject:Ingress Damage Report: Entities attacked by after:2015/6/1"
    number = "100"
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
                print ""
                print message['id']
                message = api.getMailBody(user, message['id'])
                for header in message["payload"]["headers"]:
                    if header["name"] == "Subject":
                        attackAgent = header["value"].split(" ")[6]
                    if header["name"] == "Date":
                        mailTime = datetime.datetime.strptime(header["value"], "%a, %d %b %Y %H:%M:%S +0000")
                print ""
                for part in message["payload"]["parts"]:

                    for bodyHeader in part["headers"]:
#                    if bodyHeader["value"] == "base64":
#                        print "Orignal base64"
#                        print part["body"]["data"]
#                        print "now base64 decoding"
#                        print base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
                        if bodyHeader["value"] == "quoted-printable":
                            reportHtml = base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
#                            print reportHtml

                            analyze_html(reportHtml)

        token = list.get('nextPageToken')
        if not token:
            break

if __name__ == '__main__':
    main()
