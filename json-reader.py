#!/usr/bin/python3
import json

bugs_file_name = 'bugs.txt'

bugs = {}

try: 
    bugs = json.load(open(bugs_file_name))
except:
    print("Could not read %s" % bugs_file_name)

print("Loaded %i bugs" % (len(bugs)))
