#-*- Mode: Python; tab-width: 4 -*-
# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   R. Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import os, string, sys
import cgi, glob
from pg import DB
import pmt_utils
import declarations
import time_pkg
import file_io
import urllib
import db_authentication


#----------------------------------------------------------------------------
def queryFunctionButtons(loginOk=1, help_pdf=None):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    java="return execute('query')"
    html='<INPUT NAME="query" type="button" value=" Query " onClick="%s">'%java
    pmt_utils.tableColumn(html)

    if loginOk:
        java="return execute('csv')"
        html='<INPUT NAME="csv" type="button" '
        html=html+'value=" Export " onClick="%s">' % java
        pmt_utils.tableColumn(html)

    java="return goto_url('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    print '</TR>'
    print '</TABLE>'
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
    db_key = arguments[0]
    member_username = arguments[1]
    login_username = arguments[2]

    options = '<TD ALIGN=CENTER NOWRAP>'

    # Allow the user to edit their own user information
    if member_username == login_username:
        options=options+ '<INPUT NAME="edit" type="button" value=" Edit " '
        options=options+ '''onClick="return execute('edit','%s')">''' % db_key

    options=options+ '<INPUT NAME="view" type="button" value=" View " '
    options=options+ '''onClick="return execute('view','%s')"></TD>''' % db_key

    return options
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def editFunctionButtons(db_key, menu_name, help_pdf):

    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    java="return execute('save','%s')" % db_key
    html='<INPUT NAME="save" type="button" value=" Save " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    java="return execute('view','%s')" % db_key
    html='<INPUT NAME="view" type="button" value=" View " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    java="return goto_url('%s')" % menu_name
    html='<INPUT NAME="return_to_menu" TYPE="button" '
    html=html+'VALUE=" Listing " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    java="return goto_url('%s')" % help_pdf
    html='<INPUT NAME="help" TYPE="button" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    
    print '</TR>'
    print '</TABLE>'
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def query_project_members(performDbQuery=0, onLoad=None, queryFields=None):

    status,table_data,db=pageInit('Members',formJS=0)

    if username==None:
        message="Unable to identify user."
        exit(message)

    if status != 'success':
        message="Can not connect to database.\n" + dbResult['message']
        exit(message)

    status,details=db_authentication.password_valid(db,crypt_salt=db_name,
                                                    username=username,
                                                    password=password)

    if status != 'success':
        exit(details)

    queryFields,whereFields=pmt_utils.getQueryWhereFields(form,
                                                          table_data,
                                                          'project_members')

    if queryFields == None or queryFields == []:
        queryFields = []
        whereFields = None
        queryFields.append('first_name')
        queryFields.append('last_name')
        queryFields.append('email')
        queryFields.append('phone_number_voice')
        queryFields.append('phone_extension')

    dbResult,queryStatement=pmt_utils.executeQuery(db,
                                                   table_data,
                                                   'project_members',
                                                   queryFields,
                                                   whereFields,
                                                   'query',
                                                   queryItemFunctionsHtml,
                                                   'ORDER by last_name',
                                                   ['id','member_username'],
                                                   None,
                                                   ['member_password'],
                                                   "return execute('query')",
                                                   [username])

    if dbResult['status'] != 'success':
        message="Couldn't get user data from db.\n" + dbResult['message']
        exit(message)

    pmt_utils.alertsArea(form,
                         "Last Query Statement: "+queryStatement+\
                         "\n" + `len(dbResult['result'])` +\
                         " project members retrieved from db")
                
    queryFunctionButtons(1, '/%s/html/contactsum.html' % (db_name))

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pageEnd(table_data,db)
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def pageInit(subHeading=None,formJS=0):
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    if formJS:
        pmt_utils.generate_form_javascript(table_data,'project_members',
                                           'contact_list',0)
    else:
        pmt_utils.javaScript("contact_list")
    pmt_utils.title("Contact List")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Contact List')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("contact_list",
                        db_name,
                        "contact_list",
                        "return submitForm(document.contact_list)")

    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        db=None
        status=dbResult['message']
    else:
        db=dbResult['result']
        status='success'

    return status, table_data, db
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def pageEnd(table_data,db):
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"    
#----------------------------------------------------------------------------



#----------------------------------------------------------------------------
def exit(message):
    pmt_utils.usernamePasswordDisplay()
    pmt_utils.alertsArea(form, message);
    queryFunctionButtons(0, '/%s/html/contactsum.html' % (db_name))
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    sys.exit()
#----------------------------------------------------------------------------




