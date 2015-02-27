#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Update a single ServerAlias from terminal

import os
import re
from netifaces import interfaces, ifaddresses, AF_INET

apacheLoc = '/Applications/MAMP/bin/apache2/bin/apachectl'
fileName = 'httpd-vhosts.conf'
vhostLoc = '/Applications/MAMP/conf/apache/extra/'
defaultName = 'mobileapi.dev'
patternStr = ur'''#\sBBC\sHost\s#\n\s*ServerAlias\s(.*)\n'''
repStr = ur'''# BBC Host #\n   ServerAlias '''


def replaceStringInFile(filePath, host):
    tempName = filePath+'~~~'
    inputFile = open(filePath)
    outputFile = open(tempName,'w')
    fContent = unicode(inputFile.read(), "utf-8")

    outText = re.sub(patternStr, repStr + host + '\n', fContent)

    outputFile.write((outText.encode("utf-8")))

    outputFile.close()
    inputFile.close()

    os.rename(tempName, filePath)

if __name__ == "__main__":
    ips = []
    count = 1

    print(chr(27) + "[2J")
    print 'BBC Virtual Host Updater\n----------------------------------\n'

    print '0. (none) ' + defaultName
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'-'}] )]
        if addresses[0] != '-':
            ips.append(addresses[0])
            print str(count) + '. (%s) %s' % (ifaceName, ', '.join(addresses))
            count += 1

    ip = raw_input("Choose an address: ")

    if str(ip) == '0':
        newip = defaultName
    else:
        newip = ips[int(ip)-1]

    print 'Updating vhost...'
    file = os.path.join(vhostLoc, fileName)
    fileOut = os.path.join(vhostLoc, fileName)
    replaceStringInFile(fileOut, newip)

    print 'Restarting Apache...'
    os.system(apacheLoc + ' restart')

    print 'Successfully set vhost IP to ' + newip
