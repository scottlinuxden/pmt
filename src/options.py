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
import db_authentication


#------------------------------------------------------------------------------
def verifyUserPass(db):

    status, details = db_authentication.password_valid(db,
						      crypt_salt=db_name,
						      username=username,
						      password=password)
    if status != 'success':
        print "<form method=post>"
        pmt_utils.usernamePasswordDisplay()
        pmt_utils.alertsArea(form, details)
        print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
        print "</form>"
        sys.exit(1)

    if pmt_utils.hasPriv(db, username, 'project_data')!=1:
        print "<form method=post>"
        pmt_utils.usernamePasswordDisplay()
	message='User %s does not have access to view Data Items' % username
        pmt_utils.alertsArea(form, message)
        print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
        print "</form>"
        sys.exit(1)

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def getTableName(db):

    print 'Choose the set of options to manage:<BR>'

    sqlStatement="select tablename from pg_tables where tablename!~'pg_'"
    result=pmt_utils.executeSQL(db,sqlStatement)

    table=''
    if form.has_key('table_name'):
        table=form['table_name'].value

    print '<SELECT NAME=table_name>'
    for i in xrange(len(result['result'])):
        name=result['result'][i]['tablename']
        sql="select count(*) from pg_attribute,pg_class "
	sql=sql+"where pg_attribute.attrelid=pg_class.relfilenode "
	sql=sql+"and pg_class.relname='%s' and attnum>0" % name
        num_cols=pmt_utils.executeSQL(db, sql)
        if num_cols['result'][0]['count']==1:
            if name==table:
                print '<OPTION SELECTED VALUE="%s">%s' % (name,name)
            else:
                print '<OPTION VALUE="%s">%s' % (name,name)
    print '</SELECT>'
    print '<INPUT NAME=submit VALUE="View Options" TYPE=submit>'
    print '<BR><BR>'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def listOptions(db):
    sqlStatement='select * from %s' % form['table_name'].value
    options=pmt_utils.executeSQL(db,sqlStatement)
    key=options['result'][0].keys()[0]

    print "Choose from the following options:<BR>"
    print '<SELECT NAME=to_delete>'
    for i in xrange(len(options['result'])):
        curr=options['result'][i][key]
        print '<OPTION VALUE="%s">%s' % (curr,curr)
    print '</SELECT>'
    print '<INPUT NAME=key VALUE="%s" TYPE=hidden>' % key
    print '<INPUT NAME=delete VALUE="Delete" TYPE=submit>'
    print "<BR><BR>"
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def addPrompt():

    print "Choose the name of an option to add to the selected option set:<BR>"
    print '<INPUT NAME=to_add TYPE=text maxlength=50 VALUE="">'
    print '<INPUT NAME=add TYPE=submit VALUE="Add Option">'
    print "<BR><BR>"
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def addOption(db):
    option=form['to_add'].value
    table=form['table_name'].value
    sqlStatement="insert into %s values ('%s')" % (table,option)
    add=pmt_utils.executeSQL(db, sqlStatement)
    if add['status']!='success':
        message=add['message']
    else:
        message="The option '%s' has been added to %s" % (option,table)
    return message

#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
def deleteOption(db):
    option=form['to_delete'].value
    table=form['table_name'].value
    key=form['key'].value
    sqlStatement="delete from %s where %s='%s'" % (table,key,option)
    delete=pmt_utils.executeSQL(db, sqlStatement)
    if delete['status']!='success':
        message=delete['message']
    else:
        message="The option '%s' has been removed from %s" % (option,table)
    return message


#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

print "<HTML>"
print "<HEAD>"
pmt_utils.title("Edit Project Options")
print "</HEAD>"
pmt_utils.bodySetup()
pmt_utils.mainHeading("Project Option Manager")
pmt_utils.subHeading("Add/Delete Options")

if username!=None:

    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				     declarations.pmt_info['browser_password'],
				     declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        message="Can not connect to database,\n" + dbResult['message']
        pmt_utils.alertsArea(form,message)
        sys.exit()

    db=dbResult['result']

    verifyUserPass(db)

    message=''
    if form.has_key('add'):
        message=addOption(db)

    if form.has_key('delete'):
        message=deleteOption(db)


    print '<FORM METHOD=POST ACTION=/%s-cgi-bin/options.pyc>' % db_name
    getTableName(db)

    if form.has_key('table_name'):
        listOptions(db)

    addPrompt()
    print '</FORM>'

    if message!='':
        pmt_utils.textarea(None, 'alerts', message,'2', '32', None, None)

else:
    print "<form method=post>"
    pmt_utils.usernamePasswordDisplay()
    print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
    print "</form>"

print '</BODY>'
print '</HTML>'
#------------------------------------------------------------------------------
