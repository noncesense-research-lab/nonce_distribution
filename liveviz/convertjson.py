#!/usr/bin/env python3

import csv, json
from sys import argv

try:
    filename = argv[1]
except IndexError:
    print("No input given")
    exit()

try:
    f = open(filename, 'r')
    blockdata = csv.reader(f, delimiter=',')

    timestamp = []
    height = []
    nonce = []
    diff = []

    for row in blockdata:
        #print (row)
        timestamp.append(row[3])
        height.append(row[1])
        nonce.append(row[2])
        diff.append(row[0])

    print ("{")
    print ("\"timestamp\": ")
    print (json.dumps(timestamp))
    print (",")
    print ("\"height\": ")
    print (json.dumps(height))
    print (",")
    print ("\"nonce\": ")
    print (json.dumps(nonce))
    print (",")
    print ("\"diff\": ")
    print (json.dumps(diff))
    print ("}")

except (IOError, OSError) as e:
    print("Could not open file %s -> %s" % (filename,e))
