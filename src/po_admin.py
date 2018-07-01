#-*- Mode: Python; tab-width: 4 -*-
# $Id: po_admin.py,v 1.62 2005/04/12 16:31:12 lliabraa Exp $
#
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



g_ignoreFields = ['requisitioner_sig_function',
				'direct_ra_signature_function',
				'indirect_ra_signature_function',
				'department_exec_sig_function',
				'corp_officer_sig_function',
				'po_math_checked_by_sig_function',
				'purchase_ordered_by_sig_func',
				'purchase_received_by_sig_func',
				'inv_math_checked_by_sig_func',
				'ap_entered_by_sig_function',
				'prop_id_assigned_by_sig_func',
				'billing_address',
				'direct_project_charge_number','direct_project_charge_amount',
				'direct_ra_username',          'direct_ra_password',
				'direct_ra_signature',         'direct_ra_signature_date',
				'indirect_proj_charge_number', 'indirect_proj_charge_amount',
				'indirect_ra_username',        'indirect_ra_password',
                'indirect_ra_signature',       'indirect_ra_signature_date',
                'department_exec_username',    'department_exec_password',
                'department_exec_signature',   'department_exec_sig_date',
                'corporate_officer_username',  'corporate_officer_password',
                'corporate_officer_signature', 'corporate_officer_sig_data',
                'comments',
                'po_math_checked_by_username', 'po_math_checked_by_password',
                'po_math_checked_by_signature',
                'purchase_ordered_by_username','purchase_ordered_by_password',
                'purchase_ordered_by_signature',
                'purchase_received_by_username','purchase_received_by_password',
                'purchase_received_by_signature',
                'inv_math_checked_by_username','inv_math_checked_by_password',
                'inv_math_checked_by_signature',
                'ap_entered_by_username',      'ap_entered_by_password',
                'ap_entered_by_signature']

#------------------------------------------------------------------------------
def queryFunctionButtons(priv=0,loginOk=1, help_pdf=None):
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

    
    java="return execute('csv_all')"
    html='<INPUT NAME="csv_all" type="button" value=" Export " '
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
    link=link+'?table=po&key=%s&username=%s' % (key,username)
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    java="return goto_url ('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    
    if username!=None:
        java="return popup('%s','Email_Purchase_Order',600,500)" % link
        html='<input type="button" name="email" value=Email onClick="%s">'%java
        pmt_utils.tableColumn(html)

    java="return goto_url ('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR>'
    print '</TABLE>'
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def addSearch(db,table_data,searchFields=[],searchWhere=None):
    options=[]
    selected=[]
    value=None
    for fieldName in table_data['po'].keys():
        if fieldName in g_ignoreFields:
            continue
        if table_data['po'][fieldName].has_key("form_input_type"):
            if string.lower(table_data['po'][fieldName]['form_input_type'])=='password':
                continue
        options.append(table_data['po'][fieldName]['label'])
        if searchFields!=[]:
            if fieldName in searchFields:
                selected.append("SELECTED")
            else:
                selected.append("")
        elif fieldName=="id":
            selected.append("SELECTED")
        else:
            selected.append("")

    print "<BR><HR>"
    print "Find POs where "
    pmt_utils.optionMenu('searchOption', '1', options, selected)
    if searchWhere==None:
        selected = ["SELECTED","",""]
    elif len(searchWhere)>0:
        if "=" in searchWhere[0]:
            selected = ["SELECTED","",""]
            value=searchWhere[0][string.find(searchWhere[0],"=")+3:-1]
        elif "<" in searchWhere[0]:
            selected = ["","SELECTED",""]
            value=searchWhere[0][string.find(searchWhere[0],"<")+3:-1]
        elif ">" in searchWhere[0]:
            selected = ["","","SELECTED"]
            value=searchWhere[0][string.find(searchWhere[0],">")+3:-1]
        
    pmt_utils.optionMenu("operatorOption",'1',["=","<",">"],selected)

    if value==None:
        print "<INPUT TYPE=TEXT NAME=searchValue>"
    else:
        print '<INPUT TYPE=TEXT NAME=searchValue VALUE="%s">' % value
    print "<INPUT TYPE=button NAME=searchbutton VALUE=Search"
    print ' onClick="return execute('+"'search'"+')">'
    print "<HR><BR>"
    
    
#-----------------------------------------------------------------------------

