#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

from gmailapi import GmailApi

def main():

    api = GmailApi()

    user = "me"
    qstring = "subject:Ingress Damage Report: Entities attacked by"
    number = "10"
    token = ""

    while 1:
#    for i in range(0,1):

#        print ""
#        print 'token: ',
#        print token

        list = api.getMailList(user, qstring, number, token)

        messages = list.get('messages', [])

        if not messages:
            print 'No Messages found.'
        else:
#            print 'Messages exists'
            for message in messages:
                message = api.getMailBody(user, message['id'])
                print(message["snippet"].split(":")[3].split(" ")[3]),
#                print(message["snippet"]),
                print(','),

#                print(message["payload"]["headers"][16]["value"].split(" ")[6]),
#                print(','),
#                print(message["payload"]["headers"][15]["value"])
#                print(message["snippet"])
                for header in message["payload"]["headers"]:
                    if header["name"] == "Subject":
                        print(header["value"].split(" ")[6]),
#                    if header["name"] == "Date":
#                        print header["value"],
                print ""

        token = list.get('nextPageToken')
#        print ""

#        print ""
#        print "token at end: ",
#        print token
        if not token:
#            print "match!"
            break

if __name__ == '__main__':
    main()
