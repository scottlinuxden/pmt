# $Id: email.py,v 1.3 2005/04/12 16:31:12 lliabraa Exp $
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


#------------------------------------------------------------------------------
def displayEmail(table,data,email):
    print '<form method=post>'
    print '<table>'
    print '<tr><td>To:</td><td><input type=text name=to_box></td>'
    print "<tr><td>From:</td><td>"
    print "<input type=hidden name=from_box value='%s'>%s</td>" % (email,email)
    print '<tr><td>Subject:</td><td><input type=text name=subject></td>'
    print '</table><hr><table>'

    content=''
    table_data=declarations.define_tables()[table]

    # Arrange table_data by display_order
    displayList=[]
    for i in xrange(0,len(table_data)+5):
        displayList.append('')

    for key in table_data.keys():
        index=table_data[key]['display_order']
        displayList[index]=key

    for key in displayList:
        if key=='':
            continue
        content=content+'%s:\t' % table_data[key]['label']
        if not data.has_key(key):
            key=key[:31]
        content=content+'%s\n' % data[key]

    html_content=string.replace(content,'\n','</td><tr><td>')
    html_content=string.replace(html_content,'\t','</td><td>')
    print '<tr><td>'+html_content
    print '</table>'

    print '<input type=hidden name=content value="%s">' % urllib.quote(content)
    print '<input type=hidden name=username value="%s">' % username
    print '<input type=hidden name=table value="%s">' % form['table'].value
    print '<input type=hidden name=key value="%s"><HR>' % form['key'].value

    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    java="return goto_url('%s')" % link
    print '<input type=submit name=send value="Send Email" onClick="%s">'%java
    print '</form>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def sendEmail():

    content=urllib.unquote(form['content'].value)
    if form.has_key('comments'):
        content=form['comments'].value + '\n\n' + content

    for key in form.keys():
        if (key=='to_box' or key=='subject') and form[key].value=='':
            print "Please specify and subject and recipient"
            if form.has_key('table'):
                print '<form method=post>'
                print '<input type=hidden name=table '
                print 'value="%s">' % form['table'].value
                print '<input type=hidden name=key '
                print 'value="%s">' % form['key'].value
            elif form.has_key('project'):
                print '<form method=post>'
                print '<input type=hidden name=project '
                print 'value="%s">' % form['project'].value
                print '<input type=hidden name=fullpath '
                print 'value="%s">' % form['fullpath'].value
                print '<input type=hidden name=name '
                print 'value="%s">' % form['name'].value
            print '<input type=hidden name=username '
            print 'value="%s">' % username

            link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
            print '<HR><input type=submit name=send value="Back" '
            print 'onClick="return goto_url('+"'"+link+"'"+')">'
            print '</form>'
            sys.exit()

    pmt_utils.send_email('localhost',
			 form['from_box'].value,
			 [form['to_box'].value],
			 form['subject'].value,
			 content)

    print 'An email has been sent to %s<hr>' % form['to_box'].value
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def sendDataItem(email):
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.title("Email Data")
    print "</HEAD>"
    pmt_utils.bodySetup(onLoad=None)
    pmt_utils.mainHeading('Send Email')
    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    print '<form method=post action=%s>' % link
    print '<table>'
    print '<tr><td>To:</td><td><input type=text name=to_box></td>'
    print '<tr><td>From:</td><td>'
    print '<input type=hidden name=from_box value="%s">%s</td>' % (email,email)
    print '<tr><td>Subject:</td><td><input type=text name=subject></td>'
    print '<tr><td>Comments:</td><td>'
    pmt_utils.textarea('', 'comments', '', '4', '20', None, None)
    print '</td></table><hr><table>'

    path,filename=os.path.split(form['fullpath'].value)
    index=string.find(path,'documents')
    path=path[index+9:]
    if path=='': path='/'

    
    content="An error has occurred while loading this page."
    if filename=="b00kmarkz":
        abs_filename="/home/%s/documents/%s/b00kmarkz" % (db_name, path)
        bookmarks=open(abs_filename, 'r')
        lines=bookmarks.readlines()
        for line in lines:
            words=string.split(line)
            id=words[0]
            if id==form['id'].value:
                i=3
                while words[i]!='|':
                    i=i+1

                href=words[i+1]
                content='The data item can be accessed from %s' % href
        bookmarks.close()
    else:
        content='The data item %s can be accessed from:\n' % form['name'].value
        content=content+'/%s-cgi-bin/list_docs.pyc' % form['project'].value
        content=content+'?project_name=%s' % form['project'].value
        content=content+'&directory=%s' % path

    htmlContent=string.replace(content,'\n','<br>')
    print htmlContent

    print '<input type=hidden name=content value="%s">' % urllib.quote(content)
    print '<input type=hidden name=username '
    print 'value="%s">' % username
    print '<input type=hidden name=project value="%s">' % form['project'].value
    print '<input type=hidden name=fullpath '
    print 'value="%s">' % form['fullpath'].value
    print '<input type=hidden name=name value="%s">' % form['name'].value

    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    print '<HR><input type=submit name=send value="Send Email" '
    print 'onClick="return goto_url('+"'"+link+"'"+')">'
    print '</form>'

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key('to_box'):
    #from email.py: send email
    pmt_utils.bodySetup(onLoad=None)
    sendEmail()

elif form.has_key('key') and form.has_key('table'):
    # from ecp,pai,spr: get recipient and subject

    table_data = declarations.define_tables()

    print "<HTML>"
    print "<HEAD>"
    pmt_utils.title("Email Data")
    print "</HEAD>"
    pmt_utils.bodySetup(onLoad=None)
    pmt_utils.mainHeading('Send Email')
    print '<hr>'

    db = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
			     declarations.pmt_info['browser_password'],
			     declarations.pmt_info['db_name'])
    if db['status']!='success':
        print "Cannot connect to database"
        sys.exit
    else:
        db=db['result']

    sql="select email from project_members "
    sql=sql+"where member_username='%s'" % username

    email=pmt_utils.executeSQL(db, sql)

    sql="select * from %s " % form['table'].value
    sql=sql+"where id='%s'" % form['key'].value
    data=pmt_utils.executeSQL(db, sql)

    displayEmail(form['table'].value,
		 data['result'][0],
		 email['result'][0]['email'])

elif form.has_key('project') and form.has_key('fullpath'):
    # from list_docs.py: get recipient, subject, and content
    db = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
			     declarations.pmt_info['browser_password'],
			     declarations.pmt_info['db_name'])
    
    if db['status']!='success':
        print "Cannot connect to database"
        sys.exit
    else:
        db=db['result']

    sql="select email from project_members "
    sql=sql+"where member_username='%s'" % username
    email=pmt_utils.executeSQL(db, sql)

    sendDataItem(email['result'][0]['email'])
else:
    print "No Comprende<HR>"

print '<form method="POST"'
print '<input type="button" value="Close Window" onClick="self.close()">'
print '</form>'
print '</body></html>'

#------------------------------------------------------------------------------
