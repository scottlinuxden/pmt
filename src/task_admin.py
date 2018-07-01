# $Id$
#
# CLASSIFICATION: 
#   UNCLASSIFIED
#
# COPYRIGHT:
#   Copyright (C) 2000, linuXden.com, LLC, All Rights Reserved
#   Copright Statement at http://www.linuXden.com/pmt_copyright.html
#
# AUTHOR: 
#   R. Scott Davis
#
# ORGANIZATION: 
#   www.linuXden.com, LLC
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
import string


#-----------------------------------------------------------------------------
def sendEmail(db, key_id):
# Send a notification email to the assignee(s) of this task and the task admin

    # Get the 'last, first' names of the originator and the assignee
    sqlStatement="SELECT originator,assigned_to FROM task WHERE id='%s'"%key_id
    result=pmt_utils.executeSQL(db,sqlStatement)
    
    # Split the originator's 'last, first' string into last and first name
    index=string.find(result['result'][0]['originator'],',')
    from_last_name=result['result'][0]['originator'][:index]
    from_first_name=result['result'][0]['originator'][index+2:]
    to_name=result['result'][0]['assigned_to']

    # Get the email of the originator
    sql="SELECT email FROM project_members "
    sql=sql+"WHERE last_name='%s' " % from_last_name
    sql=sql+"and first_name='%s'" % from_first_name
    result=pmt_utils.executeSQL(db,sql)
    from_email=result['result'][0]['email']

    # If task is assigned to 'All' generate list of all task viewers
    if to_name=="All":
        sqlStatement="SELECT email FROM project_members p1, priviledges p2"+\
                     " where view_task='t' and " + \
                     " p1.member_username=p2.member_username"
    else:
        # Otherwise get the email of the assignee
        index=string.find(to_name,',')
        to_last_name=to_name[:index]
        to_first_name=to_name[index+2:]
        sql="SELECT email FROM project_members "
        sql=sql+"WHERE last_name='%s' " % to_last_name
        sql=sql+"and first_name='%s'" % to_first_name
        result=pmt_utils.executeSQL(db,sql)

        # Build a list of email addresses to send the notification to
        # Always send notification to the task_admin alias
        db_name=declarations.pmt_info['db_name']
        to_email=['%s_task_admin@isrparc.org' % (db_name)]
        for i in xrange(0,len(result['result'])):
            to_email.append(result['result'][i]['email'])

    # Create content of email
    content='Description: %s\n\n' % form['description'].value
    content=content+'This task can be viewed online at www.isrparc.org'

    # Send the email
    if string.upper(db_name)=='SAVE':
        db_name='IFCS'
    if string.upper(db_name)=='BUAV':
        db_name='FCST'
    if string.upper(db_name)=='CUAV':
        db_name='PADV'
        
    pmt_utils.send_email('localhost', from_email, to_email,
                         "New %s Task" % string.upper(db_name), content)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
# Returns html for edit, (delete), and view buttons for each task in the list

    db_key = arguments[0]
    originator = arguments[1]

    options = '<TD ALIGN=CENTER NOWRAP>'

    options = options + '<INPUT NAME="edit" type="button" value=" Edit "' + \
              ' onClick="return execute(' +"'edit'"+ ", '" +db_key+ "'" + ')">'

    if username == 'rsdavis':
        options = options + '<INPUT NAME="delete" type="button"' + \
                  'value=" Delete " onClick="return execute(' + \
                  "'delete'" + ", '" + db_key + "'" + ')">'

    return options + '<INPUT NAME="view" type="button" value=" View "' + \
           ' onClick="return execute(' +"'view'"+", '"+db_key+ "'" + ')"></TD>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def editFunctionButtons(db_key, menu_name, help_pdf=None):
