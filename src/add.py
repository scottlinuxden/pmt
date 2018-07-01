# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR:
#   Lane LiaBraaten
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com

import os,sys
import pmt_utils
import declarations


def addDirectory(name,location):
    try:
        path="/home/%s/documents/%s/%s" % (db_name,location,name)
        print path
        os.makedirs(path,0700)
    except OSError,details:
        print "Cannot create folder: %s.\n%s\n" % (name,details)
    else:
        print "Folder created"
        print '<form method="POST" >'
        print '<input type="button" value="Close Window" '
        print 'onClick="return closerefresh()">'
        print '</form>'
        sys.exit()

    

pmt_utils.htmlContentType()
print "<HTML>"
print "<HEAD>"
pmt_utils.title("Add Folder")
print '<SCRIPT TYPE="text/javascript">'
print '<!--'

print 'function closerefresh()'
print '{'
print '    if (! (window.focus && window.opener))'
print '        return true;'
print '    window.opener.focus();'
print '    window.close();'
print '    if (opener.top.location != opener.location) {'
print '        opener.location.reload();}'
print '    return false;'
print '}'

print 'function closewin()'
print '{'
print '    if (! (window.focus && window.opener))'
print '        return true;'
print '    window.opener.focus();'
print '    window.close();'
print '    return false;'
print '}'

print '//-->'
print '</SCRIPT>'
print "</HEAD>"
pmt_utils.bodySetup()
form=pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']


if form.has_key('location'):
    if form.has_key('dirname'):
        addDirectory(form['dirname'].value,form['location'].value)

    else:
        print '<FORM ACTION="add.pyc" METHOD="POST">'
        print 'Folder name: '
        print '<INPUT NAME="location" TYPE=hidden '
        print 'VALUE="%s">' % form['location'].value
        print '<INPUT NAME="dirname" TYPE=text>'
        print '<BR>'
        print '<INPUT NAME="submit" TYPE=submit VALUE="Create">'

else:
    print "No folder location specified"

print '<form method="POST" >'
print '<input type="button" value="Close Window" '
print 'onClick="return closewin()">'
print '</form>'


print "</BODY></HTML>"
