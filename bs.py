#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

soup = BeautifulSoup(open("a.html"), "html.parser")
#soup = BeautifulSoup(open("index.html"), "lxml")

link = soup.find('a')
#print link
#print link.string

#print(soup.get_text())

#print soup.strippted_strings
for string in soup.strings:
  print string
#print [text for text in soup.stripped_strings]]]