#----------------------------------------------------------------------------
def doCsv():

    # Setup the javascript and html, connect to the db
    subHeading='Address Book (Palm Desktop Import File)'
    status, table_data, db = pageInit(subHeading,formJS=0)

    if status != 'success':
        message="Couldn't connect to db.\n%s" % (status)
        exit(message)

    # Get project member contact info 
    sql="SELECT first_name, last_name, email, company_name, "
    sql=sql+"address_line_1, address_line_2, city, state, zip, "
    sql=sql+"phone_number_voice, phone_extension, "
    sql=sql+"cell_phone_number, phone_number_fax "
    sql=sql+"from project_members ORDER by last_name, first_name"
    queryResult = pmt_utils.executeSQL(db, sql)

    if queryResult["status"] != 'success':
        message="Query failed.\n" + dbResult['message']
        exit(message)

    result = queryResult['result']

    # Display a link to the file and a listing of the data itself
    url='/%s/html/%s' % (urllib.quote(db_name),'address_book.dat')
    print '<BR><BR><a href="%s">' % url
    print 'Palm Desktop Address Book Import File '
    print '(Right Click Here and select '
    print '&quot;Save Link As&quot; to download)</a>'
                
    print '<BR><BR><B>You should configure Palm Desktop Tools '
    print 'to import the Address Book with a comma used as the '
    print 'field deliminter and with the following order of the '
    print 'fields for each address entry:</B>'
                
    print '<TABLE BORDER>'
    print '<TR><TD>First Name</TD><TD>Last Name</TD>'
    print '<TD>Company Name</TD><TD>Address</TD><TD>City</TD>'
    print '<TD>State</TD><TD>Zip Code</TD><TD>Work</TD>'
    print '<TD>Fax</TD><TD>Mobile</TD><TD>E-Mail</TD></TR></TABLE>'
    print '<BR><B>The contents of this Address Book '
    print 'Import file follows:</B>'
    print '<PRE>'

    output_lines = []
    for i in xrange(0, len(result)):
        if string.strip(result[i]['phone_extension']) != '':
            ext = ' x' + result[i]['phone_extension']
        else:
            ext = ''
        if string.strip(result[i]['address_line_1']) != '':
            address = result[i]['address_line_1']
            if string.strip(result[i]['address_line_2']) != '':
                address=address + ' ' + result[i]['address_line_2']
        else:
            address = ''

        outline=          result[i]['first_name'] + ','
        outline=outline + result[i]['last_name'] + ','
        outline=outline + result[i]['company_name'] + ','
        outline=outline + address + ','
        outline=outline + result[i]['city'] + ','
        outline=outline + result[i]['state'] + ','
        outline=outline + result[i]['zip'] + ','
        outline=outline + result[i]['phone_number_voice'] +ext+ ','
        outline=outline + result[i]['phone_number_fax'] + ','
        outline=outline + result[i]['cell_phone_number'] + ','
        outline=outline + result[i]['email']
        print outline
        output_lines.append(outline)

    # Write the contact data to a file
    output_filename='/home/%s/html/address_book.dat' % db_name
    file_io.writeToFile(output_filename,output_lines)
    print '</PRE>'

    # Add buttons, hidden html form data, and company info
    queryFunctionButtons(0, '/%s/html/contactsum.html' % (db_name))
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def doView():
    status, table_data, db = pageInit('View',formJS=1)

    if status!='success':
        message="Could not connect to db.\n%s" % (status)
        exit(message)

    # Get user data from db
    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                         'project_members',
                                                         form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Unable to get member data from db.\n" + dbResult['message']
        exit(message)

    # Display user data
    result = dbResult['result']
    table_data=pmt_utils.dbToTableData(table_data,'project_members',result[0])
    table_data['project_members']['member_username']['display']='read-only'
    table_data['project_members']['member_role']['display'] = 'read-only'
    table_data['project_members']['member_password']['display'] = 'Hidden'
    pmt_utils.display_form(table_data, 'project_members', editable=0)

    # Add buttons, and company info
    url='/%s-cgi-bin/contact_list.pyc?performDbQuery=1' % db_name
    pmt_utils.viewFunctionButtons(url,'/%s/html/contactsum.html' % (db_name))
    pageEnd(table_data,db)
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def doEdit():
    status,table_data,db=pageInit('Edit',formJS=0)
        
    if status!='success':
        message="Could not connect to db.\n%s" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'project_members',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Unable to get member data from db.\n"+dbResult['message']
        exit(message)

    result = dbResult['result']

    table_data = pmt_utils.dbToTableData(table_data,
                                         'project_members',
                                         result[0])

    table_data['project_members']['member_username']['display']='read-only'
    table_data['project_members']['member_password']['display'] = 'Hidden'
    table_data['project_members']['member_role']['display'] = 'read-only'
                
    pmt_utils.display_form(table_data,
                           'project_members', 1,
                           'useValues', 1, db)
    pmt_utils.alertsArea(form,"Member data retrieved successfully")

    listing_url='/%s-cgi-bin/contact_list.pyc?performDbQuery=1' % db_name
    help_url='/%s/html/contactsum.html' % (db_name)
    editFunctionButtons(form['key_id'].value,listing_url,help_url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pageEnd(table_data,db)
#----------------------------------------------------------------------------


#----------------------------------------------------------------------------
def doSave():

    status,table_data,db=pageInit('Save',formJS=0)

    if status != 'success':
        message="Could not connect to db.\n" + status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    # save the Form
    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value,
                                  "project_members",
                                  " WHERE id = '%s'" % form["key_id"].value,
                                  form)

    if dbResult['status'] != 'success':
        message="Save error.\n" + dbResult['message']
        exit(message)

    table_data = pmt_utils.formToTableData(table_data,
                                           'project_members',
                                           form,
                                           form['key_id'].value)

    table_data['project_members']['member_username']['display']='read-only'
    table_data['project_members']['member_role']['display'] = 'read-only'
    table_data['project_members']['member_password']['display'] = 'Hidden'

    pmt_utils.display_form(table_data,'project_members', 1,'useValues', 1, db)

    pmt_utils.alertsArea(form,"Member data successfully saved")

    # generate function button row
    listing_url='/%s-cgi-bin/contact_list.pyc?performDbQuery=1' % db_name
    help_url='/%s/html/contactsum.html' % (db_name)
    editFunctionButtons(form["key_id"].value,listing_url,help_url)
            
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pageEnd(table_data,db)
#----------------------------------------------------------------------------



#----------------------------------------------------------------------------
pmt_utils.htmlContentType()

form = pmt_utils.getFormData()
db_name = declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):

    if form["action"].value == "query":
        query_project_members(1)

    elif form["action"].value == "csv":
        doCsv()

    elif form["action"].value == "view":
        doView()

    elif form["action"].value == "edit":
        doEdit()

    elif form["action"].value == "save":
        doSave()

else:
    query_project_members(1)
