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
import declarations
import pmt_utils
import time
import os
import string
import shutil

form = pmt_utils.getFormData()
pmt_utils.htmlContentType()
db_name=declarations.pmt_info['db_name']


#------------------------------------------------------------------------------
def validate():
    valid='true'

    if form['name'].value=='':
        valid='false'
    if form['target'].value=='':
        valid='false'
    if form['description'].value=='':
        valid='false'

    return valid
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def showForm():

    print '<center><h2>Add new link:</h2>'
    print '<form method=post action=/%s-cgi-bin/addlink.pyc>' % db_name
    print '<input type=hidden name=dest value=%s>' % form['dest'].value
    print '<TABLE BORDER=0>'

    # display the name of the data item
    print "<TR><TD><B>Data Item Name</B>:</TD><TD>"
    pmt_utils.textbox(None, 'name', '', '30', '40', None, None)
    print "</TD></TR>"

    # display date entered and href of target
    print "<TR><TD><B>Target</B>:</TD><TD>"
    pmt_utils.textbox(None, 'target', '', '30', '256', None, None)
    print "</TD></TR>"

    # display the description field
    print "<TR><TD><B>Description:</B></TD><TD>"
    pmt_utils.textarea(None, 'description', '', '5', '25', None, None)
    print '</TABLE>'
    print '<input name="submit" type="submit" value="Add Link">'
    print '<input name="Close Window" type="button" ' + \
          'value="Close Window" onClick=self.close()'
    print '</form>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def addLink():

    date=time.strftime('%m/%d/%y',time.localtime(time.time()))

    description=string.replace(form['description'].value,'\n',' ')
    description=string.replace(description,'\r',' ')

    abs_filename="/home/%s/documents/%s/b00kmarkz"%(db_name,form['dest'].value)

    if os.path.exists(abs_filename):
        shutil.copy(abs_filename,'%s.backup' % (abs_filename))
        #os.system('cp %s %s.backup' % (abs_filename,abs_filename))
        backup=open('%s.backup' % abs_filename,'r')
        bookmarks=open(abs_filename,'w')

        # find largest index so far
        lines=backup.readlines()
        max=0;
        for line in lines:
            words=string.split(line)
            if int(words[0])>max:
                max=int(words[0])

	newline='%d | %s |'    % (max+1,form['name'].value)
	newline='%s %s |'      % (newline,form['target'].value)
	newline='%s %s | %s\n' % (newline,date,description)

        for line in lines:
            bookmarks.write(line)
        bookmarks.write(newline)
        backup.close()
	
    else:
        bookmarks=open(abs_filename,'w')
	newline='1 | %s |'    % (form['name'].value)
	newline='%s %s |'      % (newline,form['target'].value)
	newline='%s %s | %s\n' % (newline,date,description)
        bookmarks.write(newline)

    bookmarks.close()

    print '<CENTER><B><FONT COLOR="#000099">Data Item Details Page</FONT>'
    print '</B><HR SIZE=1 NOSHADE WIDTH=100%>'

    print '<TABLE border=0 align=center>'
    print '<TR><TD><B>Name:</B></TD><TD> %s <BR>' % (form['name'].value)
    print '<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % (date)
    print '<TR><TD><B>Target:</B></TD><TD> %s <BR>' %(form['target'].value)
    print '<TR><TD><B>Description:</B></TD><TD> '
    print '%s <BR>' % (form['description'].value)
    print '</TABLE>'

    print '<HR><form method="POST" >'
    print '<input type="button" value="Close Window" '
    print 'onClick="return closerefresh()">'
    print '</form>'
    print '</CENTER>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
print '<html>'
print '<head>'
print '<title>Add Link to Data Items</title>'
print '<SCRIPT TYPE="text/javascript">'
#pmt_utils.title("Edit Document Details")
print '<!--'
print 'function closerefresh()'
print '{'
print '    if (! (window.focus && window.opener))return true;'
print '    window.opener.focus();'
print '    window.close();'
print '    if (opener.top.location != opener.location) {'
print '    opener.location.reload();}'
print '    return false;'
print '}'
print '//-->'
print '</SCRIPT>'
print '</head>'
pmt_utils.bodySetup()

if form.has_key('dest') and not form.has_key('name'):
    showForm()
if form.has_key('name'):
    if validate()=='true':
        addLink()
        to_addr="%s_uploads@isrparc.org" % db_name
        msg='The link "%s" has been uploaded' % (form['name'].value)
        msg=msg+' to the %s site.' % (db_name)
        pmt_utils.send_email('localhost',
			     'web_user@isrparc.org',
			     [to_addr],
			     'Link uploaded',
			     msg)
    else:
        showForm()
        print '<br><font color=red>'
        print '<b>All fields are required.</b></font>'

print '</body></html>'
#------------------------------------------------------------------------------
