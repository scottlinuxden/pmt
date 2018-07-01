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
import db_authentication


#------------------------------------------------------------------------------
def pageSetup():
    print '    <SCRIPT TYPE="text/javascript">'
    print '    <!--'
    print '    function popup(mylink, windowname,w,h)'
    print '    {'
    print '    if (! window.focus)return true;'
    print '    var href;'
    print "    if (typeof(mylink) == 'string')"
    print '    href=mylink;'
    print '    else'
    print '    href=mylink.href;'
    print '    LeftPosition=(screen.width)?(screen.width-w)/2:100;'
    print '    TopPosition=(screen.height)?(screen.height-h)/2:100;'
    settings="'width='+ w + ',height='+ h + ',top=' + TopPosition + "
    settings=settings+"',left=' + LeftPosition + ',scrollbars=yes'"
    print "    settings=%s" % settings
    print '    popwindow=window.open(href, windowname, settings);'
    print '    popWindow.focus()'
    print '    return false;'
    print '    }'
    print '    //-->'
    print '    </SCRIPT>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
    db_key = arguments[0]
    originator = arguments[1]
    priv = arguments[4]

    options = '<TD ALIGN=CENTER NOWRAP>'

    java="return execute('edit','%s')" % db_key
    options = options + '<INPUT NAME="edit" type="button" value=" Edit " '
    options = options + 'onClick="%s">' % java

    if priv==1:
        java="return execute('delete', '%s')" % db_key
        options=options+'<INPUT NAME="delete" type="button" value=" Delete " '
        options=options+'onClick="%s">' % java

    java="return execute('view', '%s')" % db_key
    options=options + '<INPUT NAME="view" type="button" value=" View " '
    options=options + 'onClick="%s"></TD>' % java
    return options
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def editFunctionButtons(db_key, menu_name, help_pdf=None, priv=0):
    print '<HR><TABLE><TR>'

    java="return execute('save','%s')" % db_key
    html='<INPUT NAME="save" type="button" value=" Save " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    if priv==1:
        java="return execute('delete','%s')" % db_key
        html='<INPUT NAME="delete" type="button" value=" Delete " '
        html=html+'onClick="%s">' % java
        pmt_utils.tableColumn(html)

    java="return execute('view', '%s')" % db_key
    html='<INPUT NAME="view" type="button" value=" View " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    
    java="return goto_url('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)

    java="return goto_url('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    print '</TR></TABLE>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def emailButton(username,key,menu_name, help_pdf):
    link='/%s-cgi-bin/email.pyc' % db_name
    link=link+'?table=pai&key=%s&username=%s' % (key, username)
    print '<HR><TABLE><TR>'

    java="return goto_url('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    if username!=None:
        java="return popup('%s','Email_Project_Action_Item',600,500)" % link
        html='<input type="button" name="email" value=Email onClick="%s">'%java
        pmt_utils.tableColumn(html)

    java="return goto_url('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR></TABLE>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def query_pai(performDbQuery=0, onLoad=None, queryFields=None):

    status,table_data,db=pageInit("Action Items",formJS=0)

    if status != 'success':
        message= "Can not connect to database.\n%s" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    queryFields,whereFields=pmt_utils.getQueryWhereFields(form,
                                                          table_data,
                                                          'pai')

    if queryFields == None or queryFields == []:
        queryFields = []
        whereFields = None
        queryFields.append('id')
        queryFields.append('gist')
        queryFields.append('assigned_to')

    del_priv=pmt_utils.hasPriv(db,username,'del_pai')
    dbResult, queryStatement = pmt_utils.executeQuery(db,
                                                  table_data,
                                                  'pai',
                                                  queryFields,
                                                  whereFields,
                                                  'query',
                                                  queryItemFunctionsHtml,
                                                  'ORDER by int4(id)',
                                                  ['id','originator'],
                                                  None,None,
                                                  "return execute('query')",
                                                  ["","",del_priv])

    if dbResult['status'] != 'success':
        message="Could not get pai data from db.\n" + dbResult['message']
        exit(message)

    msg= "Last Query Statement: %s\n" % queryStatement
    msg=msg+"%s action items retrieved from db" % `len(dbResult['result'])`
    exit(msg,table_data,db,display_login=0)