# Add save, (delete), view, listing, and help buttons at bottom of page

    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    pmt_utils.tableColumn('<INPUT NAME="save" type="button" value=" Save "' + \
                          ' onClick="return execute(' + "'save'" + ",'" + \
                          db_key + "'" + ')">')

    if username=='rsdavis':
        pmt_utils.tableColumn('<INPUT NAME="delete" type="button"' + \
                              ' value=" Delete " onClick="return execute(' +\
                              "'delete'" + ",'" + db_key + "'" + ')">')

    pmt_utils.tableColumn('<INPUT NAME="view" type="button" value=" View "' + \
                          ' onClick="return execute(' + "'view'" + \
                          ", '" + db_key + "'" + ')">')
    pmt_utils.tableColumn('<INPUT TYPE="button" NAME="return_to_menu"' + \
                          ' VALUE=" Listing " onClick="return goto_url (' + \
                          "'" + menu_name + "'" + ')">')
    pmt_utils.tableColumn('<INPUT TYPE="button" NAME="help" VALUE=" Help "' + \
                          ' onClick="return goto_url (' + "'" + help_pdf + \
                          "'" + ')">')
    print '</TR>'
    print '</TABLE>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# This function displays the results of a SQL query on the database
def query_task(performDbQuery=0,
               onLoad=None,
               queryFields=None,
               commonWheres=None,
               customSQL=None):

    # Set up the webpage
    status,table_data,db=pageInit()

    if status!="success":
        return
    else:
        authenticate(form,db)

        queryFields, whereFields = pmt_utils.getQueryWhereFields(form,
                                                                 table_data,
                                                                 'task')

        if customSQL!=None:
            result=pmt_utils.executeSQL(db,customSQL)
            fromIndex=string.find(customSQL,'from')
            queryFieldString=customSQL[6:fromIndex]
            queryFields=string.split(queryFieldString,',')
            for i in xrange(0,len(queryFields)):
                queryFields[i]=string.strip(queryFields[i])

        if commonWheres!=None:
            for i in xrange(0,len(commonWheres)):
                whereFields.append(commonWheres[i])

        addCustomQueryButtons(username)

        if queryFields == None or queryFields == []:
            queryFields = []
            whereFields = None
            queryFields.append('id')
            queryFields.append('description')
            queryFields.append('assigned_to')

        dbResult,queryStatement=pmt_utils.executeQuery(db,table_data,'task',
                                                     queryFields,whereFields,
                                                     'query',
                                                     queryItemFunctionsHtml,
                                                     'ORDER by int4(id)',
                                                     ['id','originator'],
                                                     None, None,
                                                     "return execute('query')",
                                                     ["",""],
                                                     customSQL)

        # if query was not successful, output an error message
        if dbResult['status'] != 'success':
            pmt_utils.alertsArea(form,
                                 "Could not retrieve task from database,\n" + \
                                 dbResult['message'])
        else:
            pmt_utils.alertsArea(form,"Last Query Statement: "+queryStatement+\
                                 "\n" + `len(dbResult['result'])` +\
                                 " task items retrieved from database")

        pmt_utils.queryFunctionButtons(1, declarations.pmt_info['help_file'])

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')


    pageEnd(table_data,db)

    if form.has_key("performDbQuery") or performDbQuery == 1:
        return dbResult
    else:
        return {'status' : 'success',
                'message' : 'query successful',
                'result' : 0}
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def addCustomQueryButtons(username):
# Add buttons for common and custom queries
    print '<HR><BR>'
    print '<INPUT NAME="myTasks" type="button" value="My Tasks"' + \
          ' onClick="return execute(' + "'common_query','myTasks'" + ')">'
    print '<INPUT NAME="myUnfinishedTasks" TYPE=button' + \
          ' VALUE="My Unfinished Tasks" onClick="return execute(' + \
          " 'common_query','myUnfinishedTasks'" + ')">'
    print '<INPUT NAME="allUnfinishedTasks" TYPE=button' + \
          ' VALUE="All Unfinished Tasks" onClick="return execute(' + \
          " 'common_query','allUnfinishedTasks'" + ')">'
    print '<INPUT NAME="allTasks" TYPE=button VALUE="All Tasks"' + \
          ' onClick="return execute(' + "'common_query','allTasks'" + ')">'
    print '<BR>'
    print '<INPUT NAME="custom" TYPE=button VALUE="Custom Query"' + \
          ' onClick="return execute(' + "'common_query','custom'" + ')">'
    print '<INPUT NAME=sqlStatement TYPE=TEXT SIZE=40 MAXLENGTH=100>'
    print '<HR>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageInit(subHeading=None):
