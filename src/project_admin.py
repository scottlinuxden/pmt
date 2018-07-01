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
import db_authentication

#-----------------------------------------------------------------------------
def project_adminButtons(button_name):
    print '<HR>'
    print '<TABLE>'
    print '<TR>'
    if button_name == 'edit':
        parms="'edit','1'"
        html_text='<INPUT NAME="edit" type="button" value=" Edit " '
        html_text=html_text+'onClick="return execute(' + parms + ')">'
        pmt_utils.tableColumn(html_text)
    elif button_name == 'save':
        parms="'save','1'"
        html_text='<INPUT NAME="save" type="button" value=" Save " '
        html_text=html_text+'onClick="return execute(' + parms + ')">'
        pmt_utils.tableColumn(html_text)
    help_url="'%s'" % declarations.pmt_info['help_file']
    html_text='<INPUT TYPE="button" NAME="help" VALUE=" Help " '
    html_text=html_text+'onClick="return goto_url (' + help_url + ')">'
    pmt_utils.tableColumn(html_text)
    print '</TR>'
    print '</TABLE>'
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def edit_project_info(performDbQuery=0, onLoad=None, queryFields=None):

    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.javaScript("project_admin")
    pmt_utils.title("Project Administration")
    print "</HEAD>"

    pmt_utils.bodySetup(onLoad)
    pmt_utils.mainHeading('Project Administration')
    pmt_utils.subHeading('Project Info')
    pmt_utils.formSetup("project_admin",db_name,"project_admin",
			"return submitForm(document.project_admin)")

    if username==None:
        pmt_utils.usernamePasswordDisplay()
        project_adminButtons(button_name='edit')
        pmt_utils.textbox(None, 'key_id', '1', '10', '10', None, None,'hidden')
        pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
        pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
        print "</FORM>"
        try:
            pmt_utils.trailer(table_data, db)
            db.close()
        except NameError:
            pass
        print "</BODY>"
        print "</HTML>"
        return

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				   declarations.pmt_info['browser_password'],
				   declarations.pmt_info['db_name'])

    # could not connect to db
    if dbResult['status'] != 'success':
        pmt_utils.alertsArea(form, "Can not connect to database,\n" + dbResult['message'])
        project_adminButtons()
        print "</FORM>"
        try:
            pmt_utils.trailer(table_data, db)
            db.close()
        except NameError:
            pass
        print "</BODY>"
        print "</HTML>"
        return

    db = dbResult['result']
    status, details = db_authentication.password_valid(db,crypt_salt=db_name,
						       username=username,
						       password=password)
        
    if status != 'success':
        print '<form method=post action=/%s-cgi-bin/project_admin.pyc>'%db_name
        pmt_utils.usernamePasswordDisplay(username)
        pmt_utils.alertsArea(form,'Can not verify you as a valid user')
        print '<hr><input name=reload type=submit value="Query">'
        print '<input name=action value=edit type=hidden>'
        print '</form>'
        sys.exit()

    if pmt_utils.hasPriv(db,username,'project_data')!=1:
        print '<form method=post action=/%s-cgi-bin/project_admin.pyc>'%db_name
        pmt_utils.usernamePasswordDisplay(username)
        msg='User %s does not have project admin privileges>' % username
        pmt_utils.alertsArea(form,msg)
        print '<hr><input name=reload type=submit value="Query">'
        print '<input name=action value=edit type=hidden>'
        print '</form>'
        sys.exit()

    if form.has_key('key_id'):
        key_id=form['key_id'].value
    else:
        key_id='1'
    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'project_info',
                                                          key_id)
    dbResult = pmt_utils.executeSQL(db, sqlStatement)
    if dbResult['status'] != 'success':
        msg="Could not retrieve project information\n" + dbResult['message']
        pmt_utils.alertsArea(form, msg);
    else:
        result = dbResult['result']
        table_data = pmt_utils.dbToTableData(table_data,
                                             'project_info',
                                             result[0])
        table_data['project_info']['id']['value'] = '1'
        pmt_utils.display_form(table_data,'project_info',1,'useValues',1,db)
        pmt_utils.alertsArea(form,"Project Information retrieved successfully")

    project_adminButtons(button_name='save')
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')

    print "</FORM>"
    try:
        pmt_utils.trailer(table_data, db)
        db.close()
    except NameError:
        pass

    print "</BODY>"
    print "</HTML>"
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doSave():
    table_data = declarations.define_tables()

    print "<HTML>"
    print "<HEAD>"

    pmt_utils.generate_form_javascript(table_data,'project_info',
                                       'project_admin',0)
    pmt_utils.title("Project Info Administration")

    print "</HEAD>"

    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Project Info Administration')
    pmt_utils.subHeading('Edit Project Info')
    pmt_utils.formSetup("project_admin",db_name,"project_admin",
			"return submitForm(document.project_admin)")
    
    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				   declarations.pmt_info['browser_password'],
				   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        msg="Project Info could not be saved, could not connect to db\n"
        pmt_utils.alertsArea(form,msg+dbResult['message'])
        # generate function button row
        project_adminButtons('save')

        # generate hidden fields for form
        pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
        pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
        pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
        print "</FORM>"
        pmt_utils.trailer(table_data, db)
        db.close()
        print "</BODY>"
        print "</HTML>"
        return

    db = dbResult['result']

    # save the Form
    dbResult = pmt_utils.saveForm(table_data, db, None,
                                  "project_info", " WHERE id = '1'", form)

    # if the form was not successfully saved
    if dbResult['status'] != 'success':
        msg="Project Info could not be saved due to an error during save,\n"
        pmt_utils.alertsArea(form, msg + dbResult['message'] )
    else:
        table_data = declarations.define_tables()
        table_data = pmt_utils.formToTableData(table_data,'project_info', form)
        table_data['project_info']['id']['value'] = '1'
        pmt_utils.display_form(table_data,'project_info',1, 'useValues', 1, db)
        pmt_utils.alertsArea(form,"Project Info successfully saved")

    # generate function button row
    project_adminButtons('save')

    # generate hidden fields for form
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"

