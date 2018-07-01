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
import commands
import authentication


#------------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
    db_key = arguments[0]

    output='<TD ALIGN=CENTER NOWRAP>'
    output=output+'<INPUT NAME="edit" type="button" value=" Edit "' + \
           'onClick="return execute(' + "'edit'" + ", '" +db_key+ "'" + ')">'
    output=output+'<INPUT NAME="delete" type="button" value=" Delete "' + \
           'onClick="return execute(' + "'delete'" + ", '" +db_key+ "'" + ')">'
    output=output+'<INPUT NAME="view" type="button" value=" View "' + \
           'onClick="return execute(' + "'view'" + ", '" +db_key+ "'" + ')">'
    return output
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def query_project_members(performDbQuery=0,onLoad=None,queryFields=None):

    status,table_data,db=pageInit('Members',formJS=0)
    if status != 'success':
        message='Could not connect to database.\n%s' % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
    if status != 'success':
        exit(details)

    # Check for user admin privileges
    if pmt_utils.hasPriv(db, username,'user_admin')!=1:
        message='User %s does not have user admin privileges.' % username
        exit(message)

    queryFields,whereFields=pmt_utils.getQueryWhereFields(form,
                                                          table_data,
                                                          'project_members')

    if queryFields == None or queryFields == []:
        queryFields = []
        whereFields = None
        queryFields.append('first_name')
        queryFields.append('last_name')
        queryFields.append('phone_number_voice')

    dbResult,queryStatement=pmt_utils.executeQuery(db,
                                                   table_data,
                                                   'project_members',
                                                   queryFields,
                                                   whereFields,
                                                   'query',
                                                   queryItemFunctionsHtml,
                                                   'ORDER by last_name',
                                                   ['id'],
                                                   None,None,
                                                   "return execute('query')",
                                                   ["",""])
    if dbResult['status'] != 'success':
        message="Could not get member data from db.\n%s" % dbResult['message']
        exit(message)
    msg="Last Query Statement: %s\n" % queryStatement
    msg=msg+"%s project members retrieved from db" % `len(dbResult['result'])`
    pmt_utils.alertsArea(form,msg)

    # Add buttons and hidden fields
    help_url='/%s/html/contactsum.html' % db_name
    pmt_utils.queryFunctionButtons(1,help_url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def displayPriviledges(priv_data={},table_data={}):
    displayList=[]
    for key in table_data['priviledges'].keys():
        if (not priv_data.has_key(key)) and (key!='member_username'):
           priv_data[key] = table_data['priviledges'][key]['default']

    # Put everything in order by display_order field
    for i in xrange(0,len(table_data['priviledges'])):
        data={'key':'','label':'','priv':''}
        displayList.append(data)
    for key in priv_data.keys():
        order=table_data['priviledges'][key]['display_order']-1
        data={'key':key,
              'label':table_data['priviledges'][key]['label'],
              'priv':priv_data[key]}
        displayList[order]=data

    # List the provileges with Yes/No option menus
    print '<br><br>'
    pmt_utils.subHeading('User Priviledges')
    print "<br><table>"
    for i in xrange(0,len(displayList)):
        if displayList[i]['label']=='Username'\
        or displayList[i]['label']=='':
            continue
        text=displayList[i]['label']
        print '<tr><td ALIGN=LEFT NOWRAP>'
        print '<font FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">'
        print '%s:</font></td>' % text
        print '<td ALIGN=LEFT NOWRAP>'
        print '<font FACE="Arial,Helvetica" SIZE="-1">'
        print '<select NAME="%s" SIZE=1>' % displayList[i]['key']
        if displayList[i]['priv']=='t':
            print '<option SELECTED>Yes'
            print '<option >No'
        else:
            print '<option >Yes'
            print '<option SELECTED>No'

        print '</select></font></td>'
    print "</table>"
#------------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageInit(subHeading=None,formJS=0):
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    if formJS:
        pmt_utils.generate_form_javascript(table_data,'project_members',
                                           'project_members_admin',0)
    else:
        pmt_utils.javaScript("project_members_admin")
    pmt_utils.title("Project Members")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Project Members')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("project_members_admin",
                        declarations.pmt_info['db_name'],
                        "project_members_admin",
                        "return submitForm(document.project_members_admin)")

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
def exit(message,table_data=None,db=None):
    pmt_utils.usernamePasswordDisplay(username)
    pmt_utils.alertsArea(form, message);

    if username!=None and db!=None:
        create_priv=pmt_utils.hasPriv(db,username,'user_admin')
    else:
        create_priv=0

    url='/%s/html/contactsum.html' % db_name
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

    status,table_data,db = pageInit('Edit',formJS=1)
    
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
        message="Could not get project member data.\n%s" % dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data=pmt_utils.dbToTableData(table_data,'project_members',result[0])
    pmt_utils.display_form(table_data,'project_members', 1,'useValues', 1, db)

    # get user privileges and display them
    sqlStatement = "select * from priviledges where " +\
                   "member_username='%s'" % (result[0]['member_username'])
    dbResult = pmt_utils.executeSQL(db, sqlStatement)
    if dbResult['status'] != 'success':
        message="Could not get privileges from db.\n%s" % dbResult['message']
        exit(message,table_data,db)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data,'priviledges', result[0])
    displayPriviledges(result[0], table_data)
    pmt_utils.alertsArea(form,"Project member data retrieved successfully")

    listing_url= '/%s-cgi-bin/project_members_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/contactsum.html' % db_name
    pmt_utils.editFunctionButtons(form["key_id"].value,listing_url,help_url)
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doDelete():

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        message='Could not connect to the database.\n%s' % dbResult['message']
        onQueryLoad = "displayWindow('%s')" % message
        exit(message)

    db = dbResult['result']

    sql = "SELECT member_username FROM project_members "
    sql=sql+"WHERE id = '%s'" % (form['key_id'].value)
    dbResult = pmt_utils.executeSQL(db, sql)

    if dbResult['status'] != 'success':
        messsage='Could not delete project member data'
        onQueryLoad = "return displayWindow('%s')" % message
        exit(message)

    result = dbResult['result']
    username = string.strip(result[0]['member_username'])

    sql="DELETE FROM project_members WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sql)

    msg='/var/www/admin/%s.passwd' % (db_name)
    deleteUserStatus, output=authentication.delete_pwd_entry(msg,username)

    if (dbResult['status'] !='success') or (deleteUserStatus !='success'):
        message='Could not delete project member data'
        onQueryLoad = "return displayWindow('%s')" % message
        exit(message)

    sql = "DELETE FROM priviledges WHERE member_username='%s'" % username
    pmt_utils.executeSQL(db,sql)
        
    message='Project member data successfully deleted'
    onQueryLoad = "return displayWindow('%s')" % message
    db.close()
            
    query_project_members(1)
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def doSave():
    
    status,table_data,db=pageInit('Save',formJS=1)

    if status != 'success':
        message="Could not connect to db.\n%s" % status
        exit(message)

    create='false'
    if form["key_id"].value == 'create':
        create='true'

        # check for duplicate username
        sql="select id from project_members "
        sql=sql+"where member_username='%s'" % form['member_username'].value
        dupResult=pmt_utils.executeSQL(db,sql)
        if len(dupResult['result'])!=0:
            msg="The specified username '%s' "% form['member_username'].value
            msg=msg+'is already in use.' 
            exit(msg)

        # update the member id
        sql="SELECT NEXTVAL('project_members_id_seq')"
        queryResult = pmt_utils.executeSQL(db, sql)
        if queryResult['status']!='success':
            message="Unable to retrieve project member id"
            exit(message,table_data,db)
            
        form["key_id"].value = `queryResult['result'][0]['nextval']`
        form['id'].value=form['key_id'].value

    # save member data to project_members table in db
    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value,
                                  "project_members",
                                  " WHERE id = '%s'" % form["key_id"].value,
                                  form)
    if dbResult['status'] != 'success':
        message="Project member could not be saved.\n" + dbResult['message']
        exit(message,table_data,db)

    # save privileges to privileges table in db
    whereStr=" WHERE member_username='%s'" % form["member_username"].value
    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['member_username'].value,
                                  "priviledges",
                                  whereStr,
                                  form)
    if dbResult['status'] != 'success':
        message="Unable to save member privileges.\n%s" % dbResult['message']
        exit(message,table_data,db)

    # Display the user information
    table_data = pmt_utils.formToTableData(table_data,
                                           'project_members',
                                           form, form['key_id'].value)  
    pmt_utils.display_form(table_data,'project_members',1,'useValues',1,db)

    # Display the user's privileges
    sql = "select * from priviledges "
    sql=sql+"where member_username='%s'" % (form['member_username'].value)
    dbResult = pmt_utils.executeSQL(db, sql)
    if dbResult['status'] != 'success':
        message="Could not get member privileges.\n%s" % dbResult['message']
        exit(message)
    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'priviledges', result[0])
    displayPriviledges(result[0], table_data)
    pmt_utils.alertsArea(form,"Project member successfully saved")
    