#------------------------------------------------------------------------------
def displayItems(db,table_data,po_id,editable):
    print "</TABLE>"
    print "<TABLE>"
    print '<TR><TD COLSPAN=5><HR></TD></TR><TR>'
    print '<TD ALIGN=CENTER COLSPAN=5>'
    print "<B>-- Item Descriptions --</B></TD></TR>"
    print '<TD ALIGN=CENTER COLSPAN=5>'
    print "<B>***  Description, Quantity, & Unit Price fields REQUIRED ***</B></TD></TR>"
    print '<TR><TD COLSPAN=5><HR></TD></TR>'
    print '<TR><TD><B><U>Part Number</TD><TD><B><U>Description</TD>'
    print '<TD><B><U>Quantity</TD><TD><B><U>Unit Price</TD></B>'
    print '<TD><B><U>Total Unit Price</TD></TR></B>'

    subtotal = 0.0

    if po_id!='':
        sql="select * from inventory where po_id='%s'" % po_id
        result=pmt_utils.executeSQL(db,sql)

        if result['status']!='success':
            msg="Could not retrieve items from db.\n%s" % result['message']
            exit(msg)
        
        for row in result['result']:
            print '<TR>'
            print '<TD>%s</TD>' % row['part_number']
            print '<TD>%s</TD>' % row['description']
            print '<TD>%s</TD>' % row['quantity']

            if row['unit_price']=='':
                row['unit_price']='0'
            try:
                unit_price=float(row['unit_price'])
            except:
                unit_price = 0
                row['unit_price']='0'
            print '<TD ALIGN=RIGHT COLSPAN=1>'
            print '%.2f</TD>' % unit_price
            
            if row['quantity']=='':
                row['quantity']='0'

            total_unit_price =float(row['quantity']) * float(row['unit_price'])
            print '<TD ALIGN=RIGHT COLSPAN=1>'
            print '%.2f</TD>' % total_unit_price
            

            if editable:
                itemDescriptionFunctionsHtml(row['id'], row['po_id'])

            print '</TR>' 
                        
            subtotal=subtotal + total_unit_price 

    
    table_data['po']['subtotal']['value']='%.2f' % subtotal
                                                             
    print '<input type=hidden name=po_id value="%s">' % po_id

    if editable:
        
        print '<TR>'
        print '<TD><input type=text name=part_number></TD>'
        print '<TD><input type=text name=description></TD>'
        print '<TD><input type=text name=quantity></TD>'
        print '<TD><input type=text name=unit_price></TD>'
     

        java="return execute('add_item')"
        print '<TD><input type=button value="Add Item" onClick="%s"></TD>' % java
        print "</TR>"

    print '<TR><TD COLSPAN=5>'
    if form['action'].value=='blankFields':
        pmt_utils.alertsArea(form, 'Description, Quantity, and Unit Price fields REQUIRED.')
    print '<HR></TD></TR>'
    print "</TABLE>"

    
    print "<TABLE>"
    return table_data
    
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

    field_name_keys = table_data['po'].keys()

    SIZE = 0
    
    # find max display order = SIZE
    for i in field_name_keys:
        
        if table_data['po'][i]['display_order'] > SIZE:
            SIZE = table_data['po'][i]['display_order']
        else:
            continue
        
    # build display list array 
    for i in xrange(0,SIZE):
        display_list.append("")
        
    # load display_list entries with table display order field_names
    for i in field_name_keys:
        display_list[int(table_data['po'][i]['display_order'])-1] = i 

    field_name_keys = display_list

    po_total = 0.0

    billing_address = 'Institute for Scientific Research, Inc.\nP.O. Box 1148\nFairmont, WV  26555-1148\nPhone: (304)368-9300\nFax:  (304)368-9313'
    

    for field_name in field_name_keys:

        if field_name == '':  #if field_name is empty...continue
            continue

        if field_name == 'billing_address':
            table_data['po']['billing_address']['value'] = '%s' % billing_address

        if field_name == 'subtotal' or field_name == 'shipping_handling' or field_name == 'tax_exempt':
            value = table_data['po'][field_name]['value']
            if value == '':
                value = '0'
            po_total = po_total + float(value)
            table_data['po']['po_total']['value']='%.2f' % po_total

            table_data['po'][field_name]['value']='%.2f' % float(value)
            
        if table_data['po'][field_name].has_key('required') and \
           table_data['po'][field_name]['required'] == 1:
            required = 1
        else:
            required = 0
        
        print '<TR>'

        # Sets up inventory table to be displayed in PO form
        if field_name=='vendor_fax':
            pmt_utils.print_label(label=table_data['po'][field_name]['label'],
                                  required=required)

            print '<TD>'
            pmt_utils.display_table_item_on_form(db,
                                                 table_data,
                                                 'po',
                                                 field_name,
                                                 editable=editable,
                                                 display_item_only=1)
            print '</TD></TR>'
            table_data=displayItems(db,table_data,table_data['po']['id']['value'], editable)
            continue
        
        elif field_name == 'vendor_name':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Vendor --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'direct_project_charge_number':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Direct Resource Authority Approval --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'indirect_proj_charge_number':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Indirect Resource Authority Approval --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'department_exec_username':
            print '<TD COLSPAN=3><HR></TD></TR></TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Department Approval --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'corporate_officer_username':
            print '<TD COLSPAN=3><HR></TD></TR></TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Corporate Officer Approval --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'comments':
            print '<TD COLSPAN=3><HR></TD></TR></TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Comments --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'po_math_checked_by_username':
            print '<TD COLSPAN=3><HR></TD></TR></TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Internal Tracking --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'purchase_ordered_by_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'purchase_received_by_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'date_invoice_received':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'check_number':
            print '<TD COLSPAN=3><HR></TD></TR>'

        if view == 'read-only':
            if field_name in ['requisitioner_username',
                              'requisitioner_password',
                              'requisitioner_sig_function',
                              'direct_ra_username',
                              'direct_ra_password',
                              'direct_ra_signature_function',
                              'indirect_ra_username',
                              'indirect_ra_password',
                              'indirect_ra_signature_function',
                              'department_exec_username',
                              'department_exec_password',
                              'department_exec_sig_function',
                              'corporate_officer_username',
                              'corporate_officer_password',
                              'corp_officer_sig_function',
                              'po_math_checked_by_username',
                              'po_math_checked_by_password',
                              'po_math_checked_by_sig_function',
                              'purchase_ordered_by_username',
                              'purchase_ordered_by_password',
                              'purchase_ordered_by_sig_func',
                              'purchase_received_by_username',
                              'purchase_received_by_password', 
                              'purchase_received_by_sig_func',
                              'inv_math_checked_by_username',
                              'inv_math_checked_by_password',
                              'inv_math_checked_by_sig_func',
                              'ap_entered_by_username',
                              'ap_entered-by_password',
                              'ap_entered_by_sig_function',
                              'prop_id_assigned_by_username',
                              'prop_id_assigned_by_password',
                              'prop_id_assigned_by_sig_func']:
                continue
        else:
            print '<TR>'

        pmt_utils.print_label(label=table_data['po'][field_name]['label'],
                              required=required)

        print '<TD>'
        pmt_utils.display_table_item_on_form(db,table_data, 'po',field_name,
                                        editable=editable, display_item_only=1)
        print '</TD></TR>'     

        if field_name == 'ap_entered_by_sig_function':
            print '<TD COLSPAN=3><HR></TD></TR>'

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
    options = options + html

    java="return execute('csv_one', '%s')" % db_key
    html='<INPUT NAME="csv_one" type="button" value=" Export " onClick="%s">' % java
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

