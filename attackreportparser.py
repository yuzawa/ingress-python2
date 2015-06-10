#!/usr/bin/env python
# -*- encoding: utf-8 -*-

#import HTMLParser
from HTMLParser import HTMLParser


class AttackReportParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.strings = []

#    def handle_starttag(self, tag, attrs):
#        attrs = dict(attrs) # タプルだと扱いにくいので辞書にする
#        print 'start', tag
#        if 'div' == tag and 'class' in attrs:
#             print '-->', attrs['class']

#    def handle_endtag(self, tag):
#        print 'end', tag

    def handle_data(self, data):
#        print data
        self.strings.append(data)