#    if create=='true':
    # Add the username and password to the .passwd file or htaccess
    command='/usr/bin/htpasswd -b '
    command=command+'/var/www/admin/%s.passwd ' % db_name
    #NOTE : Use the form data here since an admin's cookie is logged in
    command=command+'%s ' % form['member_username'].value
    command=command+'%s' % form['member_password'].value
    status, output = commands.getstatusoutput(command)

    if create=='true':
        # Send an email to the new user
        db_label=string.upper(db_name)
        if db_label=='SAVE':
            db_label="IFCS"
        if db_label=="BUAV":
            db_label="FCST"
        if db_label=="CUAV":
            db_label="PADV"
        msg="A new user account has been created for you "
        msg=msg+"on the %s site at www.isrparc.org.\n\n"%string.upper(db_label)
        #NOTE : Use the form data here since an admin's cookie is logged in
        msg=msg+"Username: %s\n" % form['member_username'].value
        msg=msg+"Password: %s" % form['member_password'].value
        pmt_utils.send_email('localhost',
                             'webmaster@isrparc.org',
                             [form['email'].value],
                             "New User Account",
                             msg)

    # Add buttons and hidden fields
    listing_url='/%s-cgi-bin/project_members_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/contactsum.html' % db_name
    pmt_utils.editFunctionButtons(form["key_id"].value,listing_url, help_url)
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)	

