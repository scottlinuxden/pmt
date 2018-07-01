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
    print '<SCRIPT TYPE="text/javascript">'
    print '<!--'
    print '  function popup(mylink, windowname,w,h)'
    print '  {'
    print '    if (! window.focus)'
    print '      return true;'
    print '    var href;'
    print "    if (typeof(mylink) == 'string')"
    print '      href=mylink;'
    print '    else'
    print '      href=mylink.href;'
    print '    LeftPosition=(screen.width)?(screen.width-w)/2:100;'
    print '    TopPosition=(screen.height)?(screen.height-h)/2:100;'
    settings="'width=' +w+ ',height=' +h+ ',top=' +TopPosition+ "
    settings=settings+"',left=' +LeftPosition+ ',scrollbars=yes'"
    print "    settings=%s" % settings
    print "popwindow=window.open(href, windowname, settings);"
    print "popWindow.focus()"
    print "return false;"
    print "}"
    print "//-->"
    print "</SCRIPT>"
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def emailButton(username,key,menu_name, help_pdf):
    link='/%s-cgi-bin/email.pyc' % declarations.pmt_info['db_name']
    link=link+'?table=ecp&key=%s&username=%s' % (key,username)
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    java="return goto_url('%s')" % menu_name
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing "'
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    if username!=None:
        java="return popup('%s','Email_Change_Proposal',600,500)" % link
	html='<input type="button" name="email" value=Email onClick="%s">'%java
        pmt_utils.tableColumn(html)
    java="return goto_url('%s')" % help_pdf
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
    print 'or <B>Bold</B> on Mononchrome Displays are Required</CAPTION>'
    print '<TR><TH>Field Name</TH><TH>Value</TH>'
    print '<TH>Format</TH>'

    print '</TR>'

    display_list = []

    field_name_keys = table_data['ecp'].keys()

    # build display list array
    for i in xrange(0,len(field_name_keys)):
        display_list.append("")

    # load display_list entries with table display order field_names
    for i in field_name_keys:
        display_list[int(table_data['ecp'][i]['display_order'])-1] = i

    field_name_keys = display_list

    for field_name in field_name_keys:

        if table_data['ecp'][field_name].has_key('required') and \
           table_data['ecp'][field_name]['required'] == 1:
            required = 1
        else:
            required = 0
        
        print '<TR>'

        if field_name == 'analyst_username':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Analysis Section --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'swm_completion_username':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Completion Approval --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'ccb_disposition':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- CCB Section --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'gccb_disposition':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- GCCB Section --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'test_plan':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Testing Section --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'disposition_received_date':
            print '<TD COLSPAN=3><HR></TD></TR><TR>'
            print '<TD ALIGN=CENTER COLSPAN=3>'
            print '<B>-- Disposition Section --</B></TD></TR>'
            print '<TR><TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'swm_analysis_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'swm_completion_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'qa_completion_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'ccb_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        elif field_name == 'gccb_username':
            print '<TD COLSPAN=3><HR></TD></TR>'

        if view == 'read-only':
            if field_name in ['analyst_username',
			      'analyst_password',
			      'analyst_signature_function',
			      'swm_analysis_username',
			      'swm_analysis_password',
			      'swm_analysis_signature_function',
			      'swm_completion_username',
			      'swm_completion_password',
			      'swm_completion_signature_function',
			      'ccb_username',
			      'ccb_password',
			      'ccb_signature_function',
			      'gccb_username',
			      'gccb_password',
			      'gccb_signature_function',
			      'qa_completion_username',
			      'qa_completion_password',
			      'qa_completion_signature_function']:
                continue
        else:
            print '<TR>'

        pmt_utils.print_label(label=table_data['ecp'][field_name]['label'],
				      required=required)

        print '<TD>'
        pmt_utils.display_table_item_on_form(db,table_data, 'ecp',
						     field_name,
						     editable=editable,
						     display_item_only=1)
        print '</TD></TR>'
    print '</TABLE>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
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
    java="return goto_url('%s')" % help_pdf
    html='<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR>'
    print '</TABLE>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def queryItemFunctionsHtml(arguments):
    db_key = arguments[0]
    originator = arguments[1]
    priv = arguments[4]

    options = '<TD ALIGN=CENTER NOWRAP>'
    java="return execute('edit','%s')" % db_key
    html='<INPUT NAME="edit" type="button" value=" Edit " onClick="%s">' % java
    options = options + html
    if priv==1:
        java="return execute('delete', '%s')" % db_key
        html='<INPUT NAME="delete" type="button" value=" Delete " '
        html=html+'onClick="%s">' % java
        options = options + html

    java="return execute('view','%s')" % db_key
    html='<INPUT NAME="view" type="button" value=" View " onClick="%s">' % java
    options=options + html + '</TD>'

    return options
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def editFunctionButtons(db_key, menu_name, help_pdf=None, priv=0):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'

    java="return execute('save','%s')" % db_key
    html='<INPUT NAME="save" type="button" value=" Save " onClick="%s">' % java
    pmt_utils.tableColumn(html)

    if priv==1:
        java="return execute('delete','%s')" % db_key
        html='<INPUT NAME="delete" type="button" value=" Delete " '
        html=html+'onClick="%s">' % java
        pmt_utils.tableColumn(html)
        
    java="return execute('view','%s')" % db_key
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
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def pageInit(subHeading=None,formJS=0):
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    if formJS:
        pmt_utils.generate_form_javascript(table_data,'ecp','ecp_admin',0)
    else:
        pmt_utils.javaScript("ecp_admin")
    pmt_utils.title("Engineering Change Proposal")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Engineering Change Proposal')
    if subHeading!=None:
        pmt_utils.subHeading(subHeading)
    pmt_utils.formSetup("ecp_admin",
                        declarations.pmt_info['db_name'],
			"ecp_admin",
			"return submitForm(document.ecp_admin)")

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
def exit(message,table_data=None,db=None,login_display=1):
    if login_display:
        pmt_utils.usernamePasswordDisplay()
    pmt_utils.alertsArea(form, message);

    if username!=None and db!=None:
        create_priv=pmt_utils.hasPriv(db,username,'create_ecp')
    else:
        create_priv=0
        
    queryFunctionButtons(create_priv,0, '/%s/html/ecpsum.html' % db_name)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
	    pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------