#------------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageInit(subHeading=None,formJS=0):
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    if formJS:
        pmt_utils.generate_form_javascript(table_data,'pai','pai_admin',0)
    else:
        pmt_utils.javaScript("pai_admin")
    pmt_utils.title("Project Action Item")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Project Action Item')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("pai_admin",
                        declarations.pmt_info['db_name'],
			"pai_admin",
			"return submitForm(document.pai_admin)")

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				   declarations.pmt_info['browser_password'],
				   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        db=None
	status=dbResult['message']
    else:
         db=dbResult['result']
	 status='success'

    return status,table_data,db
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageEnd(table_data,db):
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"    
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def exit(message,table_data=None,db=None,display_login=1):
    if display_login:
        pmt_utils.usernamePasswordDisplay(username)
    pmt_utils.alertsArea(form, message);

    if username!=None and db!=None:
        create_priv=pmt_utils.hasPriv(db,username,'create_pai')
    else:
        create_priv=0

    url='/%s/html/paisum.html' % db_name
    pmt_utils.queryFunctionButtons(create_priv, url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    
    if table_data!=None and db!=None:
	    pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doEdit():

    status,table_data,db=pageInit('Edit',formJS=1)

    if status != 'success':
        message="Could not connect to the database.\n" + status
        exit(message)


    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
    if status != 'success':
        exit(details)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'pai',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Could not retrieve action item to edit.\n"+dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'pai', result[0])
    pmt_utils.display_form(table_data, 'pai', 1, 'useValues', 1, db)
                    
    pmt_utils.alertsArea(form, "Action item data retrieved successfully");

    listing_url='/%s-cgi-bin/pai_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/pai_intro.html' % (db_name)
    del_priv=pmt_utils.hasPriv(db,username,'del_pai')
    editFunctionButtons(form["key_id"].value, listing_url, help_url ,del_priv)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    

    pageEnd(table_data,db)
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doDelete():
    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])
        
    if dbResult['status'] != 'success':
        onQueryLoad = 'displayWindow("Could not connect to the database")'
        sys.exit()

    db = dbResult['result']

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)

    sqlStatement = "DELETE FROM pai WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message = "Could not delete action item data"
    else:
        message = "Action item data successfully deleted"

    onQueryLoad="return displayWindow('%s')" % message
    db.close()
    query_pai(1)
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doSave():
    saveDueToCreate=0
    status,table_data,db=pageInit('Save',formJS=1)
    
    if status != 'success':
        message="Could not connect to db.\n" + status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)

    if form["key_id"].value == 'create':
        saveDueToCreate=1
        queryResult = pmt_utils.executeSQL(db, "SELECT NEXTVAL('pai_id_seq')")

        form["key_id"].value = `queryResult['result'][0]['nextval']`

    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value, "pai",
                                  " WHERE id = '%s'"%form["key_id"].value,
                                  form)

    if dbResult['status'] != 'success':
        message="Action item could not be saved.\n" + dbResult['message']
        exit(message)

    if saveDueToCreate:
        subject='New PAI #%s has been generated' % (form['key_id'].value)
        msg="PAI #%s has been generated.\n\n" % form["key_id"].value
        msg=msg+"Assigned to: %s\n" % form['assigned_to'].value
        msg=msg+"Problem Description:\n%s" % form['action_required'].value
        msg=msg+"\n\nLog into the Project Action Item tracking tool at "
        msg=msg+"http://www.isrparc.org for further info.\n\n"
        msg=msg+"If you do not wish to be on this mailing list please "
        msg=msg+"send an email requesting removal to cm@isrparc.org.\n"
        pmt_utils.emailList(db,'localhost', 'pai_list', subject, msg)

    table_data = pmt_utils.formToTableData(table_data,'pai',
                                           form, form['key_id'].value)

    pmt_utils.display_form(table_data, 'pai', 1, 'useValues', 1, db)
    pmt_utils.alertsArea(form,"Action item successfully saved")

    # generate function button row
    listing_url= '/%s-cgi-bin/pai_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/paisum.html' % (db_name)
    editFunctionButtons(form["key_id"].value,listing_url,help_url)
            
    # generate hidden fields for form
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db) 
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doCreate():

    status,table_data,db=pageInit('Create',formJS=1)

    if status!='success':
        message="Could not connect to db.\n%s" % status
        exit(message)

    # initialize form data values to zero or blank
    table_data = pmt_utils.init_table_data(table_data,'pai')
    now=time_pkg.current_time_MM_DD_YYYY()
    table_data['pai']['date_created']['value'] = now
    
    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
    if status != 'success':
        exit(details)

    table_data['pai']['id']['display']='hidden'

    pmt_utils.display_form(table_data, 'pai', 1,'useValues',1,db)

    message="Enter information on form and depress Create button"
    pmt_utils.alertsArea(form,message)

    # create functions button row
    listing_url='/%s-cgi-bin/pai_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/pai_intro.html' % (db_name)
    pmt_utils.createFunctionButtons('create',listing_url,help_url )
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
 
    pageEnd(table_data,db)
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doView():

    status,table_data,db=pageInit("View",formJS=1)
    if status != 'success':
        message="Could not connect to db.\n" + dbResult['message']
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'pai',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Unable to get action item.\n" + dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'pai', result[0])
    pmt_utils.display_form(table_data, 'pai', 0)

    listing_url='/%s-cgi-bin/pai_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/paisum.html' % (db_name)
    emailButton(username,form['key_id'].value,listing_url,help_url)
    pageEnd(table_data,db)
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name = declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):

    if form["action"].value == "edit":
        doEdit()
       
    elif form["action"].value == "query":
        query_pai(1)

    elif form["action"].value == "delete":
        doDelete()

    elif form["action"].value == "save":
        doSave()
            
    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()

else:
    query_pai(1)
#------------------------------------------------------------------------------