#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def doCreate():
    status,table_data,db=pageInit('Create',formJS=1)
    if status != 'success':
        message="Could not connect to db.\n%s" % status
        exit(message)
 
    pmt_utils.display_form(table_data, 'project_members', 1,'useValues',1,db)
    displayPriviledges({}, table_data)

    message="Enter information on form and depress Create button"
    pmt_utils.alertsArea(form,message)

    # Add buttons and hidden fields
    listing_url='/%s-cgi-bin/project_members_admin.pyc?performDbQuery=1' % (db_name) 
    help_url='/%s/html/contactsum.html' % db_name
    pmt_utils.createFunctionButtons('create',listing_url, help_url)
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def doView():

    status,table_data,db=pageInit('View',formJS=1)
    if status != 'success':
        message="Could not connect to db.\n%s" % status
        exit(message)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'project_members',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)
    if dbResult['status'] != 'success':
        message="Unable to get project member data.\n%s" % dbResult['message']
        exit(message,table_data,db)

    # Display user data
    result = dbResult['result']
    table_data=pmt_utils.dbToTableData(table_data,'project_members',result[0])
    pmt_utils.display_form(table_data, 'project_members', 0)

    # Add buttons and hidden fields
    listing_url='/%s-cgi-bin/project_members_admin.pyc?performDbQuery=1' % (db_name) 
    help_url='/%s/html/contactsum.html' % db_name
    pmt_utils.viewFunctionButtons(listing_url, help_url)
    pageEnd(table_data,db)
#------------------------------------------------------------------------------


#----------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):
    if form["action"].value == "edit":
        doEdit()

    elif form["action"].value == "query":
        query_project_members(1)

    elif form["action"].value == "delete":
        doDelete()

    elif form["action"].value == "save":
        doSave()

    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()
else:
    query_project_members(1)
#------------------------------------------------------------------------------
