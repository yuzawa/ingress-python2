#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import string
import re
import csv

#for line in sys.stdin:
#    print line

param = sys.argv
f = open(param[1], 'r')
    
reader = csv.reader(f)
for row in reader:

    sql = "INSERT INTO Report( ReportDate, OwnerName, OwnerLevel, DamagedType, AttackerName, AttackedPortal, LinkedPortal, PortalOwner, PortalAddress, Latitude, Longitude ) VALUES ("

    length = len(row)
    i = 1

    for word in row:
        
        sql = sql + "'" + word.replace("'", "''") + "'"
        if i != length:
            sql += ","
        i += 1
    sql.rstrip(' ')
    sql += ");"
    print sql
f.close
    