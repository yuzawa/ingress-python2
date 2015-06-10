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
#            print 'Messages exists'
            for message in messages:
                print ""
                print message['id']
                message = api.getMailBody(user, message['id'])
                for header in message["payload"]["headers"]:
                    if header["name"] == "Subject":
#                        print(header["value"].split(" ")[6]),
                        attackAgent = header["value"].split(" ")[6]
                    if header["name"] == "Date":
#                        Tue, 09 Jun 2015 04:00:19
                        mailTime = datetime.datetime.strptime(header["value"], "%a, %d %b %Y %H:%M:%S +0000")
#                        print header["value"],
                print ""
                for part in message["payload"]["parts"]:

#                    print message
                    for bodyHeader in part["headers"]:
#                        if bodyHeader["name"] == "Content-Transfer-Encoding":
#                            print "body header: ",
#                            print bodyHeader["value"]
#                    if bodyHeader["value"] == "base64":
#                        print "Orignal base64"
#                        print part["body"]["data"]
#                        print "now base64 decoding"
#                        print base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
                        if bodyHeader["value"] == "quoted-printable":
#                        print "Orignal quoted-printable"
#                            print part["body"]["data"]
#                        print "now qulted-printable decoding"
                            reportHtml = base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
#                            print reportHtml

                            analyze_html(reportHtml)

                            parser = AttackReportParser()
                            parser.feed(reportHtml.decode('utf-8'))
                            parser.close()

                            print parser.strings

                            if "DAMAGE:" in parser.strings[9]:
                                myName = parser.strings[1]
                                myFaction = parser.strings[3]
                                myLevel = parser.strings[5]
                                attackedPortal = parser.strings[7]
                                address = parser.strings[8]
                                attacker = parser.strings[11]
                                if "uncaptured" in parser.strings[17]:
                                    owner = ""
                                else:
                                    owner = parser.strings[18]

#                            print reportHtml

                damageReport = True

                if damageReport:
                    print mailTime.strftime("%Y/%m/%d %H:%M:%S")
                    print attacker
                    print attackedPortal
                    print address
#                    print owner.replace("Owner: ", "")
                    print owner

        token = list.get('nextPageToken')
        if not token:
#            print "match!"
            break

if __name__ == '__main__':
    main()
