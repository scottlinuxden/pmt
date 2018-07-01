# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import os
import sys
import string
import fileinput

#----------------------------------------------------------------------------
def readFromFile(filename):
    try:
        outputFile = open(filename, 'r')
    except IOError, exception_details:
        msg="Can't open file: %s, Reason: %s" % (filename,exception_details[1])
        return('error', msg)
        
    data = outputFile.readlines()
        
    # chop off carriage return from data line if it is there
    for i in xrange(0,len(data)):
        if data[i][-1:] == '\n':
            data[i] = data[i][:-1]
    outputFile.close()
    return ('success', data)
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def writeToFile(filename,data):
    try:
        outputFile = open(filename, 'w')
    except IOError, exception_details:
        msg="Can't open file: %s, Reason: %s" % (filename,exception_details[1])
        return('error', msg)

    for i in xrange(0,len(data)):
        outputFile.write(data[i] + '\n')
    outputFile.close()

    return ('success', None)
#----------------------------------------------------------------------------
