#!/usr/bin/env python3

import json

thedict = {}
for line in open('/media/jt/ramdisk/cheesers.txt').readlines():
    #print(line)
    if '-' in line: # if he used a hyphen
        name, description = line.split('-')
        name = ''.join(name.lower().split())
    else: # no hyphen
        if line.startswith('['): # clan name was used
            name = ''.join(line.split()[:2]).lower()
            description = ' '.join(line.split()[2:]) # join the clan name to the actual name and add the description
        else: # no clan name used
            name = line.split()[0].lower()
            description = ' '.join(line.split()[1:])
    description = description.strip()
    if not description:
        description = "cheeses"
    thedict[name] = description

#from pprint import pprint
#pprint(thedict)

open('starcraftplayers.json', 'w').write(json.dumps(thedict))