#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
def doEdit():
    table_data = declarations.define_tables()
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.generate_form_javascript(table_data,'project_info',
                                       'project_admin',0)
    pmt_utils.title("Project Info Administration")
    print "</HEAD>"

    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Project Info Administration')
    pmt_utils.subHeading('Edit Project Info')
    pmt_utils.formSetup("project_admin",db_name,"project_admin",
                "return submitForm(document.project_admin)")

    dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				   declarations.pmt_info['browser_password'],
				   declarations.pmt_info['db_name'])

    if dbResult['status'] != 'success':
        msg="Could not connect to the database\n"
        pmt_utils.alertsArea(form, msg + dbResult['message']);
        sys.exit()

    db = dbResult['result']
    status, details = db_authentication.password_valid(db,crypt_salt=db_name,
						       username=username,
						       password=password)
    if status != 'success':
        print '<form method=post action=/%s-cgi-bin/project_admin.pyc>'%db_name
        pmt_utils.usernamePasswordDisplay(username)
        pmt_utils.alertsArea(form,'Can not verify you as a valid user')
        print '<hr><input name=reload type=submit value="Query">'
        print '<input name=action value=edit type=hidden>'
        print '</form>'
        sys.exit()

    if pmt_utils.hasPriv(db,username,'project_data')!=1:
        print '<form method=post action=/%s-cgi-bin/project_admin.pyc>'%db_name
        pmt_utils.usernamePasswordDisplay(username)
        msg='User %s does not have project admin privileges' % username
        pmt_utils.alertsArea(form,msg)
        print '<hr><input name=reload type=submit value="Query">'
        print '<input name=action value=edit type=hidden>'
        print '</form>'
        sys.exit()

    sqlStatement = pmt_utils.selectAllColumnsSqlStatement(table_data,
                                                          'project_info','1')
    dbResult = pmt_utils.executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':
        msg="Could not retrieve project info to edit\n"
        pmt_utils.alertsArea(form, msg + dbResult['message']);
    else:
        result = dbResult['result']
        table_data = pmt_utils.dbToTableData(table_data,
                                             'project_info', result[0])
        table_data['project_info']['id']['value'] = '1'
        pmt_utils.display_form(table_data, 'project_info', 1,
                               'useValues', 1, db)
        pmt_utils.alertsArea(form, "Project Info retrieved successfully");

    project_adminButtons('save')
    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
username,password=pmt_utils.getUserPass(form)
db_name=declarations.pmt_info['db_name']

if form.has_key("action"):
    if form["action"].value == "edit":
        doEdit()
    elif form["action"].value == "save":
        doSave()
else:
    edit_project_info(1)