# Set up the HTML for the page and connect to the database

    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"

    if subHeading==None:
        pmt_utils.javaScript("task_admin")
    else:
        pmt_utils.generate_form_javascript(table_data,'task','task_admin',0)

    pmt_utils.title("Task Item")
    print "</HEAD>"
    pmt_utils.bodySetup(onLoad=None)
    pmt_utils.mainHeading('Task Item')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)

    pmt_utils.formSetup("task_admin",
                        declarations.pmt_info['db_name'],
                        "task_admin",
                        "return submitForm(document.task_admin)")
    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])
    if dbResult['status'] != 'success':
        pmt_utils.alertsArea(form,
                             "Could not connect to the database\n" + \
                             dbResult['message'])
        db=None
        status="error"
    else:
        db=dbResult['result']
        status="success"

    return status,table_data,db
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageEnd(table_data,db):
# Print company info and close database

    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def authenticate(form,db):
# Check the given username/passswd and exit on errors or lack of privileges

    status,details = db_authentication.password_valid(db,
                                                      crypt_salt=db_name,
                                                      username=username,
                                                      password=password)

    if status != 'success':
        exit(form,details)

    if pmt_utils.hasPriv(db,username,'view_task')!=1:
        details='User %s does not have privileges to view tasks' % username
        exit(form,details)
#-----------------------------------------------------------------------------



