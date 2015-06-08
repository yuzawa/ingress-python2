#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')

import os
import json

from apiclient.discovery import build
from httplib2 import Http
import oauth2client
from oauth2client import client
from oauth2client import tools

SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

class GmailApi():

    def getMailList(self,user,qu,number,page):

        return self.service.users().messages().list(userId=user,
                                                    q=qu,
                                                    maxResults=number,
                                                    pageToken=page).execute()

    def getMailBody(self,user,id):

        return self.service.users().messages().get(userId=user,id=id).execute()

    def __init__(self):

#        print "temporary"
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'gmail-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path

        self.service = build('gmail', 'v1', http=credentials.authorize(Http()))

"""
class GmailServiceFactory():

    def createService(self, auth_info):
		STORAGE = Storage('gmail.auth.storage')
		credent = STORAGE.get()

		if credent is None or credent.invalid:
                        info = auth_info['installed']
                        flow = OAuth2WebServerFlow(info["client_id"], info["client_secret"], response_setting["scope"],info["redirect_uris"][0])
			auth_url = flow.step1_get_authorize_url()
			webbrowser.open(auth_url)#ブラウザを開いて認証する
			code = raw_input("input code : ")
			credent = flow.step2_exchange(code)
			STORAGE.put(credent)
		http = httplib2.Http()
		http = credent.authorize(http)

		gmail_service = build("gmail", "v1", http = http)
		return gmail_service
"""

"""
def get_credentials():
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials
"""