#-----------------------------------------------------------------------------
def query_ecp(performDbQuery=0, onLoad=None, queryFields=None):

    status, table_data, db = pageInit('Change Proposals',formJS=0)
    if status!='success':
        message="Cannot connect to db.\n%s" % status
        exit(message)

    status, details = db_authentication.password_valid(db,
				   crypt_salt=db_name,
				   username=username,
				   password=password)

    if status != 'success':
        exit(details)

    queryFields, whereFields = pmt_utils.getQueryWhereFields(form,
                                                             table_data,
                                                             'ecp')

    if queryFields == None or queryFields == []:
        queryFields = []
        whereFields = None
        queryFields.append('id')
        queryFields.append('change_name')
        queryFields.append('ecp_status')

    ignore_fields = ['analyst_signature_function',
		     'swm_analysis_signature_function',
		     'swm_completion_signature_function',
		     'ccb_signature_function',
		     'gccb_signature_function',
		     'qa_completion_signature_function']

    del_priv=pmt_utils.hasPriv(db,username, 'del_ecp')
    
    dbResult,queryStatement = pmt_utils.executeQuery(db,
						table_data,
						'ecp',
						queryFields,
						whereFields,
						'query',
						queryItemFunctionsHtml,
						 'ORDER by int4(id)',
						 ['id','originator'],
						 None,
						 ignore_fields,
						 "return execute('query')",
						 ["","",del_priv])

    if dbResult['status'] != 'success':
        message="Unable to get ECP data from db.\n" + dbResult['message']
        exit(message)

    message= "Last Query Statement: %s\n" % queryStatement
    message=message + `len(dbResult['result'])` + " items retrieved."
    exit(message,table_data,db,login_display=0)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doEdit():
    status,table_data,db=pageInit("Edit",formJS=1)

    if status != 'success':
	message="Could not connect to the database\n" + status
        exit(message.table_data,db)

    status, details = db_authentication.password_valid(db,
						       crypt_salt=db_name,
						       username=username,
						       password=password)

    if status != 'success':
        exit(details,table_data,db)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
							  'ecp',
							  form["key_id"].value)

    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Could not retrieve item.\n" + dbResult['message']
        exit(message,table_data,db)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'ecp', result[0])
    display_questionnaire(db,table_data, 'edit')
    pmt_utils.alertsArea(form, "Item data retrieved successfully");
        
    del_priv=pmt_utils.hasPriv(db,username,'del_ecp')
    list_url='/%s-cgi-bin/ecp_admin.pyc?performDbQuery=1' % (db_name)
    help_url="/%s/html/ecp_intro.html" % db_name
    editFunctionButtons(form["key_id"].value, list_url,help_url,del_priv)

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    
    pmt_utils.textbox(None, 'analyst_signature',
			  table_data['ecp']['analyst_signature']['value'],
			  '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_analysis_signature',
			  table_data['ecp']['swm_analysis_signature']['value'],
			  '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_completion_signature',
			table_data['ecp']['swm_completion_signature']['value'],
			'40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'gccb_signature',
			  table_data['ecp']['gccb_signature']['value'],
			  '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ccb_signature',
			  table_data['ecp']['ccb_signature']['value'],
			  '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'qa_completion_signature',
			 table_data['ecp']['qa_completion_signature']['value'],
			 '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'test_completion_signature',
                      table_data['ecp']['test_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pageEnd(table_data,db)


#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doDelete():
    
    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                   declarations.pmt_info['browser_password'],
                                   declarations.pmt_info['db_name'])
        
    if dbResult['status'] != 'success':
        onQueryLoad = 'displayWindow("Could not connect to the database")'
        return

    db = dbResult['result']

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)

    if status != 'success':
        exit(details)
                
    sqlStatement="DELETE FROM ecp WHERE id = '%s'" % (form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        onQueryLoad = "return displayWindow('Could not delete item data')"
    else:
        onQueryLoad = "return displayWindow('Item data has been deleted')"

    db.close()
    query_ecp(1)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doSave():

    saveDueToCreate = 0
        
    status,table_data,db =pageInit('Save',formJS=1)

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
        saveDueToCreate = 1
        sqlStatement="SELECT NEXTVAL('ecp_id_seq')"
        queryResult = pmt_utils.executeSQL(db, sqlStatement)

        form["key_id"].value = `queryResult['result'][0]['nextval']`

    table_data = pmt_utils.formToTableData(table_data,'ecp',
                                           form, form['key_id'].value)

    alerts = ''

    data = pmt_utils.process_signature(db,
                                      form['analyst_username'].value,
                                      form['analyst_password'].value,
                                      'Analyst',
                                      form['analyst_signature'].value,
                                      form['analyst_signature_function'].value)
    (status, details,
     table_data['ecp']['analyst_username']['value'],
     table_data['ecp']['analyst_password']['value'],
     table_data['ecp']['analyst_signature']['value'],
     table_data['ecp']['analyst_signature_function']['value']) = data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                                 form['swm_analysis_username'].value,
                                 form['swm_analysis_password'].value,
                                 'Software Manager',
                                 form['swm_analysis_signature'].value,
                                 form['swm_analysis_signature_function'].value)
    (status, details,
     table_data['ecp']['swm_analysis_username']['value'],
     table_data['ecp']['swm_analysis_password']['value'],
     table_data['ecp']['swm_analysis_signature']['value'],
     table_data['ecp']['swm_analysis_signature_function']['value']) = data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                               form['swm_completion_username'].value,
                               form['swm_completion_password'].value,
                               'Software Manager',
                               form['swm_completion_signature'].value,
                               form['swm_completion_signature_function'].value)
    (status, details,
     table_data['ecp']['swm_completion_username']['value'],
     table_data['ecp']['swm_completion_password']['value'],
     table_data['ecp']['swm_completion_signature']['value'],
     table_data['ecp']['swm_completion_signature_function']['value']) =data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                                       form['ccb_username'].value,
                                       form['ccb_password'].value,
                                       'CCB Manager',
                                       form['ccb_signature'].value,
                                       form['ccb_signature_function'].value)
    (status, details,
     table_data['ecp']['ccb_username']['value'],
     table_data['ecp']['ccb_password']['value'],
     table_data['ecp']['ccb_signature']['value'],
     table_data['ecp']['ccb_signature_function']['value']) = data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                                       form['gccb_username'].value,
                                       form['gccb_password'].value,
                                       'GCCB Manager',
                                       form['gccb_signature'].value,
                                       form['gccb_signature_function'].value)
    (status, details,
     table_data['ecp']['gccb_username']['value'],
     table_data['ecp']['gccb_password']['value'],
     table_data['ecp']['gccb_signature']['value'],
     table_data['ecp']['gccb_signature_function']['value']) = data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                                form['qa_completion_username'].value,
                                form['qa_completion_password'].value,
                                'QA Manager',
                                form['qa_completion_signature'].value,
                                form['qa_completion_signature_function'].value)
    (status, details,
     table_data['ecp']['qa_completion_username']['value'],
     table_data['ecp']['qa_completion_password']['value'],
     table_data['ecp']['qa_completion_signature']['value'],
     table_data['ecp']['qa_completion_signature_function']['value']) = data

    alerts = alerts + details

    data = pmt_utils.process_signature(db,
                                form['test_completion_username'].value,
                                form['test_completion_password'].value,
                                'Test Manager',
                                form['test_completion_signature'].value,
                                form['test_completion_signature_function'].value)
    (status, details,
     table_data['ecp']['test_completion_username']['value'],
     table_data['ecp']['test_completion_password']['value'],
     table_data['ecp']['test_completion_signature']['value'],
     table_data['ecp']['test_completion_signature_function']['value']) = data

    alerts = alerts + details

    dbResult = pmt_utils.saveForm(table_data, db,
                                  form['key_id'].value, "ecp",
                                  " WHERE id = '%s'" % form["key_id"].value,
                                  form, echoStatement=0, fromForm=0)

    if dbResult['status'] != 'success':
        message="Item could not be saved.\n" + dbResult['message']
        exit(message)

    display_questionnaire(db,table_data, 'edit')


    alerts = alerts + '\nItem saved successfully'
    pmt_utils.alertsArea(form,alerts)

    if saveDueToCreate:
        subject='New ECP #%s has been generated' % (form['key_id'].value)
        message='ECP #%s has been generated.\n\n' % (form["key_id"].value)
        message=message+'Log into the Engineering Change Proposal tracking '
        message=message+'tool at http://www.isrparc.org for further info.\n\n'
        message=message+'Change Description is as follows:\n'
        message=message+'   %s\n\n' % form['change_description'].value
        message=message+'If you do not wish to be on this mailing list please '
        message=message+'send an email requesting removal to cm@isrparc.org.\n'
 
        pmt_utils.emailList(db,'localhost', 'ecp_list', subject, message)


    # generate function button row
    listing_url='/%s-cgi-bin/ecp_admin.pyc?performDbQuery=1' % (db_name)
    help_url="/%s/html/ecpsum.html" % db_name
    editFunctionButtons(form["key_id"].value, listing_url, help_url)
           
    # generate hidden fields for form
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    pmt_utils.textbox(None, 'analyst_signature',
                      table_data['ecp']['analyst_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_analysis_signature',
                      table_data['ecp']['swm_analysis_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_completion_signature',
                      table_data['ecp']['swm_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ccb_signature',
                      table_data['ecp']['ccb_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'gccb_signature',
                      table_data['ecp']['gccb_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'qa_completion_signature',
                      table_data['ecp']['qa_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'test_completion_signature',
                      table_data['ecp']['test_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pageEnd(table_data,db)

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doCreate():

    status,table_data,db = pageInit('Create',formJS=1)

    if status != 'success':
        message="Item could not be created.\n" + status
        exit(message)

    # initialize form data values to zero or blank and set origination date
    table_data = pmt_utils.init_table_data(table_data,'ecp')
    now = time_pkg.current_time_MM_DD_YYYY()
    table_data['ecp']['origination_date']['value'] = now

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)

    display_questionnaire(db,table_data, 'edit')
                
    # display alerts area to create
    message="Enter information on form and depress Create button"
    pmt_utils.alertsArea(form,message)

    # create functions button row
    listing_url='/%s-cgi-bin/ecp_admin.pyc?performDbQuery=1' % (db_name)
    help_url="/%s/html/ecp_intro.html" % db_name
    pmt_utils.createFunctionButtons('create', listing_url, help_url)
    
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    
    pmt_utils.textbox(None, 'analyst_signature',
                      table_data['ecp']['analyst_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_analysis_signature',
                      table_data['ecp']['swm_analysis_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'swm_completion_signature',
                      table_data['ecp']['swm_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'ccb_signature',
                      table_data['ecp']['ccb_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'gccb_signature',
                      table_data['ecp']['gccb_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'qa_completion_signature',
                      table_data['ecp']['qa_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pmt_utils.textbox(None, 'test_completion_signature',
                      table_data['ecp']['test_completion_signature']['value'],
                      '40', '40', None, None, 'hidden')
    pageEnd(table_data,db)

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doView():

    status,table_data,db = pageInit('View',formJS=1)

    if status != 'success':
        message="Could not connect to db.\n" + status
        exit(message)

    status, details = db_authentication.password_valid(db,
                                                       crypt_salt=db_name,
                                                       username=username,
                                                       password=password)
        
    if status != 'success':
        exit(details)

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,'ecp',
                                                          form["key_id"].value)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        message="Item data could not be retrieved.\n" + dbResult['message']
        exit(message)

    result = dbResult['result']
    table_data = pmt_utils.dbToTableData(table_data, 'ecp', result[0])
    display_questionnaire(db,table_data, 'read-only')

    listing_url='/%s-cgi-bin/ecp_admin.pyc?performDbQuery=1' % (db_name)
    help_url="/%s/html/ecpsum.html" % db_name
            
    emailButton(username,form['key_id'].value,listing_url,help_url)
    pageEnd(table_data,db)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']

username,password=pmt_utils.getUserPass(form)

if form.has_key("action"):
    if form["action"].value == "edit":
        doEdit()
        
    elif form["action"].value == "query":
        query_ecp(1)

    elif form["action"].value == "delete":
        doDelete()

    elif form["action"].value == "save":
        doSave()

    elif form["action"].value == "create":
        doCreate()

    elif form["action"].value == "view":
        doView()

else:
    query_ecp(0)