#-----------------------------------------------------------------------------
def exit(form,message):
    pmt_utils.usernamePasswordDisplay()
    pmt_utils.alertsArea(form, message)
    pmt_utils.queryFunctionButtons(0,'/%s/html/tasksum.html' % db_name)
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    sys.exit(1)
    
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doEdit():
    status,table_data,db=pageInit("Edit")
    if status!="success":
        exit(form,"Could not initialize page")

    authenticate(form,db)

    sqlStatement=pmt_utils.selectAllColumnsSqlStatement(table_data, 'task',
                                                          form["key_id"].value)

    dbResult = pmt_utils.executeSQL(db, sqlStatement)
    if dbResult['status'] != 'success':
        details="Could not get task from db.\n" + dbResult['message']
        exit(form,details)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data,'task',result[0])
    pmt_utils.display_form(table_data,'task',1,'useValues',1,db)
    pmt_utils.alertsArea(form,"Task item retrieved successfully")

    editFunctionButtons(form["key_id"].value,
                        '/%s-cgi-bin/task_admin.pyc?performDbQuery=1'%db_name,
                        declarations.pmt_info['help_file'])

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doDelete():
    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        onQueryLoad = 'displayWindow("Could not connect to database")'
    else:
        db = dbResult['result']
        authenticate(form,db)

        sqlStatement="DELETE FROM task WHERE id='%s'" %form["key_id"].value
        dbResult = pmt_utils.executeSQL(db, sqlStatement)

        if dbResult['status'] != 'success':
            onQueryLoad="return displayWindow('Cannot delete task data')"
        else:
            onQueryLoad="return displayWindow('Task has been deleted')"

        db.close()
        query_task(1)
 
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doSave():
    status,table_data,db=pageInit("Save")

    if status!='success':
        sys.exit()
    else:
        authenticate(form,db)

        create='false'
        if form["key_id"].value == 'create':
            queryResult=pmt_utils.executeSQL(db,
                                             "SELECT NEXTVAL('task_id_seq')")
            form["key_id"].value = `queryResult['result'][0]['nextval']`
            create='true'

        # save the Form
        dbResult = pmt_utils.saveForm(table_data, db,
                                      form['key_id'].value,
                                      "task",
                                      " WHERE id = '"+form["key_id"].value+"'",
                                      form)

        # if the form was not successfully saved
        if dbResult['status'] != 'success':
            pmt_utils.alertsArea(form,"Task could not be saved due to" + \
                                 " a db error .\n" +dbResult['message'])
        else:
            # form was successfully saved
            # table_data = declarations.define_tables()
            table_data = pmt_utils.formToTableData(table_data,'task', form,
                                                   form['key_id'].value)

        pmt_utils.display_form(table_data, 'task', 1, 'useValues', 1, db)

        if create=='true':
            sendEmail(db, form['key_id'].value)
            pmt_utils.alertsArea(form,"Task item successfully saved.\n" + \
                                 "Email notifications have been sent.")
        else:
            pmt_utils.alertsArea(form,"Task item successfully saved.")

    # generate function button row
    editFunctionButtons(form["key_id"].value,
                        '/%s-cgi-bin/task_admin.pyc?performDbQuery=1'%db_name,
                        declarations.pmt_info['help_file'])

    # generate hidden fields for form
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pageEnd(table_data,db)

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doCreate():
    status,table_data,db=pageInit('Create')

    table_data = pmt_utils.init_table_data(table_data,'task')
    now=time_pkg.current_time_MM_DD_YYYY()
    table_data['task']['date_created']['value'] = now

    if status!="success":
        sys.exit()

    authenticate(form,db)
    pmt_utils.display_form(table_data, 'task', 1,'useValues',1,db)

    # display alerts area to create
    pmt_utils.alertsArea(form,"Enter data on form and press Create button")

    # create functions button row
    pmt_utils.createFunctionButtons('create',
                                    '/%s-cgi-bin/task_admin.pyc?performDbQuery=1'%db_name,
                                    declarations.pmt_info['help_file'])

    # create hidden fields for form
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pageEnd(table_data,db)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doView():
    status,table_data,db=pageInit("View")

    if status!="success":
        sys.exit()
    else:
        authenticate(form,db)

        sqlStatement=pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'task',
                                                          form["key_id"].value)

        dbResult = pmt_utils.executeSQL(db, sqlStatement)

        # if select failed
        if dbResult['status'] != 'success':
            # generate error in alerts area
            pmt_utils.alertsArea(form,
                                 "Task data could not be retrieved.\n" + \
                                 dbResult['message'])
        else:
            # assign result data
            result = dbResult['result']
            table_data=pmt_utils.dbToTableData(table_data,'task',result[0])
            pmt_utils.display_form(table_data, 'task', 0)

    pmt_utils.viewFunctionButtons('/%s-cgi-bin/task_admin.pyc?performDbQuery=1'%db_name,
                                  declarations.pmt_info['help_file'])

    pageEnd(table_data,db)
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doCommonQuery():
    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])
    db=dbResult['result']
    names=pmt_utils.executeSQL(db,"select first_name,last_name from" + \
                               " project_members where" + \
                               " member_username='%s'" % username)

    first=names['result'][0]['first_name']
    last=names['result'][0]['last_name']

    whereFields=[]
    sqlStatement=None
    if form['key_id'].value=='myTasks':
        whereFields.append("assigned_to='%s, %s'" % (last,first))
    if form['key_id'].value=='myUnfinishedTasks':
        whereFields.append("assigned_to='%s, %s'" % (last,first))
        whereFields.append('completion_date IS NULL')
    if form['key_id'].value=='allUnfinishedTasks':
        whereFields.append('completion_date IS NULL')
    if form['key_id'].value=='custom':
        sqlStatement=form['sqlStatement'].value
        if sqlStatement=='':
            sqlStatement=None
        elif string.upper(sqlStatement[:6])!="SELECT":
            sqlStatement=None

    query_task(0,commonWheres=whereFields,customSQL=sqlStatement)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
pmt_site = declarations.pmt_info['domain_name']
db_name = declarations.pmt_info['db_name']
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
username,password=pmt_utils.getUserPass(form)


if form.has_key("action"):
    if form["action"].value == "edit":
        doEdit()

    elif form["action"].value == "query":
        query_task(1)

    elif form["action"].value == "delete":
        doDelete

    elif form["action"].value == "save":
        doSave()

    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()

    elif form["action"].value == 'common_query':
        doCommonQuery()
else:
    query_task(0)
#-----------------------------------------------------------------------------

