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
#

import os, string, sys
import cgi, glob
from pg import DB
import urllib
import os_utils
import pmt_utils
import declarations
import time_pkg
import time
import stat
import file_io
import commands
import  db_authentication
import shutil


#------------------------------------------------------------------------------
def doPopup():

    if not form.has_key('fullpath'):
        sys.exit()
    
    #if os.path.isdir(form['fullpath'].value):
    #    print "Cannot delete directories.  Use Folder Maintenance."
    #    print '<form method="POST" >'
    #    print '<input type="button" value="Close Window" '
    #    print 'onClick="self.close()">'
    #    print '</form>'
    #    sys.exit()


    print "Are you sure you want to delete <br>"
    path,file=os.path.split(form['fullpath'].value)
    if file=='b00kmarkz':
        print "the link to %s?" % form['name'].value
    elif os.path.isdir(form['fullpath'].value):
        index=string.find(form['fullpath'].value,"documents")
        path=form['fullpath'].value[index+10:]
        print "the directory %s (and all its contents)?<BR>" % path
    else:
        index=string.find(form['fullpath'].value,"documents")
        path=form['fullpath'].value[index+10:]
        print path + '?<BR>'

    print '<form method="POST" action=/%s-cgi-bin/delete.pyc>' % db_name
    print '<input type="submit" value="Delete File"> '
    print '<input type="button" value="Cancel" onclick="self.close()">'
    print '<input type=hidden name=project value="%s">' % form['project'].value
    print '<input type=hidden name=fullpath value="%s">'%form['fullpath'].value
    if file=='b00kmarkz':
        print '<input type=hidden name=id value="%s">' % form['id'].value
        print '<input type=hidden name=name value="%s">' % form['name'].value
    print '<input type=hidden name=popup value="0">'
    print '</form>'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def doDelete():

    if os.path.isdir(form['fullpath'].value):
        # Handle directories
        #status,output=os_utils.super_remove(form['fullpath'].value)
        #if status=='error':
        #    print "Unable to delete directory"
        #else:
        try:
            os.rmdir(form['fullpath'].value)
        except:
            print "Cannot remove directory (make sure it is empty first)<BR>"
            print '<form method="POST" >'
            print '<input type="button" value="Close Window" '
            print 'onClick="return closerefresh()">'
            print '</form>'
            return
        else:
            print "The directory has been deleted.<BR>"
        htmlfile=form['fullpath'].value+'.html'
        permfile=form['fullpath'].value+'.perm'
        if os.path.exists(htmlfile):
            try:
                os.remove(htmlfile)
            except:
                print "Unable to delete details file.<BR>"
        if os.path.exists(permfile):
            try:
                os.remove(permfile)
            except:
                print "Unable to delete permissions file.<BR>"

    else:
        # Handle files
        path,file=os.path.split(form['fullpath'].value)
        if string.count(file,".") > 1:
            file = string.replace(file,".","_")

        if file=="b00kmarkz":
            filepathname=form['fullpath'].value
            #os.system('cp %s %s.backup' % (filepathname,filepathname))
            shutil.copy(filepathname,'%s.backup' % (filepathname))
            backup=open('%s.backup' % form['fullpath'].value, 'r')
            bookmarks=open('%s' % form['fullpath'].value, 'w')
            lines=backup.readlines()
            for line in lines:
                words=string.split(line)
                if not words[0]==form['id'].value:
                    bookmarks.write(line)

            backup.close()
            bookmarks.close()
            print "The link has been deleted."
        else:
            htmlfile=path+os.sep+file+'.html'
            permfile=path+os.sep+file+'.perm'
            #filename=string.replace(form['fullpath'].value,' ','\ ')
            filename=form['fullpath'].value
            try:
                os.remove(filename)
            except:
                print "Unable to remove file: %s" % filename
            if os.path.exists(htmlfile):
                try:
                    os.remove(htmlfile)
                except:
                    print "Unable to remove details file: %s" % htmlfile
            if os.path.exists(permfile):
                try:
                    os.remove(permfile)
                except:
                    print "Unable to remove permissions file: %s" % permfile
            print "The file has been deleted."


    print '<form method="POST" >'
    print '<input type="button" value="Close Window" '
    print 'onClick="return closerefresh()">'
    print '</form>'

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']

print "<HTML>"
print "<HEAD>"
pmt_utils.title("Remove Document")
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
print '//-->'
print '</SCRIPT>'
print "</HEAD>"
pmt_utils.bodySetup()
#print '<body background="/%s/icons/circ_bg.jpg" text="#000080" '
#print 'link="#000080" alink="#DAA520" vlink="darkmagenta">' % (db_name)
print '<Font Face="SerpentineSansICG,Arial">'

if form.has_key('popup'):
    if form['popup'].value=='1':
        doPopup()
    elif form['popup'].value=='0':
        doDelete()
    else: "No Comprende"
else:
    print "No Comprende"

print '</BODY>'
print '</HTML>'
#------------------------------------------------------------------------------
