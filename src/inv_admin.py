# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Scott Davis
#
# CONTACT:
#   Scott Davis
#   E-mail: scott.davis@linuxden.com
#
import os, string, sys
import cgi, glob
from pg import DB
import pmt_utils
import declarations
import time_pkg
import db_authentication
import urllib
import file_io



#------------------------------------------------------------------------------
def queryFunctionButtons(priv=0,loginOk=0, help_pdf=None):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    java="return execute('query')"
    html='<INPUT NAME="query" type="button" value=" Query " onClick="%s">'%java
    pmt_utils.tableColumn(html)
    if priv == 1:
        java="return execute('create')"
        html='<INPUT NAME="create" type="button" value=" Create " '
        html=html+'onClick="%s">' % java
        pmt_utils.tableColumn(html)
    if loginOk==1:
        java="return execute('csv')"
        html='<INPUT NAME="csv" type="button" value=" Export " '
        html=html+'onClick="%s">' % java
        pmt_utils.tableColumn(html)

    java="return goto_url ('%s')" % help_pdf 
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' %java
    pmt_utils.tableColumn(html)
    print '</TR>'
    print '</TABLE>'
#------------------------------------------------------------------------------

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
def emailButton(username,key,menu_name, help_pdf):
    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    link=link+'?table=inventory&key=%s&username=%s' % (key,username)
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    java="return goto_url ('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    
    if username!=None:
        java="return popup('%s','Email_Inventory_Item',600,500)" % link
        html='<input type="button" name="email" value=Email onClick="%s">'%java
        pmt_utils.tableColumn(html)

    java="return goto_url ('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR>'
    print '</TABLE>'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def display_questionnaire(db, table_data, view):

    if view == 'read-only':
        editable = 0
    else:
        editable = 1

    print '<TABLE>' 

    print '<CAPTION>Field Labels in <B><FONT COLOR=RED>Red</FONT></B>'
    print ' or <B>Bold</B> on Mononchrome Displays are Required</CAPTION>'
    print '<TR><TH>Field Name</TH><TH>Value</TH><TH>Format</TH></TR>'

    display_list = []

    field_name_keys = table_data['inventory'].keys()

    SIZE = 0 #####
    
    # find max display order = SIZE
    for i in field_name_keys:
        
        if table_data['inventory'][i]['display_order'] > SIZE:
            SIZE = table_data['inventory'][i]['display_order']
        else:
            continue

    # build display list array
    for i in xrange(0,SIZE):
        display_list.append("")
        
    # load display_list entries with table display order field_names
    for i in field_name_keys:
        display_list[int(table_data['inventory'][i]['display_order'])-1] = i

    field_name_keys = display_list

    for field_name in field_name_keys:

        if field_name == '':  #if field_name is empty...continue  #####
            continue

        if field_name == 'total_unit_price':           
            sql="SELECT quantity, unit_price FROM inventory WHERE id = '%s'" % form['key_id'].value
            db_result = pmt_utils.executeSQL(db, sql)

            if len(db_result['result'])==0:
                total_unit_price=0.0
            else:
                quantity = float(db_result['result'][0]['quantity'])
                unit_price = float(db_result['result'][0]['unit_price'])
                total_unit_price = quantity * unit_price
                
            print '<TR>'
            pmt_utils.print_label(label=table_data['inventory'][field_name]['label'],required=required)
            print '</TD><TD>%.2f</TD></TR>' % total_unit_price 

            sql="UPDATE inventory SET total_unit_price='%s'" % (str(total_unit_price))
            sql="%s WHERE id = '%s'" % (sql,form['key_id'].value)
            db_result = pmt_utils.executeSQL(db, sql)
            continue


        if table_data['inventory'][field_name].has_key('required') and \
           table_data['inventory'][field_name]['required'] == 1:
            required = 1
        else:
            required = 0
        
        print '<TR>'

        if view == 'read-only':
            if field_name in ['analyst_username',
                              'qa_completion_signature_function']:
                continue
        else:
            print '<TR>'
 
        pmt_utils.print_label(label=table_data['inventory'][field_name]['label'],
                              required=required)

        print '<TD>'
        pmt_utils.display_table_item_on_form(db,table_data, 'inventory',field_name,
                                        editable=editable, display_item_only=1)
        print '</TD></TR>'

        #if field_name == 'qa_completion_signature_function':
            #print '<TD COLSPAN=3><HR></TD></TR><TR>'

    print '</TABLE>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
    db_key = arguments[0]
    priv = arguments [3]

    options = '<TD ALIGN=CENTER NOWRAP>'

    java="return execute('edit', '%s')" % db_key
    html='<INPUT NAME="edit" type="button" value=" Edit " onClick="%s">' % java
    options = options + html

    if priv==1:
        java="return execute('delete', '%s')" % db_key
        html='<INPUT NAME="delete" type="button" value=" Delete " '
        html=html+'onClick="%s">' % java
        options = options + html

    java="return execute('view', '%s')" % db_key
    html='<INPUT NAME="view" type="button" value=" View " onClick="%s">' % java
    options = options + html + "</TD>"
    
    return options
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def editFunctionButtons(db_key, menu_name, help_pdf=None):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    java="return execute('save','%s')" % db_key
    html='<INPUT NAME="save" type="button" value=" Save " onClick="%s">' % java
    pmt_utils.tableColumn(html)

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
    print '</TR>'
    print '</TABLE>'
