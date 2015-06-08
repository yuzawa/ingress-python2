#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

from gmailapi import GmailApi

import base64
import quopri

def main():

    api = GmailApi()

    user = "me"
    qstring = "subject:Ingress Damage Report: Entities attacked by"
    number = "3"
    token = ""

#    while 1:
    for i in range(0,1):

        list = api.getMailList(user, qstring, number, token)

        messages = list.get('messages', [])

        if not messages:
            print 'No Messages found.'
        else:
#            print 'Messages exists'
            for message in messages:
                print message['id']
                message = api.getMailBody(user, message['id'])
                for header in message["payload"]["headers"]:
                    if header["name"] == "Subject":
                        print(header["value"].split(" ")[6]),
                    if header["name"] == "Date":
                        print header["value"],
                print ""

                for part in message["payload"]["parts"]:
                    for bodyHeader in part["headers"]:
                        if bodyHeader["name"] == "Content-Transfer-Encoding":
                            print "body header: ",
                            print bodyHeader["value"]
                    if bodyHeader["value"] == "base64":
#                        print "Orignal base64"
#                        print part["body"]["data"]
#                        print "now base64 decoding"
                        print base64.urlsafe_b64decode(part["body"]["data"].encode("utf-8"))
#                    if bodyHeader["value"] == "quoted-printable":
#                        print "Orignal quoted-printable"
#                        print part["body"]["data"]
#                        print "now qulted-printable decoding"
#                        print quopri.decodestring(part["body"]["data"])


        token = list.get('nextPageToken')
        if not token:
#            print "match!"
            break

if __name__ == '__main__':
    main()
