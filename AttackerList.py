#!/usr/bin/python
# -*- coding: utf-8 -*-

#import sys
#sys.path.insert(1, '/Library/Python/2.7/site-packages')

from gmailapi import GmailApi

CLIENT_SECRET_FILE = 'client_secret.json'

def main():

    api = GmailApi()

    user = "me"
    qstring = "subject:Ingress Damage Report: Entities attacked by"
    number = "10"
    token = ""

    list = api.getMailList(user, qstring, number, token)

if __name__ == '__main__':
    main()