#------------------------------------------------------------------------------
def exportAllFunctionButtons(db_key, menu_name, help_pdf=None):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'

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
        pmt_utils.generate_form_javascript(table_data,'po','po_admin',0)
    else:
        pmt_utils.javaScript("po_admin")
    pmt_utils.title("Purchase Order")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Purchase Order')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("po_admin",
                        declarations.pmt_info['db_name'],
                        "po_admin",
                        "return submitForm(document.po_admin)")

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
       # create_priv=pmt_utils.hasPriv(db,username,'create_po')
        create_priv=1
    else:
        create_priv=0

    url='/%s/html/posum.html' % db_name
    queryFunctionButtons(create_priv,1, url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
        pageEnd(table_data,db)
    sys.exit()
#----------------------------------------------------------------------------- 


#------------------------------------------------------------------------------
def query_po(performDbQuery=0, onLoad=None,searchFields=[],searchWheres=None):

    status,table_data,db=pageInit('Purchase Orders',formJS=0)

    if status != 'success':
        message="Can not connect to database.\n%s" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                        crypt_salt=db_name,
                                                        username=username,
                                                        password=password)

    if status != 'success':
        exit(details)

    addSearch(db,table_data, searchFields, searchWheres)

    queryFields, whereFields = pmt_utils.getQueryWhereFields(form,
                                                                table_data,
                                                                'po')
    if queryFields == None:
        queryFields=[]

    if searchWheres!=None:
        for i in xrange(0,len(searchWheres)):
            whereFields.append(searchWheres[i])

    if searchFields!=None:
        for field in searchFields:
            if field in queryFields:
                continue
            if not field in ['id','vendor_name','date_requested','po_total']:
                queryFields.insert(1,field)


    if queryFields == []:
        whereFields = None
        queryFields.append('id')
        queryFields.append('vendor_name')
        queryFields.append('date_requested')
        queryFields.append('po_total')

    ignore_fields = g_ignoreFields

    # Displays buttons at top of query_po form.
    if username!=None and db!=None:
        create_priv=1
    else:
        create_priv=0

    url='/%s/html/posum.html' % db_name
    queryFunctionButtons(create_priv, 1, url)

    del_priv=pmt_utils.hasPriv(db, username, 'del_po')
    dbResult,queryStatement=pmt_utils.executeQuery(db,
                                                    table_data,
                                                    'po',
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
        message="Could not retrieve po data from db.\n" + dbResult['message']
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
                                                          'po',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)
           
    if dbResult['status'] != 'success':
        message="Could not retrieve item to edit.\n" + dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'po', result[0])
    display_questionnaire(db,table_data, 'edit')
    pmt_utils.alertsArea(form, "Item data retrieved successfully")
    pmt_utils.textbox(None, 'direct_ra_signature',
                      table_data['po']['direct_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'indirect_ra_signature',
                      table_data['po']['indirect_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'department_exec_signature',
                      table_data['po']['department_exec_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'corporate_officer_signature',
                      table_data['po']['corporate_officer_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'po_math_checked_by_signature',
                      table_data['po']['po_math_checked_by_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_ordered_by_signature',
                      table_data['po']['purchase_ordered_by_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_received_by_signature',
                      table_data['po']['purchase_received_by_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'inv_math_checked_by_signature',
                      table_data['po']['inv_math_checked_by_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ap_entered_by_signature',
                      table_data['po']['ap_entered_by_signature']['value'],
                      '40', '40', None, None, 'hidden')

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % (db_name)
    editFunctionButtons(form["key_id"].value, listing_url,help_url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
    
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doCsvAll():

    status,table_data,db=pageInit("Export",formJS=0)

    if status != 'success':
        message="Can not connect to database.\n" + status
        exit(message)

    sql="SELECT id, po_number, revision_number, "
    sql=sql+"shipping_address, date_requested, "
    sql=sql+"date_needed_by, requisitioner_signature, payment_method, "
    sql=sql+"vendor_name, vendor_address, vendor_city_state_zip, "
    sql=sql+"vendor_contact, vendor_phone, vendor_fax, project_id, "
    sql=sql+"shipping_handling, tax_exempt, "
    sql=sql+"direct_project_charge_number, direct_project_charge_amount, "
    sql=sql+"direct_ra_signature, direct_ra_signature_date, "
    sql=sql+"indirect_proj_charge_number, indirect_proj_charge_amount, "
    sql=sql+"indirect_ra_signature, indirect_ra_signature_date, "
    sql=sql+"department_exec_signature, department_exec_sig_date, "
    sql=sql+"corporate_officer_signature, corporate_officer_sig_date, comments, "
    sql=sql+"po_math_checked_by_signature, purchase_ordered_by_signature, "
    sql=sql+"purchase_ordered_date, purchase_received_by_signature, "
    sql=sql+"purchase_received_date, date_invoice_received, invoice_number, "
    sql=sql+"invoice_date, inv_math_checked_by_signature, check_number, check_amount, "
    sql=sql+"check_date, check_mailed_date, ap_entered_by_signature from po ORDER by id, int4(id)"
    queryResult = pmt_utils.executeSQL(db, sql)

    if queryResult["status"] != 'success':
        message="Query failed.\n" + queryResult['message']
        exit(message)

    result = queryResult['result']

    print '<a href="/%s/html/%s">' % (db_name,'purchase_orderAll.csv')
    print 'Purchase Order File '
    print '(Right Click and select &quot;Save Link As&quot; to download)</a>'
    print '<BR><BR><B>The Comma Separated Values file contains the following'
    print 'fields for each record:</B>'
    print '<TABLE BORDER>'
    print '<TR><TD>Id</TD><TD>PO Number</TD><TD>Revision Number</TD>'
    print '<TD>Shipping Address</TD>'
    print '<TD>Date Requested</TD>'
    print '<TD>Date Needed By</TD><TD>Requisitioner Signature</TD><TD>Payment Method</TD>'
    print '<TD>Vendor Name</TD><TD>Vendor Address</TD>'
    print '<TD>Vendor Contact</TD><TD>Vendor Phone</TD>'
    print '<TD>Vendor Fax</TD><TD>Project ID</TD><TD>Line Item</TD><TD>Quantity</TD>'
    print '<TD>Description</TD><TD>Unit Price</TD>'
    print '<TD>Shipping & Handling</TD><TD>Tax Exempt</TD>'
    print '<TD>Direct Project Charge Number</TD>'
    print '<TD>Direct Project Charge Amount</TD><TD>Direct RA Signature</TD>'
    print '<TD>Direct RA Signature Date</TD><TD>Indirect Project Charge Number</TD>'
    print '<TD>Indirect Project Charge Amount</TD><TD>Indirect RA Signature</TD>'
    print '<TD>Indirect RA Signature Date</TD><TD>Department Executive Signature</TD>'
    print '<TD>Department Exec Signature Date</TD><TD>Corporate Officer Signature</TD>'
    print '<TD>Corporate Officer Signature Date</TD><TD>Comments</TD>'
    print '<TD>PO Math Checked By Signature</TD><TD>Purchase Ordered By Signature</TD>'
    print '<TD>Purchase Ordered Date</TD><TD>Purchase Received by Signature</TD>'
    print '<TD>Purchase Received Date</TD><TD>Date Invoice Received</TD>'
    print '<TD>Invoice Number</TD><TD>Invoice Date</TD>'
    print '<TD>Invoice Math Checked By Signature</TD><TD>Check Number</TD><TD>Check Amount</TD>'
    print '<TD>Check Date</TD><TD>Check Mailed Date</TD><TD>AP Entered By Signature</TD><TD>Property ID Number</TD>'
    print '<TD>Property ID Assigned By Signature</TD><TD>Date Property ID Assigned</TD>'
    print '<TD>Property Location</TD></TR></TABLE>'
    print 'NOTE: Commas in fields have been changed to whitespace'
    print '<BR><B>The contents of this Purchase Order Import file follows: </B>'
    print '<PRE>'

    output_lines = []
    for i in xrange(0, len(result)):
        po_completed = 'Open'
        if string.strip(result[i]['purchase_received_by_signature']) != '':
                po_completed = 'Closed'

        txt = string.replace(result[i]['id'],',','') + ','
        txt=txt+ string.replace(result[i]['po_number'],',','') + ','
        txt=txt+ string.replace(result[i]['revision_number'],',','') + ','
        txt=txt+ string.replace(result[i]['shipping_address'],',','') + ','
        txt=txt+ string.replace(result[i]['date_requested'],',','')+ ','
        txt=txt+ string.replace(result[i]['date_needed_by'],',','') + ','
        txt=txt+ string.replace(result[i]['requisitioner_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['payment_method'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_name'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_address'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_city_state_zip'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_contact'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_phone'],',','') + ','
        txt=txt+ string.replace(result[i]['vendor_ext'],',','')+ ','
        txt=txt+ string.replace(result[i]['vendor_fax'],',','') + ','
        txt=txt+ string.replace(result[i]['project_id'],',','') + ','
        txt=txt+ string.replace(result[i]['shipping_handling'],',','')+ ','
        txt=txt+ string.replace(result[i]['tax_exempt'],',','') + ','
        txt=txt+ string.replace(result[i]['direct_project_charge_number'],',','') + ','
        txt=txt+ string.replace(result[i]['direct_project_charge_amount'],',','') + ','
        txt=txt+ string.replace(result[i]['direct_ra_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['direct_ra_signature_date'],',','') + ','
        txt=txt+ string.replace(result[i]['indirect_proj_charge_number'],',','') + ','
        txt=txt+ string.replace(result[i]['indirect_proj_charge_amount'],',','') + ','
        txt=txt+ string.replace(result[i]['indirect_ra_signature'],',','')+ ','
        txt=txt+ string.replace(result[i]['indirect_ra_signature_date'],',','') + ','
        txt=txt+ string.replace(result[i]['department_exec_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['department_exec_sig_date'],',','') + ','
        txt=txt+ string.replace(result[i]['corporate_officer_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['corporate_officer_sig_date'],',','') + ','
        txt=txt+ string.replace(result[i]['comments'],',','') + ','
        txt=txt+ string.replace(result[i]['po_math_checked_by_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['purchase_ordered_by_signature'],',','')+ ','
        txt=txt+ string.replace(result[i]['purchase_ordered_date'],',','')+ ','
        txt=txt+ string.replace(result[i]['purchase_received_by_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['purchase_received_date'],',','') + ','
        txt=txt+ string.replace(result[i]['date_invoice_received'],',','') + ','
        txt=txt+ string.replace(result[i]['invoice_number'],',','') + ','
        txt=txt+ string.replace(result[i]['invoice_date'],',','') + ','
        txt=txt+ string.replace(result[i]['inv_math_checked_by_signature'],',','') + ','
        txt=txt+ string.replace(result[i]['check_number'],',','') + ','
        txt=txt+ string.replace(result[i]['check_amount'],',','') + ','
        txt=txt+ string.replace(result[i]['check_date'],',','') + ','
        txt=txt+ string.replace(result[i]['check_mailed_date'],',','')+ ','
        txt=txt+ string.replace(result[i]['ap_entered_by_signature'],',','')+ ','
        txt=txt+ po_completed
        txt = string.replace(txt,'\r\n',' ')
        txt = string.replace(txt,'\n',' ')
        print txt
        output_lines.append(txt)

        sql="SELECT  id, po_number, line_item, quantity, description, "
        sql=sql+"unit_price, property_id_number, prop_id_assigned_by_signature, "
        sql=sql+"date_property_id_assigned, property_location "
        sql=sql+"from inventory where po_id='%s' ORDER by id, int4(id)" % result[i]['id']
        itemsInPo = pmt_utils.executeSQL(db, sql)


        if itemsInPo['status'] != 'success':
            message='Query failed. \n' + itemsInPo['message']
            exit(message)

        itemsInPo = itemsInPo['result']

        for i in xrange(0, len(itemsInPo)):    
            txt = '   '+string.replace(itemsInPo[i]['id'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['po_number'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['line_item'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['quantity'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['description'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['unit_price'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['property_id_number'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['prop_id_assigned_by_signature'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['date_property_id_assigned'],',','') + ','
            txt=txt+ string.replace(itemsInPo[i]['property_location'],',','') + ','
            txt = string.replace(txt,'\r\n',' ')
            txt = string.replace(txt,'\n',' ')
            print txt
            output_lines.append(txt)        
    

    filename='/home/%s/html/purchase_orderAll.csv' % db_name
    file_io.writeToFile(filename,output_lines)
    print '</PRE>'

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    exportAllFunctionButtons(0,listing_url, '/%s/html/posum.html' % (db_name))
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    
    pageEnd(table_data,db)

#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doCsvOne():

    status,table_data,db=pageInit("Export",formJS=0)

    if status != 'success':
        message="Can not connect to database.\n" + status
        exit(message)

    sql="SELECT * FROM po WHERE id = '%s'" % (form['key_id'].value)
    queryResult = pmt_utils.executeSQL(db, sql)


    if queryResult["status"] != 'success':
        message="Query failed.\n" + dbResult['message']
        exit(message)

    result = queryResult['result']

    data={}
    data['po_number']={'size'   : 15,
                       'value'  : result[0]['po_number']}
    data['revision_number']=                {'size'   : 20,
                                             'value'  : result[0]['revision_number']}
    data['po_status']=                      {'size'   : 30,
                                             'value'  : result[0]['po_status']}
    data['shipping_address']=               {'size'   : 100,
                                             'value'  : result[0]['shipping_address']}
    data['date_requested']=                 {'size'   : 20,
                                             'value'  : result[0]['date_requested']}
    data['date_needed_by']=                 {'size'   : 20,
                                             'value'  : result[0]['date_needed_by']}
    data['requisitioner_signature']=        {'size'   : 40,
                                             'value'  : result[0]['requisitioner']}
    data['payment_method']=                 {'size'   : 20,
                                             'value'  : result[0]['payment_method']}
    data['line_item']=                      {'size'   : 20,
                                             'value'  : result[0]['line_item']}
    data['vendor_name']=                    {'size'   : 40,
                                             'value'  : result[0]['vendor_name']}
    data['vendor_address']=                 {'size'   : 100,
                                             'value'  : result[0]['vendor_address']}
    data['vendor_city_state_zip']=          {'size'   : 100,
                                             'value'  : result[0]['vendor_city_state_zip']}
    data['vendor_contact']=                 {'size'   : 40,
                                             'value'  : result[0]['vendor_contact']}
    data['vendor_phone']=                   {'size'   : 20,
                                             'value'  : result[0]['vendor_phone']}
    data['vendor_ext']=                     {'size'   : 20,
                                             'value'  : result[0]['vendor_ext']}
    data['vendor_fax']=                     {'size'   : 20,
                                             'value'  : result[0]['vendor_fax']}
    data['quote_number']=                   {'size'   : 20,
                                             'value'  : result[0]['quote_number']}
    data['shipping_handling']=              {'size'   : 25,
                                             'value'  : result[0]['shipping_handling']}
    data['tax_exempt']=                     {'size'   : 20,
                                             'value'  : result[0]['tax_exempt']}
    data['direct_project_charge_number']=   {'size'   : 35,
                                           'value'  : result[0]['direct_project_charge_number']}
    data['direct_project_charge_amount']=   {'size'   : 35,
                                           'value'  : result[0]['direct_project_charge_amount']}
    data['direct_project_charge_number2']=  {'size'   : 35,
                                           'value'  : result[0]['direct_project_charge_number2']}
    data['direct_project_charge_amount2']=  {'size'   : 35,
                                           'value'  : result[0]['direct_project_charge_amount2']}
    data['direct_ra_signature']=            {'size'   : 40,
                                             'value'  : result[0]['direct_ra_signature']}
    data['direct_ra_sig_date']=             {'size'   : 25,
                                             'value'  : result[0]['direct_ra_signature_date']}
    data['indirect_proj_charge_number']=    {'size'   : 35,
                                            'value'  : result[0]['indirect_proj_charge_number']}
    data['indirect_proj_charge_amount']=    {'size'   : 35,
                                            'value'  : result[0]['indirect_proj_charge_amount']}
    data['indirect_proj_charge_number2']=    {'size'   : 35,
                                            'value'  : result[0]['indirect_proj_charge_number2']}
    data['indirect_proj_charge_amount2']=    {'size'   : 35,
                                            'value'  : result[0]['indirect_proj_charge_amount2']}
    data['indirect_ra_signature']=          {'size'   : 40,
                                             'value'  : result[0]['indirect_ra_signature']}
    data['indirect_ra_sig_date']=           {'size'   : 30,
                                             'value'  : result[0]['indirect_ra_signature_date']}
    data['department_exec_signature']=      {'size'   : 40,
                                             'value'  : result[0]['department_exec_signature']}
    data['department_exec_sig_date']=       {'size'   : 35,
                                             'value'  : result[0]['department_exec_sig_date']}
    data['corporate_officer_signature']=    {'size'   : 40,
                                            'value'  : result[0]['corporate_officer_signature']}
    data['corporate_officer_sig_date']=     {'size'   : 35,
                                             'value'  : result[0]['corporate_officer_sig_date']}
    data['comments']=                       {'size'   : 100,
                                             'value'  : result[0]['comments']}
    data['po_math_checked_by_signature']=   {'size'   : 40,
                                           'value'  : result[0]['po_math_checked_by_signature']}
    data['purchase_ordered_by_signature']=  {'size'   : 40,
                                          'value'  : result[0]['purchase_ordered_by_signature']}
    data['purchase_ordered_date']=          {'size'   : 30,
                                             'value'  : result[0]['purchase_ordered_date']}
    data['purchase_received_by_signature']= {'size'   : 40,
                                         'value'  : result[0]['purchase_received_by_signature']}
    data['purchase_received_date']=         {'size'   : 30,
                                             'value'  : result[0]['purchase_received_date']}
    data['date_invoice_received']=          {'size'   : 30,
                                             'value'  : result[0]['date_invoice_received']}
    data['invoice_number']=                 {'size'   : 20,
                                             'value'  : result[0]['invoice_number']}
    data['invoice_date']=                   {'size'   : 20,
                                             'value'  : result[0]['invoice_date']}
    data['inv_math_checked_by_signature']=  {'size'   : 40,
                                          'value'  : result[0]['inv_math_checked_by_signature']}
    data['check_number']=                   {'size'   : 20,
                                             'value'  : result[0]['check_number']}
    data['check_date']=                     {'size'   : 20,
                                             'value'  : result[0]['check_date']}
    data['check_amount']=                   {'size'   : 20,
                                             'value'  : result[0]['check_amount']}
    data['check_mailed_date']=              {'size'   : 25,
                                             'value'  : result[0]['check_mailed_date']}
    data['ap_entered_by_signature']=        {'size'   : 40,
                                             'value'  : result[0]['ap_entered_by_signature']}

    print '<a href="/%s/html/%s">' % (db_name,'po_out.xls')
    print 'Purchase Order File '
    print '(Right Click and select &quot;Save Link As&quot; to download)</a>'
    print '<BR><BR><B>The Comma Separated Values file contains the following'
    print 'fields for each record:</B>'
    print '<TABLE BORDER>'
    print '<TR><TD>PO Number</TD><TD>Revision Number</TD><TD>PO Status</TD>'
    print '<TD>Shipping Address</TD>'
    print '<TD>Date Requested</TD>'
    print '<TD>Date Needed By</TD><TD>Requisitioner</TD><TD>Payment Method</TD><TD>Line Item</TD>'
    print '<TD>Vendor Name</TD><TD>Vendor Address</TD><TD>Vendor Address 2</TD>'
    print '<TD>Vendor Contact</TD><TD>Vendor Phone</TD><TD>Vendor Ext</TD>'
    print '<TD>Vendor Fax</TD><TD>Quote Number</TD>'
    print '<TD>Shipping & Handling</TD><TD>Tax Exempt</TD>'
    print '<TD>Direct Project Charge Number</TD><TD>Direct Project Charge Amount</TD>'
    print '<TD>Direct Project Charge Number2</TD><TD>Direct Project Charge Amount2</TD>'
    print '<TD>Direct RA Signature</TD>'
    print '<TD>Direct RA Signature Date</TD><TD>Indirect Project Charge Number</TD>'
    print '<TD>Indirect Project Charge Amount</TD><TD>Indirect Project Charge Number2</TD>'
    print '<TD>Indirect Project Charge Amount2</TD><TD>Indirect RA Signature</TD>'
    print '<TD>Indirect RA Signature Date</TD><TD>Department Executive Signature</TD>'
    print '<TD>Department Exec Signature Date</TD><TD>Corporate Officer Signature</TD>'
    print '<TD>Corporate Officer Signature Date</TD><TD>Comments</TD>'
    print '<TD>PO Math Checked By Signature</TD><TD>Purchase Ordered By Signature</TD>'
    print '<TD>Purchase Ordered Date</TD><TD>Purchase Received by Signature</TD>'
    print '<TD>Purchase Received Date</TD><TD>Date Invoice Received</TD>'
    print '<TD>Invoice Number</TD><TD>Invoice Date</TD>'
    print '<TD>Invoice Math Checked By Signature</TD><TD>Check Number</TD><TD>Check Amount</TD>'
    print '<TD>Check Date</TD><TD>Check Mailed Date</TD><TD>AP Entered By Signature</TD><TD>Project Id</TD>'
    print '<TD>Line Item</TD><TD>Quantity</TD><TD>Description</TD><TD>Unit Price</TD>'
    print '<TD>Property ID Number</TD>'
    print '<TD>Property ID Assigned By Signature</TD><TD>Date Property ID Assigned</TD>'
    print '<TD>Property Location</TD></TR></TABLE>'
    print 'NOTE: Commas in fields have been changed to whitespace'
    print '<BR><B>The contents of this Purchase Order Import file follows: </B>'
    print '<PRE>'

    output_lines = []

    po_completed = 'Open'
    if string.strip(result[0]['purchase_received_by_signature']) != '':
        po_completed = 'Closed'

    txt = string.replace(result[0]['po_number'],',','') + ','
    txt=txt+ string.replace(result[0]['revision_number'],',','') + ','
    txt=txt+ string.replace(result[0]['po_status'],',','') + ','
    txt=txt+ string.replace(result[0]['shipping_address'],',','') + ','
    txt=txt+ string.replace(result[0]['date_requested'],',','')+ ','
    txt=txt+ string.replace(result[0]['date_needed_by'],',','') + ','
    txt=txt+ string.replace(result[0]['requisitioner'],',','') + ','
    txt=txt+ string.replace(result[0]['payment_method'],',','') + ','
    txt=txt+ string.replace(result[0]['line_item'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_name'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_address'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_city_state_zip'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_contact'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_phone'],',','') + ','
    txt=txt+ string.replace(result[0]['vendor_ext'],',','')+ ','
    txt=txt+ string.replace(result[0]['vendor_fax'],',','') + ','
    txt=txt+ string.replace(result[0]['quote_number'],',','') + ','
    txt=txt+ string.replace(result[0]['shipping_handling'],',','')+ ','
    txt=txt+ string.replace(result[0]['tax_exempt'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_project_charge_number'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_project_charge_amount'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_project_charge_number2'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_project_charge_amount2'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_ra_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['direct_ra_signature_date'],',','') + ','
    txt=txt+ string.replace(result[0]['indirect_proj_charge_number'],',','') + ','
    txt=txt+ string.replace(result[0]['indirect_proj_charge_amount'],',','') + ','
    txt=txt+ string.replace(result[0]['indirect_proj_charge_number2'],',','') + ','
    txt=txt+ string.replace(result[0]['indirect_proj_charge_amount2'],',','') + ','
    txt=txt+ string.replace(result[0]['indirect_ra_signature'],',','')+ ','
    txt=txt+ string.replace(result[0]['indirect_ra_signature_date'],',','') + ','
    txt=txt+ string.replace(result[0]['department_exec_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['department_exec_sig_date'],',','') + ','
    txt=txt+ string.replace(result[0]['corporate_officer_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['corporate_officer_sig_date'],',','') + ','
    txt=txt+ string.replace(result[0]['comments'],',','') + ','
    txt=txt+ string.replace(result[0]['po_math_checked_by_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['purchase_ordered_by_signature'],',','')+ ','
    txt=txt+ string.replace(result[0]['purchase_ordered_date'],',','')+ ','
    txt=txt+ string.replace(result[0]['purchase_received_by_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['purchase_received_date'],',','') + ','
    txt=txt+ string.replace(result[0]['date_invoice_received'],',','') + ','
    txt=txt+ string.replace(result[0]['invoice_number'],',','') + ','
    txt=txt+ string.replace(result[0]['invoice_date'],',','') + ','
    txt=txt+ string.replace(result[0]['inv_math_checked_by_signature'],',','') + ','
    txt=txt+ string.replace(result[0]['check_number'],',','') + ','
    txt=txt+ string.replace(result[0]['check_amount'],',','') + ','
    txt=txt+ string.replace(result[0]['check_date'],',','') + ','
    txt=txt+ string.replace(result[0]['check_mailed_date'],',','')+ ','
    txt=txt+ string.replace(result[0]['ap_entered_by_signature'],',','')+ ','
    txt=txt+ po_completed
    txt = string.replace(txt,'\r\n',' ')
    txt = string.replace(txt,'\n',' ')
    print txt
    output_lines.append(txt)

    sql="SELECT  id, po_number, project_id, line_item, quantity, description, "
    sql=sql+"unit_price, property_id_number, prop_id_assigned_by_signature, "
    sql=sql+"date_property_id_assigned, property_location "
    sql=sql+"from inventory where po_id='%s'" % (form['key_id'].value)
    itemsInPo = pmt_utils.executeSQL(db, sql)


    if itemsInPo['status'] != 'success':
        message='Query failed. \n' + itemsInPo['message']
        exit(message)

    for i in xrange(0,10):
        data['project_id%d'%i]={'size':20,      'value':''}
        data['line_item%d'%i]={'size':20,        'value':''}
        data['quantity%d'%i]={'size':15,        'value':''}
        data['description%d'%i]={'size':100,     'value':''}
        data['unit_price%d'%i]={'size':20,   'value':''}
        data['property_id_number%d'%i]={'size':25,    'value':''}
        data['prop_id_assigned_by_signature%d'%i]={'size':40, 'value':''}
        data['date_property_id_assigned%d'%i]={'size':35, 'value':''}
        data['property_location%d'%i]={'size':50,'value':''}

    itemsInPo = itemsInPo['result']
    for i in xrange(0, len(itemsInPo)):    
        data['project_id%d'%i]['value']=itemsInPo[i]['project_id']
        data['line_item%d'%i]['value']=itemsInPo[i]['line_item']
        data['quantity%d'%i]['value']=itemsInPo[i]['quantity']
        data['description%d'%i]['value']=itemsInPo[i]['description']
        data['unit_price%d'%i]['value']=itemsInPo[i]['unit_price']
        data['property_id_number%d'%i]['value']=itemsInPo[i]['property_id_number']
        data['prop_id_assigned_by_signature%d'%i]['value']=itemsInPo[i]['prop_id_assigned_by_signature']
        data['date_property_id_assigned%d'%i]['value']=itemsInPo[i]['date_property_id_assigned']
        data['property_location%d'%i]['value']=itemsInPo[i]['property_location']
        txt = '   '+string.replace(itemsInPo[i]['project_id'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['line_item'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['quantity'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['description'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['unit_price'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['property_id_number'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['prop_id_assigned_by_signature'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['date_property_id_assigned'],',','') + ','
        txt=txt+ string.replace(itemsInPo[i]['property_location'],',','') + ','
        txt = string.replace(txt,'\r\n',' ')
        txt = string.replace(txt,'\n',' ')
        print txt
        output_lines.append(txt)

    exportToExcel(data) 
    filename='/home/%s/html/Sheet2.csv' % db_name
    file_io.writeToFile(filename,output_lines)
    print '</PRE>'

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    exportAllFunctionButtons(0,listing_url, '/%s/html/posum.html' % (db_name))

    #queryFunctionButtons(0,1, '/%s/html/posum.html' % (db_name))
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
                
    sqlStatement = "DELETE FROM po WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        onQueryLoad = "return displayWindow('Could not delete item data')"
    else:
        onQueryLoad = "return displayWindow('Item data successfully deleted')"


    sqlStatement = "DELETE FROM inventory WHERE po_id = '%s'" % (form["key_id"].value)
    pmt_utils.executeSQL(db, sqlStatement)

    db.close()
    query_po(1)
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def doSearch():
    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])
    db=dbResult['result']

    operator=form['operatorOption'].value
    value=form['searchValue'].value
    table_data=declarations.define_tables()
    for fieldName in table_data['po'].keys():
        if table_data['po'][fieldName]['label']==form['searchOption'].value:
            whereFields=["%s %s '%s'" % (fieldName,operator,value)]
            query_po(searchFields=[fieldName],searchWheres=whereFields)
            
            return
        
    exit("Search Error")

#----------------------------------------------------------------------


#----------------------------------------------------------------------
def itemDescriptionFunctionsHtml(db_key, po_id):

    # This function is used to execute the function buttons within the
    #   inv form that is within the po form.

    options = '<TD ALIGN=CENTER NOWRAP>'

    java="return goto_url('/%s-cgi-bin/inv_admin.pyc?action=edit&key_id=%s&return_to_po=1')" % (db_name, db_key)
    html='<INPUT NAME="editItem" type="button" value=" Edit " onClick="%s">' % java
    options = options + html

    #if priv==1:
    java="return goto_url('/%s-cgi-bin/po_admin.pyc?action=deleteItem&key_id=%s&return_to_po=1')" % (db_name, db_key)
    html='<INPUT NAME="deleteItem" type="button" value=" Delete " '
    html=html+'onClick="%s">' % java
    options = options + html

    java="return goto_url('/%s-cgi-bin/inv_admin.pyc?action=view&key_id=%s&return_to_po=1')" % (db_name, db_key)
    html='<INPUT NAME="viewItem" type="button" value=" View " onClick="%s">' % java
    options = options + html + "</TD>"
    
    print options
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def editItemFunctionButtons(db_key, menu_name, help_pdf=None):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    java="return execute('saveItem','%s')" % db_key
    html='<INPUT NAME="saveItem" type="button" value=" Save & Return to PO " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    print '</TR>'
    print '</TABLE>'
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doDeleteItem():

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

    sqlStatement = "SELECT po_id FROM inventory WHERE id = '%s'" % (form["key_id"].value)
    poIdResult = pmt_utils.executeSQL(db, sqlStatement)    
            
    sqlStatement = "DELETE FROM inventory WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success' or poIdResult['status'] != 'success':
        onQueryLoad = "return displayWindow('Could not delete item data')"
    else:
        onQueryLoad = "return displayWindow('Item data successfully deleted')"

    db.close()
    form["key_id"].value = poIdResult['result'][0]['po_id']
    doEdit()
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doDeleteAllItems(db, po_id):
            
    sqlStatement = "DELETE FROM inventory WHERE po_id = '%s'" % po_id
    pmt_utils.executeSQL(db, sqlStatement)

   
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doEditItem():

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
    display_questionnaireItems(db,table_data, 'edit')
    pmt_utils.alertsArea(form, "Item data retrieved successfully");

    pmt_utils.textbox(None, 'prop_id_assigned_by_signature',
                      table_data['inventory']['prop_id_assigned_by_signature']['value'],
                       '40', '40', None, None, 'hidden')

    #listing_url='/%s-cgi-bin/inv_admin.pyc?performDbQuery=1' % (db_name)
    #help_url='/%s/html/sprsum.html' % (db_name)
    #editItemFunctionButtons(form["key_id"].value, listing_url,help_url)

    print '<TABLE><TR><TD>'
    print '<FORM ACTION=https://lanux/home/save/cgi-bin/inv_admin.pyc?project_name=IFCS>'
    java="execute('save')"
    print '<INPUT TYPE=submit VALUE="Save" NAME=save onClick="%s" % java>'
    print '</FORM>'
    print '</TD></TR></TABLE>'

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pageEnd(table_data,db)
    
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def display_questionnaireItems(db, table_data, view):

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

        if table_data['inventory'][field_name].has_key('required') and \
           table_data['inventory'][field_name]['required'] == 1:
            required = 1
        else:
            required = 0
        
        print '<TR>'

        if field_name == 'analyst_username':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Analysis Approval --</B>' 
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'swm_completion_username':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Completion Approval --</B>'
            print '</TD>'
            print '</TR>'
            print '<TR>'
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'corrective_action':
            print '<TD COLSPAN=3><HR></TD></TR>'



        if view == 'read-only':
            if field_name in ['analyst_username',
                              'qa_completion_signature_function']:
                continue
        else:
            print '<TR>'
 
        pmt_utils.print_label(label=table_data['inventory'][field_name]['label'],
                              required=required)

        print '<TD>'
        pmt_utils.display_table_item_on_form(db,table_data,
                                             'inventory',
                                             field_name,
                                             editable=editable,
                                             display_item_only=1)
        print '</TD></TR>'

        if field_name == 'qa_completion_signature_function':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'

    print '</TABLE>'
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
        queryResult = pmt_utils.executeSQL(db, "SELECT NEXTVAL('po_id_seq')")

        form["key_id"].value = `queryResult['result'][0]['nextval']`
    
    table_data = pmt_utils.formToTableData(table_data,
                                           'po',
                                           form,
                                           form['key_id'].value)
    alerts = ''

    data=pmt_utils.process_signature(db,
                                    form['direct_ra_username'].value,
                                    form['direct_ra_password'].value,
                                    'Resource Authority',
                                    form['direct_ra_signature'].value,
                                    form['direct_ra_signature_function'].value)
    (status, details,
     table_data['po']['direct_ra_username']['value'],
     table_data['po']['direct_ra_password']['value'],
     table_data['po']['direct_ra_signature']['value'],
     table_data['po']['direct_ra_signature_function']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                  form['indirect_ra_username'].value,
                                  form['indirect_ra_password'].value,
                                  'Resource Authority',
                                  form['indirect_ra_signature'].value,
                                  form['indirect_ra_signature_function'].value)
    (status, details,
     table_data['po']['indirect_ra_username']['value'],
     table_data['po']['indirect_ra_password']['value'],
     table_data['po']['indirect_ra_signature']['value'], 
     table_data['po']['indirect_ra_signature_function']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                    form['department_exec_username'].value,
                                    form['department_exec_password'].value,
                                    'Department Executive',
                                    form['department_exec_signature'].value,
                                    form['department_exec_sig_function'].value)
    (status, details,
     table_data['po']['department_exec_username']['value'],
     table_data['po']['department_exec_password']['value'],
     table_data['po']['department_exec_signature']['value'],
     table_data['po']['department_exec_sig_function']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                     form['corporate_officer_username'].value,
                                     form['corporate_officer_password'].value,
                                     'Corporate Officer',
                                     form['corporate_officer_signature'].value,
                                     form['corp_officer_sig_function'].value)
    (status, details,
     table_data['po']['corporate_officer_username']['value'],
     table_data['po']['corporate_officer_password']['value'],
     table_data['po']['corporate_officer_signature']['value'],
     table_data['po']['corp_officer_sig_function']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                 form['po_math_checked_by_username'].value,
                                 form['po_math_checked_by_password'].value,
                                 'Accounting',
                                 form['po_math_checked_by_signature'].value,
                                 form['po_math_checked_by_sig_function'].value)
    (status, details,
     table_data['po']['po_math_checked_by_username']['value'],
     table_data['po']['po_math_checked_by_password']['value'],
     table_data['po']['po_math_checked_by_signature']['value'],
     table_data['po']['po_math_checked_by_sig_function']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                   form['purchase_ordered_by_username'].value,
                                   form['purchase_ordered_by_password'].value,
                                   'Accounting',
                                   form['purchase_ordered_by_signature'].value,
                                   form['purchase_ordered_by_sig_func'].value)
    (status, details,
     table_data['po']['purchase_ordered_by_username']['value'],
     table_data['po']['purchase_ordered_by_password']['value'],
     table_data['po']['purchase_ordered_by_signature']['value'],
     table_data['po']['purchase_ordered_by_sig_func']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                  form['purchase_received_by_username'].value,
                                  form['purchase_received_by_password'].value,
                                  'Analyst',
                                  form['purchase_received_by_signature'].value,
                                  form['purchase_received_by_sig_func'].value)
    (status, details,
     table_data['po']['purchase_received_by_username']['value'],
     table_data['po']['purchase_received_by_password']['value'],
     table_data['po']['purchase_received_by_signature']['value'],
     table_data['po']['purchase_received_by_sig_func']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                   form['inv_math_checked_by_username'].value,
                                   form['inv_math_checked_by_password'].value,
                                   'Accounting',
                                   form['inv_math_checked_by_signature'].value,
                                   form['inv_math_checked_by_sig_func'].value)
    (status, details,
     table_data['po']['inv_math_checked_by_username']['value'],
     table_data['po']['inv_math_checked_by_password']['value'],
     table_data['po']['inv_math_checked_by_signature']['value'],
     table_data['po']['inv_math_checked_by_sig_func']['value']) = data

    alerts = alerts + details

    data=pmt_utils.process_signature(db,
                                     form['ap_entered_by_username'].value,
                                     form['ap_entered_by_password'].value,
                                     'Accounting',
                                     form['ap_entered_by_signature'].value,
                                     form['ap_entered_by_sig_function'].value)
    (status, details,
     table_data['po']['ap_entered_by_username']['value'],
     table_data['po']['ap_entered_by_password']['value'],
     table_data['po']['ap_entered_by_signature']['value'],
     table_data['po']['ap_entered_by_sig_function']['value']) = data

    alerts = alerts + details

    
    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value, "po",
                                  " WHERE id = '%s'" % form["key_id"].value,
                                  form, 0, 0)

    if dbResult['status'] != 'success':
        message="Item could not be saved.\n" + dbResult['message']
        exit(message)

    if saveDueToCreate:
        subject='New PO #%s has been generated' % form['key_id'].value
       # message='PO #%s has been generated.\n\n' % form["key_id"].value
       # message=message+'Assigned to: %s\n\n' % form['assigned_to'].value
       # message=message+'Problem Description is as follows:\n'
       # message=message+'form['problem_description'].value+'\n\n'
       # message=message+'Log into the Purchase Order tracking tool at '
       # message=message+'http://www.isrparc.org for further info.'
       # message=message+'If you do not wish to be on this mailing list please '
       # message=message+'send an email requesting removal to cm@isrparc.org.\n'
       # pmt_utils.emailList(db,'localhost', 'po_list', subject, message)

    display_questionnaire(db,table_data, 'edit')

    alerts = alerts + '\nItem saved successfully'
    pmt_utils.alertsArea(form,alerts)

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % db_name
    editFunctionButtons(form["key_id"].value, listing_url, help_url)
    
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pmt_utils.textbox(None, 'direct_ra_signature',
                      table_data['po']['direct_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'indirect_ra_signature',
                      table_data['po']['indirect_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'department_exec_signature',
                      table_data['po']['department_exec_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'corporate_officer_signature',
                      table_data['po']['corporate_officer_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'po_math_checked_by_signature',
                   table_data['po']['po_math_checked_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_ordered_by_signature',
                   table_data['po']['purchase_ordered_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_received_by_signature',
                   table_data['po']['purchase_received_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'inv_math_checked_by_signature',
                   table_data['po']['inv_math_checked_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ap_entered_by_signature',
                   table_data['po']['ap_entered_by_signature']['value'], '40',
                   '40', None, None, 'hidden')

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

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % db_name
    pmt_utils.createFunctionButtons('create',listing_url,help_url)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    pmt_utils.textbox(None, 'direct_ra_signature',
                      table_data['po']['direct_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'indirect_ra_signature',
                      table_data['po']['indirect_ra_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'department_exec_signature',
                      table_data['po']['department_exec_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'corporate_officer_signature',
                      table_data['po']['corporate_officer_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'po_math_checked_by_signature',
                   table_data['po']['po_math_checked_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_ordered_by_signature',
                   table_data['po']['purchase_ordered_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'purchase_received_by_signature',
                   table_data['po']['purchase_received_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'inv_math_checked_by_signature',
                   table_data['po']['inv_math_checked_by_signature']['value'],
                   '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ap_entered_by_signature',
                   table_data['po']['ap_entered_by_signature']['value'],
                   '40', '40', None, None, 'hidden')

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
                                                          'po',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Item data could not be retrieved.\n" + dbResult['message']
        exit(message)
               
    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'po', result[0])
    display_questionnaire(db,table_data, 'read-only')

    listing_url='/%s-cgi-bin/po_admin.pyc?performDbQuery=1' % (db_name)
    help_url='/%s/html/sprsum.html' % (db_name)
    emailButton(username,form['key_id'].value,listing_url, help_url)
    pageEnd(table_data,db)
#----------------------------------------------------------------------


#----------------------------------------------------------------------
def doAddItem():


    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        msg='Could not connect to db.\n%s' % result['message']
        exit(msg)
        
    db=dbResult['result']

    sql="select nextval('inventory_id_seq')"
    result=pmt_utils.executeSQL(db,sql)

    if result['status']!='success':
        msg="Could not add item to inventory.\n%s" % result['message']
        exit(msg)

    item_id=result['result'][0]['nextval']

    fromCreate=0
    if form['po_id'].value=='':
        fromCreate=1   
        sql="select last_value, is_called from po_id_seq"
        result=pmt_utils.executeSQL(db,sql)
        if result['status']!='success':
            msg="Unable to get PO id from db.\n%s" % result['message']
            exit(msg)
        if int(result['result'][0]['last_value'])==1 and result['result'][0]['is_called']=='f':
            po_id=str(int(result['result'][0]['last_value'])+0)
        else:
            po_id=str(int(result['result'][0]['last_value'])+1)
    else:
        po_id=form['po_id'].value

    if form['description'].value!='' and form['quantity'].value!='' and form['unit_price'].value!='':
        sql="INSERT INTO inventory (id,po_id,project_id,part_number,description,quantity,unit_price,total_unit_price) "
        sql=sql+"VALUES ('%s','%s','%s','%s','%s','%s','%s','%.2f')" % (item_id,
                                             po_id,
                                             form['project_id'].value,
                                             form['part_number'].value,
                                             form['description'].value,
                                             form['quantity'].value,
                                             form['unit_price'].value,
                                             float(form['quantity'].value) * float(form['unit_price'].value))

        result=pmt_utils.executeSQL(db,sql)
        if result['status']!='success':
            message="Could not add item to inventory.\n%s" % result['message']
            exit(message)

        if fromCreate:
            form['key_id'].value='create'
            doSave()
        else:
            form['key_id'].value =po_id
            doSave()
        
    else:
        form['action'].value='blankFields'
        if fromCreate:
            doCreate()
        else:
            form['key_id'].value = po_id
            doEdit()
    

    
#----------------------------------------------------------------------

#----------------------------------------------------------------------
def exportToExcel(data):

    po_num=data['po_number']['value']
    if po_num=='':
        po_num='no_number'
    input=open('../html/po.xls','rb')
    output=open('../html/po_out.xls','wb')

    match=0
    continue_count=0
    buffer=input.read()
    for i in xrange(0,len(buffer)):
        # Skip characters until continue count==0
        if continue_count>0:
            continue_count=continue_count-1
            continue

        # If current character is an underscore
        if buffer[i]=='_':        
            # Check if the next few characters match a key in data
            for key in data.keys():
                length=len(key)+5
                excel_key='_var_%s' % key
                # If there is a match
                if buffer[i:i+length]==excel_key:
                    # Then write the value and pad the cell with spaces to
                    #   preserve file size, then set continue count to skip the
                    #   rest of the cell
                    value=data[key]['value']
                    size =data[key]['size']
                    output.write(value)
                    #padding=size-len(value)
                    #output.write(' '*padding)
                    continue_count=size-1
                    match=1
                    #print "Found '%s'" % (excel_key)
            # If a key matched, reset flag to 0
            if match:
                match=0
            else:
                # Otherwise no key matched, so write the underscore
                output.write(buffer[i])
        else:
            # Otherwise not an underscore, just write the character to the file
            output.write(buffer[i])

    input.close()
    output.close()
#----------------------------------------------------------------------


#----------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name = declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):

    if form["action"].value == "edit":
        doEdit()

    elif form["action"].value == "editItem":
        doEditItem()    

    elif form["action"].value == "query":
        query_po(1)

    elif form['action'].value == 'csv_all':
        doCsvAll()

    elif form['action'].value == 'csv_one':
        doCsvOne()

    elif form["action"].value == "delete":
        doDelete()

    elif form["action"].value == "deleteItem":

        doDeleteItem()

    elif form["action"].value == "deleteAllItems":
        doDeleteAllItems()

    elif form["action"].value == "save":
        doSave()

    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()
             
    elif form["action"].value == "add_item":        
        doAddItem()

    elif form["action"].value == "search":
        doSearch()

else:
    query_po(1)
#-------------------------------------------------------------------------


#-------------------------------------------------------------------------


























