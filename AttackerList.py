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

    list = api.getMailList(user, qstring, number, token)

    messages = list.get('messages', [])

    if not messages:
        print 'No Messages found.'
    else:
        print 'Messages exists'
        for message in messages:
            message = api.getMailBody(user, message['id'])


if __name__ == '__main__':
    main()
