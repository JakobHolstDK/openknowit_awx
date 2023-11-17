#!/usr/bin/env python



import os
import sys
import time
import datetime
import subprocess
import xml.etree.ElementTree as ET


readfile = open('data/quatareport.xml', 'r')
xml = readfile.read()
readfile.close()

root = ET.fromstring(xml)

for child in root:
    print(child.tag, child.attrib)
    for domain in child:
        print(domain.tag, domain.attrib)

#        for user in domain:
#            print(user.tag, user.attrib)
#
#           for quota in user:
#                print(quota.tag, quota.attrib)