#------------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageInit(subHeading=None,formJS=0):
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    if formJS:
       pmt_utils.generate_form_javascript(table_data,'inventory','inv_admin',0)
    else:
       pmt_utils.javaScript("inv_admin")
    pmt_utils.title("Inventory")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Inventory')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("inv_admin",
                        declarations.pmt_info['db_name'],
                        "inv_admin",
                        "return submitForm(document.inv_admin)")

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
       # create_priv=pmt_utils.hasPriv(db,username,'create_inv')
        create_priv=1
    else:
        create_priv=0

    url='/%s/html/sprsum.html' % db_name
    pmt_utils.queryFunctionButtons(create_priv, url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
        pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------


#------------------------------------------------------------------------------
def query_inventory(performDbQuery=0, onLoad=None, queryFields=None):

    status,table_data,db=pageInit('Inventory',formJS=0)

    if status != 'success':
        message="Can not connect to database.\n%s" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)
            
    queryFields, whereFields = pmt_utils.getQueryWhereFields(form,
                                                             table_data,
                                                             'inventory')

    if queryFields == None or queryFields == []:
        queryFields = []
        whereFields = None
        queryFields.append('quantity')
        queryFields.append('part_number')
        queryFields.append('description')
        queryFields.append('unit_price')
    ignore_fields = []
    del_priv=pmt_utils.hasPriv(db, username, 'del_inv')
    dbResult,queryStatement=pmt_utils.executeQuery(db,
                                                  table_data,
                                                 'inventory',
                                                  queryFields,
                                                  whereFields,
                                                  'query',
                                                  queryItemFunctionsHtml,
                                                  'ORDER by int4(id)',
                                                 ['id'],
                                                  None,
                                                  ignore_fields,
                                                   "return execute('query')",
                                                  ["","",del_priv])

    if dbResult['status'] != 'success':
       message="Could not retrieve inv data from db.\n" + dbResult['message']
       exit(message)

    msg="Last Query Statement: %s\n" % queryStatement
    msg=msg+"%s items retrieved from database." % `len(dbResult['result'])`
    exit(msg,table_data,db)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doEdit():

    status,table_data,db=pageInit("Edit",formJS=1)

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
                                                          'inventory',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)
           
    if dbResult['status'] != 'success':
        message="Could not retrieve item to edit.\n" + dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'inventory', result[0])
    display_questionnaire(db,table_data, 'edit')
    pmt_utils.alertsArea(form, "Item data retrieved successfully");

    pmt_utils.textbox(None, 'prop_id_assigned_by_signature',
                      table_data['inventory']['prop_id_assigned_by_signature']['value'],
                       '40', '40', None, None, 'hidden')

    listing_url='/%s-cgi-bin/inv_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % (db_name)
    po_id = table_data['inventory']['po_id']['value']
    print '<input type=hidden name=po_id value="%s">' % po_id

    if form.has_key("return_to_po"):
        print '<input type=hidden name=return_to_po value=1>'
        java="return goto_url('/%s-cgi-bin/po_admin.pyc?action=edit&key_id=%s')" % (db_name, table_data['inventory']['po_id']['value'])
        html='<INPUT NAME="edit" type="button" value=" Return to PO " onClick="%s">' % java
        print '<BR><BR>'
        print html
    
    editFunctionButtons(form["key_id"].value, listing_url,help_url)
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
    
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doCsv():

    status,table_data,db=pageInit("Export",formJS=0)

    if status != 'success':
        message="Can not connect to database.\n" + status

    sql="SELECT id, inv_prefix, outside_id, gist, source, inv_status, "
    sql=sql+"problem_description, problem_duplication, system_status, "
    sql=sql+"priority, category, originator, origination_date, assigned_to, "
    sql=sql+"analysis, analyst_signature, swm_analysis_signature, "
    sql=sql+"corrective_action, config_items_impacted, test_plan, "
    sql=sql+"test_results, swm_completion_signature, "
    sql=sql+"test_completion_signature, cm_completion_signature, "
    sql=sql+"qa_completion_signature from inventory ORDER by inv_prefix, int4(id)"
    queryResult = pmt_utils.executeSQL(db, sql)

    if queryResult["status"] != 'success':
        message="Query failed.\n" + dbResult['message']

    result = queryResult['result']

    print '<a href="/%s/html/%s">' % (db_name,'inventory.csv')
    print 'Inventory File '
    print '(Right Click and select &quot;Save Link As&quot; to download)</a>'
    print '<BR><BR><B>The Comma Separated Values file contains the following'
    print 'fields for each record:</B>'
    print '<TABLE BORDER>'
    print '<TR><TD>Inventory Id</TD><TD>Prefix</TD><TD>Outside Id</TD>'
    print '<TD>Gist</TD><TD>Source</TD><TD>Status</TD>'
    print '<TD>Problem Description</TD><TD>Problem Duplication</TD>'
    print '<TD>System Status</TD><TD>Priority</TD><TD>Category</TD>'
    print '<TD>Originator</TD><TD>Origination Date</TD><TD>Assigned To</TD>'
    print '<TD>Analysis</TD><TD>Corrective Action</TD>'
    print '<TD>Configuration Items Impacted</TD><TD>Test Plan</TD>'
    print '<TD>Test Results</TD><TD>Completion Status</TD></TR></TABLE>'
    print 'NOTE: Commas in fields have been changed to whitespace'
    output_lines = []
    for i in xrange(0, len(result)):
        inv_completed = 'Open'
        if string.strip(result[i]['inv_status']) == 'Fixed (complete)':
            if string.strip(result[i]['analyst_signature']) != ''         and \
                 string.strip(result[i]['swm_analysis_signature'])!=''    and \
                 string.strip(result[i]['swm_completion_signature'])!=''  and \
                 string.strip(result[i]['test_completion_signature'])!='' and \
                 string.strip(result[i]['cm_completion_signature'])!=''   and \
                 string.strip(result[i]['qa_completion_signature'])!='':
                inv_completed = 'Closed'                            

        txt = string.replace(result[i]['inv_prefix'],',','') + ','
        txt=txt+ string.replace(result[i]['id'],',','') + ','
        txt=txt+ string.replace(result[i]['outside_id'],',','') + ','
        txt=txt+ string.replace(result[i]['gist'],',','') + ','
        txt=txt+ string.replace(result[i]['source'],',','') + ','
        txt=txt+ string.replace(result[i]['inv_status'],',','') + ','
        txt=txt+ string.replace(result[i]['problem_description'],',','')+ ','
        txt=txt+ string.replace(result[i]['problem_duplication'],',','')+ ','
        txt=txt+ string.replace(result[i]['system_status'],',','') + ','
        txt=txt+ string.replace(result[i]['priority'],',','') + ','
        txt=txt+ string.replace(result[i]['category'],',','') + ','
        txt=txt+ string.replace(result[i]['originator'],',','') + ','
        txt=txt+ string.replace(result[i]['origination_date'],',','') + ','
        txt=txt+ string.replace(result[i]['assigned_to'],',','') + ','
        txt=txt+ string.replace(result[i]['analysis'],',','') + ','
        txt=txt+ string.replace(result[i]['corrective_action'],',','') + ','
        txt=txt+ string.replace(result[i]['config_items_impacted'],',','')+ ','
        txt=txt+ string.replace(result[i]['test_plan'],',','') + ','
        txt=txt+ string.replace(result[i]['test_results'],',','') + ','
        txt=txt+ inv_completed
        txt = string.replace(txt,'\r\n',' ')
        txt = string.replace(txt,'\n',' ')
        output_lines.append(txt)

    filename='/home/%s/html/inventory.csv' % db_name
    file_io.writeToFile(filename,output_lines)

    queryFunctionButtons(0,1, '/%s/html/sprsum.html' % (db_name))
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doDelete():

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        onQueryLoad = 'displayWindow("Could not connect to the database")'
        message="Could not connect to the database.\n%s" % dbResult['message']
        exit(message)

    db = dbResult['result']
    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)
                
    sqlStatement = "DELETE FROM inventory WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        onQueryLoad = "return displayWindow('Could not delete item data')"
    else:
        onQueryLoad = "return displayWindow('Item data successfully deleted')"

    db.close()
    query_inventory(1)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doSave():
    saveDueToCreate = 0    

    status,table_data,db=pageInit('Edit',formJS=1)

    if status != 'success':
        message="Could not connect to db.\n%" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    if form["key_id"].value == 'create':
        saveDueToCreate = 1
        queryResult = pmt_utils.executeSQL(db, "SELECT NEXTVAL('inventory_id_seq')")

        form["key_id"].value = `queryResult['result'][0]['nextval']`

    table_data = pmt_utils.formToTableData(table_data,
                                           'inventory',
                                           form,
                                           form['key_id'].value)
    alerts = ''

    data=pmt_utils.process_signature(db,
                                     form['prop_id_assigned_by_username'].value,
                                     form['prop_id_assigned_by_password'].value,
                                     'Property ID Authority',
                                     form['prop_id_assigned_by_signature'].value,
                                     form['prop_id_assigned_by_sig_func'].value)
    (status, details,
     table_data['inventory']['prop_id_assigned_by_username']['value'],
     table_data['inventory']['prop_id_assigned_by_password']['value'],
     table_data['inventory']['prop_id_assigned_by_signature']['value'],
     table_data['inventory']['prop_id_assigned_by_sig_func']['value']) = data


    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value, "inventory",
                                  " WHERE id = '%s'" % form["key_id"].value,
                                  form, 0, 0)

    if dbResult['status'] != 'success':
        message="Item could not be saved.\n" + dbResult['message']
        exit(message)

    if saveDueToCreate:
        subject='New INV #%s has been generated' % form['key_id'].value
       # message='INV #%s has been generated.\n\n' % form["key_id"].value
       # message=message+'Assigned to: %s\n\n' % form['assigned_to'].value
       # message=message+'Problem Description is as follows:\n'
       # message=message+form['problem_description'].value+'\n\n'
       # message=message+'Log into the Inventory tracking tool at '
       # message=message+'http://www.isrparc.org for further info.'
       # message=message+'If you do not wish to be on this mailing list '
       # message=message+'please send an email requesting removal to '
       # message=message+'cm@isrparc.org.\n'
       # pmt_utils.emailList(db,'localhost', 'inv_list', subject, message)

    display_questionnaire(db,table_data, 'edit')

    alerts = alerts + '\nItem saved successfully'
    pmt_utils.alertsArea(form,alerts)

    listing_url='/%s-cgi-bin/inv_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % db_name

    # This will return to po_admin.py or inv_admin.py in Edit mode.
    if form.has_key("return_to_po"):
        data='?action=edit&key_id=%s'%table_data['inventory']['po_id']['value']
        java="return goto_url('/%s-cgi-bin/po_admin.pyc%s')" % (db_name, data)
        html='<INPUT NAME="edit" type="button" value=" Return to PO '
        html=html+'" onClick="%s">' % java
        print '<BR><BR>'
        print html
    
    editFunctionButtons(form["key_id"].value, listing_url, help_url)


    po_id = table_data['inventory']['po_id']['value']
    print '<input type=hidden name=po_id value="%s">' % po_id

    val=table_data['inventory']['prop_id_assigned_by_signature']['value']
    pmt_utils.textbox(None, 'prop_id_assigned_by_signature',
                      val,'40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)


#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doCreate():
    status,table_data,db=pageInit('Create',formJS=1)
    if status != 'success':
        message="Could not connect to db,\n" + dbResult['message']
        exit(message)
    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)

    display_questionnaire(db,table_data, 'edit')
    message="Enter information on form and depress Create button"
    pmt_utils.alertsArea(form,message)

    listing_url='/%s-cgi-bin/inv_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % db_name
    pmt_utils.createFunctionButtons('create',listing_url,help_url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    po_id = table_data['inventory']['po_id']['value']
    print '<input type=hidden name=po_id value="%s">' % po_id
    val=table_data['inventory']['prop_id_assigned_by_signature']['value']
    pmt_utils.textbox(None, 'prop_id_assigned_by_signature',
                      val, '40', '40', None, None, 'hidden')
    pageEnd(table_data,db)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doView():
    status,table_data,db=pageInit("View",formJS=1)
    if status != 'success':
        message='Could not connect to db.\n%s' % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'inventory',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Item data could not be retrieved.\n" + dbResult['message']
        exit(message)
               
    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'inventory', result[0])
    display_questionnaire(db,table_data, 'read-only')

    listing_url='/%s-cgi-bin/inv_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % (db_name)
    emailButton(username,form['key_id'].value,listing_url, help_url)

    po_id = table_data['inventory']['po_id']['value']
    print '<input type=hidden name=po_id value="%s">' % po_id

    if form.has_key("return_to_po"):
        print '<input type=hidden name=return_to_po value=1>'
        java="return goto_url('/%s-cgi-bin/po_admin.pyc?action=edit&key_id=%s')" % (db_name, table_data['inventory']['po_id']['value'])
        html='<INPUT NAME="view" type="button" value=" Return to PO " onClick="%s">' % java
        print '<BR><BR>'
        print html

    pageEnd(table_data,db)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name = declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):

    if form["action"].value == "edit":
            doEdit()
        
    elif form["action"].value == "query":
        query_inventory(1)

    elif form['action'].value == 'csv':
        doCsv()

    elif form["action"].value == "delete":
        doDelete()

    elif form["action"].value == "save":
        doSave()
            
    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()

else:
    query_inventory(1)
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------
