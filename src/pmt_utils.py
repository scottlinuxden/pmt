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
import types
import file_io
from pg import DB
import _pg
import types
import StringIO, smtplib
from passwdCookie import *
import sha
from mod_python import apache,util

pmt_site = '12.180.241.12'   # www.wavefish.com

debugOn = 0
debugReq=None

def debug(output):
    global debugOn
    if debugOn:
        debugReq.write('DEBUG: %s<BR>' % (output))

def getUserPass(form=None):
    loginCookie = authCookie()
    username,password=loginCookie.get()

    if username==None:
        if form==None:
            return None,None
        if form.has_key('username'):
            username=form['username'].value
            password=sha.new(form['password'].value).digest()
        else:
            return None,None

    return username,password

def process_signature(db, username, password, role, signature, signature_function):

    if string.strip(username) == '' and string.strip(password) == '':
        #return ('success', '', username, password, '', 'Sign')
        return ('success', '', '', '', signature, 'Sign')

    dbResult = executeSQL(db, "SELECT member_role, first_name, last_name FROM project_members WHERE member_username = '%s' and member_password = '%s'" % (username, password))

    if dbResult['status'] != 'success':
        #return ('error', 'Invalid username or password for %s\n' % (role), username, password, '', 'Sign')
        return ('error', 'Invalid username or password for %s\n' % (role), '', '', signature, 'Sign')

    else:
        result = dbResult['result']

        if result == []:

            return ('error', 'Invalid username or password for %s\n' % (role),'', '', signature, 'Sign')

        if (role != 'Analyst'):

            if role != result[0]['member_role']:

                return ('error', 'You are not a member of the %s role.\n' % (role),'','', signature, 'Sign')

            else:

                if signature_function == 'Sign':
                    username = username
                    password = password
                    signature = '%s %s' % (result[0]['first_name'],result[0]['last_name'])
                    signature_function = 'Sign'

                elif signature_function == 'Erase':
                    username = ''
                    password = ''
                    signature = ''
                    signature_function = 'Sign'

                #return ('success', '%s signature processed.\n' % (role), username, password, signature, signature_function)
                return ('success', '%s signature processed.\n' % (role), '', '', signature, signature_function)

        else:

            if signature_function == 'Sign':
                username = username
                password = password

                signature = '%s %s' % (result[0]['first_name'],result[0]['last_name'])
                signature_function = 'Sign'

            elif signature_function == 'Erase':

                username = ''
                password = ''
                signature = ''
                signature_function = 'Sign'

            #return ('success', '%s signature processed\n' % (role), username, password, signature, signature_function)
            return ('success', '%s signature processed\n' % (role), '', '', signature, signature_function)

def exec_sql_file(db, filename):

    status, sql_commands = file_io.readFromFile(filename)

    exec_sql_commands = []

    for index in xrange(0,len(sql_commands)):
        sql_commands[index] = string.strip(sql_commands[index])
        if sql_commands[index] == '' or sql_commands[index][:1] == '#':
            continue
        elif sql_commands[index][:4] == 'COPY':
            exec_sql_commands.append(os.path.expandvars(sql_commands[index]))
        else:
            exec_sql_commands.append(sql_commands[index])

    queryResult = executeSqlItemList(req,db, exec_sql_commands, 1,1)

    if queryResult["status"] != 'success':
        req.write(queryResult)
        req.write("Failed to execute all sql statements")
        sys.exit(1)                                                                    	

def escape_quote(s):
    if string.find(s,"'") == -1:
        return s
    else:
        return string.replace(s, "'", "\\'")

def send_email(mailserver, from_address, recipients, subject, content):

    recipient_list = ''
    raw_string=0
    for i in recipients:
        if len(i)>1:
            recipient_list = recipient_list + i+', '
        else: raw_string=1

    if raw_string==1:
        recipient_list=recipients

    recipient_list = recipient_list[:-2]

    out=StringIO.StringIO()
    out.write("Subject: %s\n" % subject)
    out.write("To: %s\n\n" % recipient_list)
    out.write(content)

    mail=smtplib.SMTP(mailserver)


    mail.sendmail(
            from_addr=from_address,
            to_addrs=recipients,
            msg=out.getvalue())

"""
Global definitions for this module
queryResult ->
    {'status' : [error|success], 'message' : string, 'result' : [rows returned by query|None]}
"""

def sort(list, field):
    res = []
    for x in list:
        i = 0
        for y in res:
            if x[field] <= y[field]: break
            i = i + 1
        res[i:i] = [x]
    return res

def mainHeading(req, topic):
    """
    Generates the Main Header HTML
    """
    req.write('<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="darkRed"><B>' + topic + '</B></FONT><BR>')

def subHeading(req, topic):
    """
    Generates a Sub Heading HTML
    """
    req.write('<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="blue"><B><i>' + topic + '</i></B></FONT><BR>')

def printText(req,text,color='blue'):
    """
    Prints all text in a specified font
    """
    req.write('<FONT FACE="Arial,Helvetica" SIZE="-1" COLOR="' + color + '">' + text + '</FONT><BR>')

def bodySetup(req,onLoad=None,bgColor='#B7BAB7',textColor='#000000'):
    """
    Generates the BODY tag for an HTML page with the optional onLoad specifier
    to execute a JavaScript function when the page loads
    """
    req.write('<BODY BGCOLOR="' + bgColor + '" TEXT="' + textColor + '"')
    req.write(' background="/icons/circ_bg.jpg" ')
    if onLoad != None:
        req.write(' onLoad="' + onLoad + '"')
    req.write('>')

def buildColumnDeclaration(table_name, column_name, table_data):
    """
    Builds a column declaration to be used in a create table statement
    """
    sqlStatement = column_name + " "

    debug(table_data[table_name][column_name])

    if (table_data[table_name][column_name]["type"] == 'VARCHAR') or (table_data[table_name][column_name]["type"] == 'DECIMAL'):

        sqlStatement = sqlStatement + table_data[table_name][column_name]["type"] + "(" + table_data[table_name][column_name]["db_size"] + ")"

    else:
        sqlStatement = sqlStatement + table_data[table_name][column_name]["type"]

    if table_data[table_name][column_name]["default"] != None:

        if (table_data[table_name][column_name]["type"] == 'VARCHAR') or \
           (table_data[table_name][column_name]["type"] == 'DECIMAL') or \
           (table_data[table_name][column_name]["type"] == 'BOOL'):

            sqlStatement = sqlStatement + " DEFAULT '" + table_data[table_name][column_name]["default"] + "'" 

        else:
            sqlStatement = sqlStatement + " DEFAULT " + table_data[table_name][column_name]["default"]

    if column_name == 'id':

        if table_data[table_name][column_name].has_key('db_constraints'):
            sqlStatement = sqlStatement + " " + table_data[table_name][column_name]['db_constraints']
        else:
            sqlStatement = sqlStatement + " NOT NULL UNIQUE PRIMARY KEY"

    return sqlStatement

def saveForm(table_data, db, key, table_name, where_clause, form, echoStatement=0, fromForm=1,insert_regardless=0):
    """
    Will save field data in form or table_data which is designated by the
    fromForm argument which if it is 0 the save is performed from table_data
    else if it is 1 the save is done from form.  That has the same names of
    the fields in
    table_name found in table_data.  The where_clause specifies what rows 
    should be updated or if row does not exist an insert is performed on table.
    if echoStatement == 1 then the sql statement that is performed for the
    save of the form data is echoed to standard output.  The db argument is
    an already open database connection.  The key argument is the database key
    or id that is used for an insert should the row not already exist.  If
    any of the form fields are numeric fields and the field value is blank
    then the blank field value is converted to int4 -> 0, float4 -> 0.0,
    decimal -> 0.00 in order to be saved to the database.
    the result of the save is returned as a queryResult dictionary value, see
    top of file for return type
    """

    if fromForm:
        keyitems = form.keys()
    else:
        keyitems = table_data[table_name].keys()

    if not insert_regardless:
        sqlStatement = "SELECT count(*) FROM " + table_name + " " + where_clause

        queryResult = executeSQL(db, sqlStatement)

        result = queryResult['result']

        rows_which_match = result[0]["count"]

    else:
        rows_which_match = 0

    if rows_which_match > 0:

        # row exists perform an update of data
        sqlStatement = "UPDATE " + table_name + " SET "

        for i in keyitems:

            if table_data[table_name].has_key(i):

                sqlStatement = sqlStatement + i + " = "

                # if the type of the field is varchar, date, or boolean
                if (table_data[table_name][i]["type"] == 'VARCHAR') or (table_data[table_name][i]["type"] == 'DATE') or (table_data[table_name][i]["type"] == 'BOOL'):

                    # if the field is a boolean
                    if table_data[table_name][i]["type"] == 'BOOL':

                        if fromForm:
                            if string.lower(form[i].value) == 'yes':
                                sqlStatement = sqlStatement + "'t', "
                            elif string.lower(form[i].value) == 'no':
                                sqlStatement = sqlStatement + "'f', "
                        else:

                            if string.lower(table_data[table_name][i]['value']) == 'yes':
                                sqlStatement = sqlStatement + "'t', "
                            elif string.lower(table_data[table_name][i]['value']) == 'no':
                                sqlStatement = sqlStatement + "'f', "

                    # else field is not a boolean field
                    else:

                        if fromForm:
                            if string.strip(form[i].value) == '':
                                sqlStatement = sqlStatement + "NULL, "
                            else:
                                sqlStatement = sqlStatement + "'" + escape_quote(form[i].value) + "', "

                        else:
                            if string.strip(table_data[table_name][i]['value']) == '':
                                sqlStatement = sqlStatement + "NULL, "
                            else:
                                sqlStatement = sqlStatement + "'" + escape_quote(table_data[table_name][i]['value']) + "', "

                # else field is not a varchar, boolean, or date
                else:

                    if fromForm:
                        if string.strip(form[i].value) == '':
                            sqlStatement = sqlStatement + "NULL, "
                        else:
                            sqlStatement = sqlStatement + form[i].value + ", "

                    else:
                        if string.strip(table_data[table_name][i]['value']) == '':
                            sqlStatement = sqlStatement + "NULL, "
                        else:
                            sqlStatement = sqlStatement + table_data[table_name][i]['value'] + ", "

        # remove last comma
        sqlStatement = sqlStatement[:-2]

        if where_clause != None:
            sqlStatement = sqlStatement + where_clause

    else:

        # row does not exist so insert
        sqlStatement = "INSERT INTO " + table_name + " ("

        if key != None and fromForm == 1 and table_name!='priviledges':
            sqlStatement = sqlStatement + "id, "

        for i in keyitems:
            if i=='id' and fromForm==1:
                continue

            if table_data[table_name].has_key(i):

                sqlStatement = sqlStatement + i + ", "
                req.write(i+'<br>')

        sqlStatement = sqlStatement[:-2] + ") VALUES ("

        if key != None and fromForm == 1 and table_name!='priviledges':
            sqlStatement = sqlStatement + "'" + key + "', "

        for i in keyitems:
            #print i+'<br>'
            if i=='id' and fromForm==1:
                continue

            if table_data[table_name].has_key(i):

                if (table_data[table_name][i]["type"] == 'VARCHAR') or (table_data[table_name][i]["type"] == 'DATE') or (table_data[table_name][i]["type"] == 'BOOL'):

                    if table_data[table_name][i]["type"] == 'BOOL':

                        if fromForm:
                            if string.lower(form[i].value) == 'yes':
                                sqlStatement = sqlStatement + "'t', "
                            elif string.lower(form[i].value) == 'no':
                                sqlStatement = sqlStatement + "'f', "
                        else:
                            if string.lower(table_data[table_name][i]['value']) == 'yes':
                                sqlStatement = sqlStatement + "'t', "
                            elif string.lower(table_data[table_name][i]['value']) == 'no':
                                sqlStatement = sqlStatement + "'f', "
                    else:

                        if fromForm:
                            if string.strip(form[i].value) == '':
                                sqlStatement = sqlStatement + "NULL, "
                            else:
                                sqlStatement = sqlStatement + "'" + escape_quote(form[i].value) + "', "
                        else:
                            if string.strip(table_data[table_name][i]['value']) == '':
                                sqlStatement = sqlStatement + "NULL, "
                            else:
                                sqlStatement = sqlStatement + "'" + escape_quote(table_data[table_name][i]['value']) + "', "


                else:

                    if fromForm:
                        if string.strip(form[i].value) == '':
                            sqlStatement = sqlStatement + "NULL, "
                        else:
                            sqlStatement = sqlStatement + form[i].value + ", "

                    else:
                        if string.strip(table_data[table_name][i]['value']) == '':
                            sqlStatement = sqlStatement + "NULL, "
                        else:
                            sqlStatement = sqlStatement + table_data[table_name][i]['value'] + ", "

        # remove last comma
        sqlStatement = sqlStatement[:-2] + ")"

    if echoStatement == 1:
        req.write("\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully")

    debug(sqlStatement)

    queryResult = executeSQL(db, sqlStatement)

    return queryResult

def textbox(req,table_name, name, value, size, maxlength, leaveFocus, gainFocus, inputType='text',readonly=0):
    """
    Generates HTML for a form password, hidden, or text field.  Table Name is
    reserved for future use. name is the name of the field, value is the value
    to set the field to, size is the size to initially display the field with
    and maxlength is the maximum length the field can scroll.  leavefocus is
    the javascript function to call when the operator moves out of the field.
    gainFocus is the javascript function to call when the operator moves into
    the field.  inputType of field can be password, hidden, or text
    HTML is written to standard output.
    """
    if type(value) is types.IntType:
        valueItem = `value`
    elif type(value) is types.FloatType:
        valueItem = `value`
    elif type(value) is types.LongType:
        valueItem = `value`
    elif type(value) is types.StringType:
        valueItem = value
    else:
        valueItem=""

    valueItem = string.strip(valueItem)

    req.write('<INPUT NAME="' + name + '" TYPE="' + inputType + '" VALUE="' + valueItem + '"')

    req.write(' SIZE="' + size + '" MAXLENGTH="' + maxlength + '"')

    if leaveFocus != None:
        req.write(' onBlur="' + leaveFocus + '"')

    if gainFocus != None:
        req.write(' onFocus="' + gainFocus + '"')

    if readonly:
        req.write(' readonly ')

    req.write('>')

def optionMenu(req, name, size, options, selected):
    """
    Generates HTML for an optionMenu form item that can allow 1-many
    selections from its options provided.
    name is the name of the optionMenu
    size is the number of items to display at a time
    options is a list sequence of all valid options that the menu 
    should display
    selected is a list sequence which is a one-to-one mapping to 
    the options list which contains per option specified by the options list
    either a NULL or blank string if the option should not be selected when
    displayed or the keyword SELECTED if the option should be selected
    HTML is written to standard output
    """
    req.write('<FONT FACE="Arial,Helvetica" SIZE="-1">')
    req.write('<SELECT NAME="' + name + '" SIZE=' + size + '>\n')
    for i in range(0,len(options)):
        req.write('<OPTION ' + selected[i] + '>' + options[i] + '\n')
    req.write('</SELECT>')
    req.write('</FONT>')

def sqlFieldFormat(fieldValue):
    isNumber=0
    checkForNumber = string.replace(fieldValue,",","")
    for i in [int,float]:
        try:
            b = i(checkForNumber)
            fieldValue = `b`
        except ValueError:
            pass
        else:
            isNumber = 1
            break

    if not isNumber:
        if string.strip(fieldValue) == '':
            fieldValue = "NULL"
        else:
            fieldValue = string.replace(fieldValue,"'","\\'")
            fieldValue = "'%s'" % (fieldValue)

    return fieldValue

def textarea(req,
             table_name,
             name,
             value,
             rows,
             cols,
             leaveFocus,
             gainFocus):
    """
    Generates HTML for a form textarea field
    table_name is reserved for future use and should contain the table name
    that the field maps to
    name is the name of the textarea form item
    value is the value to set the textarea field to
    rows is the number of rows for the initial size of the textarea
    cols is the number of cols to display at a time
    leaveFocus is the javascript handler to call when operator leaves field
    gainFocus is the javascript handler to call when operator enters field
    HTML generated is written to standard output.
    """
    
    req.write( '<TEXTAREA NAME="' + name + '" ROWS="' + rows + '" COLS="' + cols + '" SIZE="' + rows + "," + cols + '" WRAP="virtual" ')

    if leaveFocus != None:
        req.write( ' onBlur="' + leaveFocus + '"')

    if gainFocus != None:
        req.write( ' onFocus="' + gainFocus + '"')

    req.write( '>')

    if type(value) is types.IntType:
        valueItem = `value`
    elif type(value) is types.FloatType:
        valueItem = `value`
    elif type(value) is types.LongType:
        valueItem = `value`
    elif type(value) is types.StringType:
        valueItem = value

    valueItem = string.strip(valueItem)

    req.write(valueItem + '</TEXTAREA>')

def urlhref(req, target, link):
    """
    Generates HTML for a selectable link than when selected visits the target
    specified
    target is the url of the web page to visit when link clicked
    link is the text to be displayed for the link.  HTML is written to standard
    output
    """
    req.write('<A HREF="' + target + '">' + link + '</A>')

def mailhref(target, link, subject_line=None):
    """
    Generates HTML for a mail link where
    target is the e-mail address of the recipient of the message
    link is the text of the link to be displayed
    subject_line is the Subject of the message to be pre-filled when
    mail browser appears.  HTML is written to standard output.
    """
    if subject_line == None:
        req.write('<A HREF="mailto:' + target + '">' + link + '</A>')
    else:
        req.write('<A HREF="mailto:' + target + '?Subject=' + subject_line + '">' + link + '</A>')

def image(image_name, db_name, target=None, imageMissing='imageMissing.gif', hSize=None, vSize=None):
    """
    Generates HTML for an image that should be placed in the images script
    alias directory for your web server, on Linux /home/httpd/images.  HTML
    is written to standard output.
    """
    if string.strip(image_name) != "" and \
       os.path.exists(os.path.join("/home",db_name,'images',image_name)):
        image_name = string.strip(image_name)
    else:
        image_name = 'imageMissing.gif'

    if target == None:
        target = '/' + db_name + '-images'

    req.write('<IMG SRC="' + target + '/' + image_name + '">')

def trailer(table_data, db, copyright_date='1999'):
    """
    Generates HTML for a trailer message describing Copyright
    """

    sqlStatement = selectAllColumnsSqlStatement(table_data,'project_info','1')

    dbResult = executeSQL(db, sqlStatement)

    if dbResult['status'] != 'success':

        return 'error'

    else:

        result = dbResult['result']

        table_data = dbToTableData(table_data, 'project_info', result[0])

        req.write('<P ALIGN=RIGHT><FONT FACE="Arial,Helvetica" SIZE="-2" COLOR="BLACK">')
        req.write(table_data['project_info']['name']['value'] + '<BR>')
        req.write(table_data['project_info']['address_line_1']['value'] + '<BR>')

        if string.strip(table_data['project_info']['address_line_2']['value']) != '':
            req.write(table_data['project_info']['address_line_2']['value'] + '<BR>')

        req.write(table_data['project_info']['city']['value'] + ', ' + table_data['project_info']['state']['value'] + '&nbsp;&nbsp;' + table_data['project_info']['zip']['value'] + '<BR>')
        if string.strip(table_data['project_info']['phone_number_voice']['value']) != '':
            req.write('Voice: '  + table_data['project_info']['phone_number_voice']['value'] + '<BR>')

        if string.strip(table_data['project_info']['phone_number_fax']['value']) != '':
            req.write('FAX: ' + table_data['project_info']['phone_number_fax']['value'] + '<BR>')

        if string.strip(table_data['project_info']['email']['value']) != '':
            req.write('E-mail: <A HREF="mailto:' + table_data['project_info']['email']['value'] + '">' + table_data['project_info']['email']['value'] + '</A><BR>')

        req.write('<BR><BR><FONT FACE="Arial,Helvetica" SIZE="-2" COLOR="BLACK">Copyright &copy; '+ copyright_date + '<BR>')
        req.write('<A HREF="http://www.linuxden.com" target="_top">linuXden.com, LLC</A><BR>')
        req.write('All Rights Reserved</FONT>')

def usernamePasswordDisplay(username=''):
    """
    Generate a username and password display fields for a form and 
    authentication.  HTML is written to standard output.
    """
    req.write('<TABLE><BORDER=0>')
    req.write('<TR>')

    tableColumn(req,'<B>Username:</B>')
    req.write('<TD ALIGN=CENTER NOWRAP>')

    textbox(req, None,'username',username,'9','9',None,"displayHint('Enter your username')")
    req.write('</TD>')

    tableColumn(req,'<B>Password:</B>')

    req.write('<TD ALIGN=CENTER NOWRAP>')
    textbox(req, None,'password','','8','8',None,"displayHint('Enter your password')",'password')
    req.write('</TD>')
    req.write('</TR>')
    req.write('</TABLE>')

def formSetup(req, name, db_name, cgi_name, submit_action, enc_type='application/x-www-form-urlencoded'):
    """
    Generates HTML for the description of a form to follow
    name is the name of the form
    cgi_name is the name of the cgi to execute to process form
    submit_action is a javascript function to execute prior to form
    processing by cgi.  HTML is written to standard output
    """
    req.write('<FORM NAME="' + name + '" ACTION="/' + db_name + '-cgi-bin/' + cgi_name + '.pyc"')
    if submit_action != None:
        req.write(' onSubmit="' + submit_action + '"')

    req.write(' METHOD="POST" ENCTYPE="' + enc_type + '">')

def generate_form_javascript(req,table_data,table_name,form_name,firstErrorDontSubmit=0):
    ''' 
        Generates a series of javascript form processing support
        functions.  Also generates a validate_form javascript function
        which will call all validation routines listed for each field in
        the table specified by table which is found in the table_data
        declarations.  When the submit form action is processed this
        routine is called as long as <form action="return
        validate_form()"> is specified in the HTML.  All validation
        routines called by validate_form should perform all validation
        responses to errors such as display an alert window, etc.  This
        routine merely generates a dynamically built javascript procedure
        to verify all fields which should be verified before a form is
        sent to http server.  All arguments to validation routines can
        either be string or numeric.  If the argument is string it is
        surrounded by single quotes and syntax generated to preserve
        white space in the string.  Numerics are not converted to strings
        before the syntax is emitted to the validate_form function so if
        you need all arguments to the javascript to be string then
        convert the numeric to a string representation.  The
        firstErrorDontSubmit parameter when set to the default of 0
        signifies to continue validation through the entire list even if
        fields have errors.  This could possibly display multiple error
        message, etc. if the validation routines perform this operation.
        When set to 1 signifies that validation should cease on the first
        error.
    '''

    form_routine = {}
    req.write('<SCRIPT>')

    form_routine['displayHint'] = {'number_arguments' : 1}
    req.write("  function displayHint(hint) {")
    req.write("	top.status = hint;")
    req.write("	return true;")
    req.write("  }\n")

    form_routine['goto_url'] = {'number_arguments' : 1}
    req.write("function goto_url(url) {")
    req.write("  window.location.href = url;")
    req.write("  return true;")
    req.write("}\n")

    form_routine['confirmDialog'] = {'number_arguments' : 1}
    req.write('function confirmDialog(message) {')
    req.write('	if (window.confirm(message)) {')
    req.write("	  return true;")
    req.write("	}")
    req.write("	else {")
    req.write("	  return false;")
    req.write("	}")
    req.write('}\n')

    form_routine['previousUrl'] = {'number_arguments' : 1}
    req.write('  function previousUrl(url) {')
    req.write('	top.history.go(url);')
    req.write('	return true;')
    req.write('  }\n')

    form_routine['execute'] = {'number_arguments' : 2}
    req.write("function execute(action_name, id_key) {")
    req.write("  var status = false;")
    req.write('  document.' + form_name + '.action.value = action_name;')
    req.write('  document.' + form_name + '.key_id.value = id_key;')
    req.write('  status = submitForm(' + 'document.' + form_name +');')
    req.write('  if (status == true) {')

    req.write('	document.' + form_name + '.submit();')
    req.write('	return true;')
    req.write('  }')
    req.write('  else {')
    req.write("	return false;")
    req.write('  }')
    req.write("}\n")

    form_routine['process_item'] = {'number_arguments' : 3}
    req.write("function process_item(action_name, item_no, form_key) {")
    req.write("  var status = false;")
    req.write('  document.' + form_name + '.action.value = action_name;')
    req.write('  document.' + form_name + '.key_id.value = form_key;')
    req.write('  document.' + form_name + '.item_no.value = item_no;')
    req.write('  status = submitForm(' + 'document.' + form_name +');')
    req.write('  if (status == true) {')

    req.write('	document.' + form_name + '.submit();')
    req.write('	return true;')
    req.write('  }')
    req.write('  else {')
    req.write("	return false;")
    req.write('  }')
    req.write("}\n")

    form_routine['checkBlankField'] = {'number_arguments' : 2}
    req.write("  function checkBlankField(field,label) {")
    req.write("	var str = field.value;")
    req.write("	var blankStr = true;")
    req.write("	var temp_str = \"\"")

    req.write("	for (var i = 0; i < str.length; i++) {")
    req.write("	  var ch = str.substring(i,i+1)")
    req.write("	  if (ch != \" \") {")
    req.write("		blankStr = false;")
    req.write("		break;")
    req.write("	  }")
    req.write("	}")

    req.write("	if (blankStr || str.length == 0) {")
    req.write("	  alert_window(label,'Field can not be blank',field.value,'Field is required');")
    req.write("	  return false;")
    req.write("	}")
    req.write("	else {")
    req.write("	  return true;")
    req.write("	}")
    req.write("  }\n")

    form_routine['checkLength'] = {'number_arguments' : 4}
    req.write("  function checkLength (textarea, maxlength, label, required) {")
    req.write("	if (textarea.value.length > maxlength) {")
    req.write("	  alert_window(label,'Length of ' + label + ' exceeds maximum length of ' + maxlength,'Please specify less characters','Length should be less than: ' + maxlength);")
    req.write("	  return false;")
    req.write("	}")
    req.write("	if ((required) && (textarea.value.length==0)){")
    req.write("	  alert_window(label,'Field can not be blank',textarea.value,'Field is required');")
    req.write("	  return false;")
    req.write("	}")
    req.write("return true;}\n")

    form_routine['daysInMonth'] = {'number_arguments' : 2}
    req.write('  function daysInMonth(month, year) {')
    req.write('	var months = "312831303130313130313031";')
    req.write('	if (month == 2) {')
    req.write('	  if (((year % 4) == 0) && ((year % 100 != 0) || ((year % 400) == 0))) {')
    req.write('		months = months.substring(0,2) + "29" + months.substring(4,24);')
    req.write('	  }')
    req.write('	}')
    req.write('	return months.substring((month-1)*2,((month-1)*2)+2);')
    req.write('  }\n')

    form_routine['valid_integer'] = {'number_arguments' : 4}
    req.write('  function valid_integer(number,format,label,required) {')
    req.write('	if ((required) && (number.value.length) == 0) {')
    req.write('	  alert_window(label,"Integer value required","No integer input provided",format);')
    req.write('	  return false;')
    req.write('	}')

    req.write('	if ((!required) && (number.value.length == 0)) {')
    req.write('	  return true;')
    req.write('	}')

    req.write('	if (format.length != 0) {')
    req.write('	  if (number.value.length != format.length) {')
    req.write('		alert_window(label,"Invalid integer specified","Number digits input does not match format",format);')
    req.write('		return false;')
    req.write('	  }')
    req.write('	}')

    req.write('	for (var i = 0; i < number.value.length; i++) {')
    req.write('	  if (!is_digit(number.value.substring(i,i+1))) {')
    req.write('		alert_window(label,"Invalid integer specified","All digits must be 0-9",format);')
    req.write('		return false;')
    req.write('	  }')
    req.write('	}')
    req.write('	return true;')
    req.write('  }\n')

    form_routine['valid_float'] = {'number_arguments' : 4}
    req.write('  function valid_float(number,format,label,required) {')

    req.write('	var num_periods = 0;')
    req.write('	var dec_pos = 0;')

    req.write('	if ((required) && (number.value.length) == 0) {')
    req.write('	  alert_window(label,"Float value required","No floating input provided",format);')
    req.write('	  return false;')
    req.write('	}')

    req.write('	if ((!required) && (number.value.length == 0)) {')
    req.write('	  return true;')
    req.write('	}')

    req.write('	if (format.length != 0) {')
    req.write('	  if (number.value.length != format.length) {')
    req.write('		 alert_window(label,"Invalid float specified","Number digits input does not match format",format);')
    req.write('		 return false;')
    req.write('	  }')

    req.write('	  for (var i = 0; i < number.value.length; i++) {')

    req.write("		if (format.substring(i,i+1) == '.') {")
    req.write("		  if (number.value.substring(i,i+1) != '.') {")
    req.write('			alert_window(label,"Invalid float specified","Number specified does not match format",format);')
    req.write('			return false;')
    req.write('		  }')
    req.write('		}')

    req.write("		else if (format.substring(i,i+1) == '#') {")
    req.write('		  if (!is_digit(number.value.substring(i,i+1))) {')
    req.write('			alert_window(label,"Invalid float specified","Number specified does not match format",format);')
    req.write('			return false;')
    req.write('		  }'			  )
    req.write('		}')
    req.write('	  }')
    req.write('	  return true;')
    req.write('	}')
    req.write('	else {')
    req.write('	  for (var i = 0; i < number.value.length; i++) {')
    req.write("		if (number.value.substring(i,i+1) == '.') {")
    req.write('		  dec_pos = i;')
    req.write('		  num_periods = num_periods + 1;')
    req.write('		}')
    req.write('		else if (!is_digit(number.value.substring(i,i+1))) {')
    req.write("		  alert_window(label,'Invalid float specified','Non-digit found in float specified','9.9');")
    req.write('		  return false;')
    req.write('		}')
    req.write('	  }')

    req.write('	  if (num_periods != 1) {')
    req.write('		alert_window(label,"Invalid float specified","Number specified should have one decimal point","9.9");')
    req.write('		return false;')
    req.write('	  }')
    req.write('	  else {')
    req.write('		if (dec_pos == 0) {')
    req.write('		  alert_window(label,"Invalid float specified","Number specified should have a leading digit before decimal","9.9");')
    req.write('		  return false;')
    req.write('		}')
    req.write('		if (dec_pos == number.value.length) {')
    req.write('		  alert_window(label,"Invalid float specified","Number specified should have a trailing digit after decimal","9.9");')
    req.write('		  return false;')
    req.write('		}')
    req.write('	  }')
    req.write('	}')
    req.write('  }\n')

    form_routine['valid_money'] = {'number_arguments' : 4}
    req.write('  function valid_money(number,format,label,required) {')

    req.write('	var num_periods = 0;')
    req.write('	var dec_pos = 0;')

    req.write('	if ((required) && (number.value.length) == 0) {')
    req.write('	  alert_window(label,"Dollar amount value required","No dollar amount provided",format);')
    req.write('	  return false;')
    req.write('	}')

    req.write('	if ((!required) && (number.value.length == 0)) {')
    req.write('	  return true;')
    req.write('	}')

    req.write('	if (format.length != 0) {')
    req.write('	  if (number.value.length != format.length) {')
    req.write('		 alert_window(label,"Invalid dollar amount specified","Number digits input does not match format",format);')
    req.write('		 return false;')
    req.write('	  }')

    req.write('	  for (var i = 0; i < number.value.length; i++) {')

    req.write("		if (format.substring(i,i+1) == '.') {")
    req.write("		  if (number.value.substring(i,i+1) != '.') {")
    req.write('			alert_window(label,"Invalid dollar amount specified","Number specified does not match format",format);')
    req.write('			return false;')
    req.write('		  }')
    req.write('		}')

    req.write("		else if (format.substring(i,i+1) == '#') {")
    req.write('		  if (!is_digit(number.value.substring(i,i+1))) {')
    req.write('			alert_window(label,"Invalid dollar amount specified","Number specified does not match format",format);')
    req.write('			return false;')
    req.write('		  }'			  )
    req.write('		}')
    req.write('	  }')
    req.write('	  return true;')
    req.write('	}')
    req.write('	else {')
    req.write('	  for (var i = 0; i < number.value.length; i++) {')
    req.write("		if (number.value.substring(i,i+1) == '.') {")
    req.write('		  dec_pos = i;')
    req.write('		  num_periods = num_periods + 1;')
    req.write('		}')
    req.write('		else if (!is_digit(number.value.substring(i,i+1))) {')
    req.write("		  alert_window(label,'Invalid dollar amount specified','Non-digit found in dollar amount specified','9.99');")
    req.write('		  return false;')
    req.write('		}')
    req.write('	  }')

    req.write('	  if (num_periods != 1) {')
    req.write('		alert_window(label,"Invalid dollar amount specified","Number specified should have one decimal point","9.99");')
    req.write('		return false;')
    req.write('	  }')
    req.write('	  else {')
    req.write('		if (dec_pos == 0) {')
    req.write('		  alert_window(label,"Invalid dollar amount specified","Number specified should have a leading digit before decimal","9.99");')
    req.write('		  return false;')
    req.write('		}')
    req.write('		if ((dec_pos + 3) != number.value.length) {')
    req.write('		  alert_window(label,"Invalid dollar amount specified","Number specified should have 2 trailing digits after decimal","9.99");')
    req.write('		  return false;')
    req.write('		}')
    req.write('	  }')
    req.write('	  return true;')
    req.write('	}')
    req.write('  }\n')

    form_routine['valid_format'] = {'number_arguments' : 4}
    req.write('  function valid_format(field,format,label,required) {')
    req.write('	if ((required) && (field.value.length) == 0) {')
    req.write('	  alert_window(label,"Input value required","No input provided",format);')
    req.write('	  return false;')
    req.write('	}')

    req.write('	if ((!required) && (field.value.length == 0)) {')
    req.write('	  return true;')
    req.write('	}')

    req.write('	if (field.value.length != format.length) {')
    req.write('	  alert_window(label,"Not enough input provided","Data entered does not match format",format);')
    req.write('	  return false;')
    req.write('	}')

    req.write('	for (var i = 0; i < field.value.length; i++) {')
    req.write("	  if (format.substring(i,i+1) == '#') {")
    req.write('		if (!is_digit(field.value.substring(i,i+1))) {')
    req.write('		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);')
    req.write('		  return false;')
    req.write('		}'			  )
    req.write('	  }')
    req.write("	  else if (format.substring(i,i+1) == 'L') {")
    req.write('		if (!is_letter(field.value.substring(i,i+1))) {')
    req.write('		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);')
    req.write('		  return false;'			)
    req.write('		}')
    req.write('	  }')
    req.write("	  else if ((format.substring(i,i+1) != '*') && (format.substring(i,i+1) != field.value.substring(i,i+1))) {")
    req.write('		  alert_window(label,"Invalid character specified","Character specified: " + field.value.substring(i,i+1) + " does not match format",format);')
    req.write('		  return false;			')
    req.write('	  }')
    req.write('	}')
    req.write('	return true;')
    req.write('  }\n')

    form_routine['alert_window'] = {'number_arguments' : 4}
    req.write('  function alert_window(field_name, message, erroneous_data, format) {')
    req.write("	window.alert('Field Name: ' + field_name + '\\n' + message + ': ' + erroneous_data + '\\n' + 'Format: ' + format);")
    req.write('	return true;')
    req.write('  }\n')

    form_routine['is_digit'] = {'number_arguments' : 1}
    req.write('  function is_digit(character) {')
    req.write("	if (character < '0' || character > '9') {")
    req.write('	  return false;')
    req.write('	}')
    req.write('	else {')
    req.write('	  return true;')
    req.write('	}')
    req.write('  }\n')

    form_routine['is_letter'] = {'number_arguments' : 1}
    req.write('  function is_letter(character) {')
    req.write("	if ((character > 'a' && character < 'z') || (character > 'A' && character < 'Z')) {")
    req.write('	  return true;')
    req.write('	}')
    req.write('	else {')
    req.write('	  return false;')
    req.write('	}')
    req.write('  }\n')

    form_routine['valid_date'] = {'number_arguments' : 3}
    req.write('  function valid_date(date_time,label,required) {')

    req.write('	if ((required) && (date_time.value.length == 0)) {')
    req.write('	  alert_window(label,"Date value required","No date input provided","YYYY-MM-DD");')
    req.write('	  return false;')
    req.write('	}')

    req.write('	if ((!required) && (date_time.value.length == 0)) {')
    req.write('	  return true;')
    req.write('	}')

    req.write('	if (date_time.value.length != 10) {')
    req.write("	   alert_window(label,'Invalid date specified',date_time.value + ' is not long enough','MM-DD-YYYY');")
    req.write('	   return false;')
    req.write('	}')

    req.write('	for (var i = 0; i < 2; i++) {')
    req.write('	  var ch = date_time.value.substring(i,i+1);')
    req.write('	  if (!is_digit(ch)) {')
    req.write("	   alert_window(label,'Invalid month specified',date_time.value.substring(5,7) + ' is not 01-12','MM-DD-YYYY');")
    req.write('		return false;')
    req.write('	  }')
    req.write('	}')

    req.write('	if (date_time.value.substring(0,2) <= 0 || date_time.value.substring(0,2) > 12) {')
    req.write("	  alert_window(label,'Invalid month specified',date_time.value.substring(0,2) + ' is not 01-12','MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')

    req.write("	if (date_time.value.substring(2,3) != '-') {")
    req.write("	  alert_window(label,'Invalid year/month delimiter specified',date_time.value.substring(2,3) + ' is not -','MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')

    req.write('	for (var i = 3; i < 5; i++) {')
    req.write('	  var ch = date_time.value.substring(i,i+1);')
    req.write('	  if (!is_digit(ch)) {')
    req.write("		alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-31','MM-DD-YYYY');")
    req.write('		return false;')
    req.write('	  }' )
    req.write('	}')

    req.write('	if (date_time.value.substring(3,5) <= 0 || date_time.value.substring(3,5) > 31) {')
    req.write("	  alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-31','MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')

    req.write('	if (date_time.value.substring(3,5) > daysInMonth(date_time.value.substring(0,2), date_time.value.substring(6,10))) {')
    req.write("	  alert_window(label,'Invalid day specified',date_time.value.substring(3,5) + ' is not 01-' + daysInMonth(date_time.value.substring(0,2),date_time.value.substring(6,10)),'MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')

    req.write("	if (date_time.value.substring(5,6) != '-') {")
    req.write("	  alert_window(label,'Invalid month/day delimiter specified',date_time.value.substring(5,6) + ' is not -','MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')

    req.write('	for (var i = 6; i < 10; i++) {')
    req.write('	  var ch = date_time.value.substring(i,i+1);')
    req.write('	  if (!is_digit(ch)) {')
    req.write("		alert_window(label,'Invalid year specified',date_time.value.substring(6,10) + ' is not in range 1800-2037','MM-DD-YYYY');")
    req.write('		return false;')
    req.write('	  }' )
    req.write('	}')

    req.write('	if (date_time.value.substring(6,10) < 1800 || date_time.value.substring(6,10) > 2037) {')
    req.write("	  alert_window(label,'Invalid year specified',date_time.value.substring(6,10) + ' is not in range 1800-2037','MM-DD-YYYY');")
    req.write('	  return false;')
    req.write('	}')
    req.write('	return true;')
    req.write('  }\n')

    validationRoutineFound = 0

    # process all fields in field list
    for field_name in table_data[table_name].keys():

        # if the table declaration has a validation routine for the item in the
        # field list being processed
        if table_data[table_name][field_name].has_key('validation_routine') and table_data[table_name][field_name]['validation_routine'] != None:

            # if the field is not currently being displayed on form or is being displayed but not editable 
            if string.lower(table_data[table_name][field_name]['display']) != 'editable' or \
               string.lower(table_data[table_name][field_name]['display']) == 'hidden':
                # skip this field no validation required since it is not displayed or field designated
                # as not editable
                continue

            if table_data[table_name][field_name]['validation_routine'] not in form_routine.keys():
                req.write(table_data[table_name][field_name]['validation_routine'])
                req.write(form_routine.keys())
                raise Invalid_Form_Routine

            if len(table_data[table_name][field_name]['validation_arguments']) != form_routine[table_data[table_name][field_name]['validation_routine']]['number_arguments']:
                req.write(table_name)
                req.write(field_name)
                raise Invalid_Num_Args_For_Form_Routine

            if not validationRoutineFound:
                req.write('  function validate_form(form) {')
                req.write('	var error_in_form = false;')
                validationRoutineFound = 1

            # emit the if statement using the routine name and arguments specified
            # by field list

            req.write('	if (' + table_data[table_name][field_name]['validation_routine'] + '(')

            # if the validation routine has arguments
            if table_data[table_name][field_name]['validation_arguments'] != None:

                for argument_number in xrange(0,len(table_data[table_name][field_name]['validation_arguments'])):
                    if argument_number != 0:
                        req.write(',')
                    if type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.StringType:
                        req.write(table_data[table_name][field_name]['validation_arguments'][argument_number])
                    elif type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.IntType or type(table_data[table_name][field_name]['validation_arguments'][argument_number]) is types.FloatType:
                        req.write(`table_data[table_name][field_name]['validation_arguments'][argument_number]`)

            req.write(') == false) {')
            if firstErrorDontSubmit:
                req.write('	  return false;')
            else:
                req.write('	  error_in_form = true;')
            req.write('	}')

    if validationRoutineFound and firstErrorDontSubmit == 0:
        req.write('	if (error_in_form) {')
        req.write('	  return false;')
        req.write('	}')
        req.write('	else {')
        req.write('	  return true;')
        req.write('	}')
        req.write('  }\n')

    form_routine['submitForm'] = {'number_arguments' : 1}
    req.write("function submitForm(form) {")
    if validationRoutineFound:
        req.write('  var valid_form = false;')
    req.write('  if (form.action.value == "delete" || form.action.value == "delete_item") {')
    req.write('	if (window.confirm("Are you sure you want to delete this item?")) {')
    req.write("	  return true;")
    req.write("	}")
    req.write("	else {")
    req.write("	  return false;")
    req.write("	}")
    req.write("  }")

    if validationRoutineFound:
        req.write('  valid_form = validate_form(form);')
        req.write('  if (valid_form) {')
        req.write('	return true;')
        req.write('  }')
        req.write('  else {')
        req.write('	return false;')
        req.write('  }')
    else:
        req.write("  return true;")

    req.write("}\n"	)

    req.write('</SCRIPT>')

    # add the popup window function
    req.write('    <SCRIPT TYPE="text/javascript">')
    req.write('    <!--')
    req.write('    function popup(mylink, windowname,w,h)')
    req.write('    {')
    req.write('    if (! window.focus)return true;')
    req.write('    var href;')
    req.write("    if (typeof(mylink) == 'string')")
    req.write('    href=mylink;')
    req.write('    else')
    req.write('    href=mylink.href;')
    req.write('    LeftPosition=(screen.width)?(screen.width-w)/2:100;')
    req.write('    TopPosition=(screen.height)?(screen.height-h)/2:100;')
    settings="'width='+ w + ',height='+ h + ',top=' + TopPosition + "
    settings=settings+"',left=' + LeftPosition + ',scrollbars=yes'"
    req.write("    settings=%s" % settings)
    req.write('    popwindow=window.open(href, windowname, settings);')
    req.write('    popWindow.focus()')
    req.write('    return false;')
    req.write('    }')
    req.write('    //-->')
    req.write('    </SCRIPT>')

def javaScript(req, form_name):
    """
    Generates HTML for a variety of javascript functions to handle
    form processing.  HTML is written to standard output
    """

    req.write( "<SCRIPT>")
    req.write( "<!-- For browser without JavaScript support")

    req.write( 'function confirmDialog(message) {\n')
    req.write( '	if (window.confirm(message)) {\n')
    req.write( "	  return true;\n")
    req.write( "	}\n")
    req.write( "	else {\n")
    req.write( "	  return false;\n")
    req.write( "	}\n")
    req.write( '}\n')

    req.write( 'function goto_url(url) {\n')
    req.write( '  window.location.href = url;\n')
    req.write( '  return true;\n')
    req.write( '}\n')

    req.write( 'function toMenu (menuName) {\n')
    req.write( '  window.history.go(menuName);\n')
    req.write( '  return true;\n')
    req.write( '}\n')

    req.write( "function submitForm(form) {\n")
    req.write( '  if (form.action.value == "delete" || form.action.value == "delete_item") {\n')
    req.write( '	if (window.confirm("Are you sure you want to delete this item?")) {\n')
    req.write( "	  return true;\n")
    req.write( "	}\n")
    req.write( "	else {\n")
    req.write( "	  return false;\n")
    req.write( "	}\n")
    req.write( "  }\n")
    req.write( "  return true;\n")
    req.write( "}")

    req.write( "function execute(action_name, id_key) {\n")
    req.write( "  var status = false;\n")
    req.write( '  document.' + form_name + '.action.value = action_name;\n')
    req.write( '  document.' + form_name + '.key_id.value = id_key;\n')
    req.write( '  status = submitForm(' + 'document.' + form_name +');\n')
    req.write( '  if (status == true) {\n')

    req.write( '	document.' + form_name + '.submit();\n')
    req.write( '	return true;\n')
    req.write( '  }\n')
    req.write( '  else {\n')
    req.write( "	return false;\n")
    req.write( '  }\n')
    req.write( "}\n")

    req.write( "function process_item(action_name, item_no) {\n")
    req.write( "  var status = false;\n")
    req.write( '  document.' + form_name + '.action.value = action_name;\n')
    req.write( '  document.' + form_name + '.item_no.value = item_no;\n')
    req.write( '  status = submitForm(' + 'document.' + form_name +');\n')
    req.write( '  if (status == true) {\n')

    req.write( '	document.' + form_name + '.submit();\n')
    req.write( '	return true;\n')
    req.write( '  }\n')
    req.write( '  else {\n')
    req.write( "	return false;\n")
    req.write( '  }\n')
    req.write( "}\n")

    req.write( "function displayHint(hint) {\n")
    req.write( "  window.status = hint;\n")
    req.write( "  return true;\n")
    req.write( "}\n")

    req.write( "function carriage_return () {\n")
    req.write( "  if (navigator.appVersion.lastIndexOf ('Win') != -1) {\n")
    req.write( '	return "\\r\\n";\n')
    req.write( "  }\n")
    req.write( "  return \"\\n\";\n")
    req.write( "}\n")

    req.write( "function checkBlankField(theField, fieldName) {\n")
    req.write( "  var str = theField.value;\n")
    req.write( "  var blankStr = true;\n")
    req.write( "  for (var i = 0; i < str.length; i++) {\n")
    req.write( "	var ch = str.substring(i,i+1);\n")
    req.write( '	if (ch != " ") {\n')
    req.write( "	  blankStr = false;\n")
    req.write( "	  break;\n")
    req.write( "	}\n")
    req.write( "  }\n")

    req.write( "  if (blankStr || str.length == 0) {\n")
    req.write( '	document.' + form_name + '.alerts.value = fieldName + " can not be blank!" + document.' + form_name + '.alerts.value;\n')
    req.write( "	return true;\n")
    req.write( "  }\n")
    req.write( "  else {\n")
    req.write( "	return false;\n")
    req.write( "  }\n")
    req.write( "}\n")

    req.write( "function goto_url(url) {")
    req.write( "  window.location.href = url;")
    req.write( "  return true;")
    req.write( "}\n")


    req.write( "// -->")
    req.write( "</SCRIPT>")

    # add the popup window function
    req.write( '    <SCRIPT TYPE="text/javascript">')
    req.write( '    <!--')
    req.write( '    function popup(mylink, windowname,w,h)')
    req.write( '    {')
    req.write( '    if (! window.focus)return true;')
    req.write( '    var href;')
    req.write( "    if (typeof(mylink) == 'string')")
    req.write( '    href=mylink;')
    req.write( '    else')
    req.write( '    href=mylink.href;')
    req.write( '    LeftPosition=(screen.width)?(screen.width-w)/2:100;')
    req.write( '    TopPosition=(screen.height)?(screen.height-h)/2:100;')
    settings="'width='+ w + ',height='+ h + ',top=' + TopPosition + ")
    settings=settings+"',left=' + LeftPosition + ',scrollbars=yes'")
    req.write( "    settings=%s" % (settings))
    req.write( '    popwindow=window.open(href, windowname, settings);')
    req.write( '    popWindow.focus()')
    req.write( '    return false;')
    req.write( '    }')
    req.write( '    //-->')
    req.write( '    </SCRIPT>')

def tableColumn(req, data, align='center',wrap='NOWRAP'):
    """
    Generates HTML table column tags with data inserted in the column
    optional alignment specifier for column is provided.  HTML is written
    to standard output.
    """

    req.write('<TD ALIGN=' + align + ' ' + wrap + '><FONT FACE="Arial,Helvetica" SIZE="-1">' + data + '</FONT></TD>')

def header(headers):
    pass

def tableDataToDb(table_data,table_name):
    """
    Converts table data items specified by table_name to data values that
    can be stored in the database.  Resultant db data created is returned.
    """

    dbData = {}

    for field_name in table_data[table_name].keys():

        if table_data[table_name][field_name]["type"] == 'BOOL':

            if string.lower(table_data[table_name][field_name]["value"]) == "yes":
                dbData[field_name] = 't'
            elif string.lower(table_data[table_name][field_name]['value']) == 'no':
                dbData[field_name] = 'f'

        elif table_data[table_name][field_name]["type"] == 'INT4':
            dbData[field_name] = int(table_data[table_name][field_name]["value"])

        elif table_data[table_name][field_name]["type"] == 'FLOAT4':
            dbData[field_name] = float(table_data[table_name][field_name]["value"])

        else:
            dbData[field_name] = string.strip(table_data[table_name][field_name]["value"])


    return dbData

def dbToTableData(table_data, table_name, db):
    """
    Converts data found in the database fields specified by the dictionary db
    to data that can be stored in table_data designated by table_name.
    Specifically handles BOOL conversion to Yes, No values and converted
    numerically stored db data into strings since all table data values are
    stored as strings.  The values are stripped of whitespace on the left and
    right.  The resultant table_data is returned.
    """

    for field_name in db.keys():

        if table_data[table_name].has_key(field_name):

            if table_data[table_name][field_name]["type"] == 'BOOL':

                if db[field_name] == 't':
                    table_data[table_name][field_name]["value"] = "Yes"
                else:
                    table_data[table_name][field_name]["value"] = "No"

            elif table_data[table_name][field_name]["type"] == 'INT4' or \
                 table_data[table_name][field_name]["type"] == 'FLOAT4':
                #req.write("\n\n<BR>"+db[field_name]+'<BR>\n\n')
                if db[field_name]=='':
                    table_data[table_name][field_name]["value"]=""
                else:
                    table_data[table_name][field_name]["value"] = `db[field_name]`

            else:
                table_data[table_name][field_name]["value"] = db[field_name]

            if table_data[table_name][field_name]["value"] != None:
                string.strip(table_data[table_name][field_name]["value"])

    return table_data

def cookieToTableData(table_data,table_name,cookie,key=None):
    """
    Converts the data fields in cookie to table_data specified by table_name
    the id of the table can optionally be set.  Cookie field names must match
    table_data field names in table_name for this to work as is the case with
    all of the mapping functions in this file.  The resultant table_data
    will be returned
    """
    for field_name in cookie.keys():
        if table_data[table_name].has_key(field_name):
            table_data[table_name][field_name]['value'] = cookie[field_name].value

    if key != None:
        table_data[table_name]['id'] = key

    return table_data

def retainAllHiddenFormFields(req,table_data,form):

    for field_name in form.keys():

        if field_name[-6:] == 'hidden':

            start = string.index(field_name,'_')+1
            end = string.rindex(field_name,'_',start)

            table_name = field_name[:string.index(field_name,'_')]

            textbox(req,None,field_name,form[field_name].value,table_data[table_name][field_name[start:end]]['form_size'],table_data[table_name][field_name[start:end]]['form_size'],None,None,'hidden')

def formToHiddenFields(req,table_data,table_name,form):

    for field_name in form.keys():
        if table_data[table_name].has_key(field_name):
            textbox(req,None,table_name + '_' + field_name + '_hidden',form[field_name].value,table_data[table_name][field_name]['form_size'],table_data[table_name][field_name]['form_size'],None,None,'hidden')

def tableDataToCookie(table_data,table_name,cookie,key=None):

    for field_name in table_data[table_name].keys():
        cookie[field_name] = table_data[table_name][field_name]["value"]

    if key != None:
        cookie['id'] = table_data[table_name]["id"]["value"]

    return cookie

def formToTableData(table_data,table_name, form, key=None):

    for field_name in form.keys():
        if table_data[table_name].has_key(field_name):			
            table_data[table_name][field_name]["value"] = form[field_name].value

    if key != None:
        table_data[table_name]["id"]["value"] = key

    return table_data

def hiddenFieldsWithTableNameToTableData(table_data,table_name,form,key=None):
    """
    Examines the form fields in argument form that are hidden fields or 
    specifically are named {table_name}{field_in_table_name}_hidden.  Then 
    sets the table_data, table_name_field_name entry for this field to the 
    value of the hidden field. Returns resultant table_data items
    """

    for field_name in form.keys():

        # if the table name is the first part of the field name and field is a hidden field
        if field_name[:len(table_name)] == table_name and field_name[-6:] == 'hidden':
            start = string.index(field_name,'_')+1
            end = string.rindex(field_name,'_',start)

            if table_data[table_name].has_key(field_name[start:end]):			
                table_data[table_name][field_name[start:end]]["value"] = form[field_name].value 

    if key != None:
        table_data[table_name]["id"]["value"] = key

    return table_data

def formToDict(form):
    """ 
    Converts a module cgi dictionary of form field values to a 
    simple dictionary[field_name] = value dictionary
    Returns the dictionary.  Basically loads form[field_name].value
    into a dictionary[field_name] = value representation
    """

    dict = {}
    keyitems = form.keys()

    for i in keyitems:
        dict[i] = form[i].value

    return dict

def formOptionListToList(form, optionListName):
    optionList = []
    optionListData = form[optionListName]
    if type(optionListData) is type([]):
        for option in optionListData:
            optionList.append(option.value)
    else:
        optionList.append(optionListData.value)

    return optionList

def getFormData(keep_blank_values=1):
    """
    Returns the fields and values of a form that has been submitted to
    a CGI script.  By default form fields that the operator has not entered
    data into or are blank are submitted to the CGI.  The CGI module would
    not give the CGI these fields by default, they would merely not exist.
    """
    return cgi.FieldStorage(keep_blank_values=1)

def htmlContentType(req,cookies=None):		
    """
    Generates the content type header that web browser look for in order
    to determine how it should process the data to follow.  Will optionally
    generate the cookie header text which sets the values of cookies
    """

    req.write("Content-type: text/html")
    if cookies != None:
        req.write(cookies)

def title(req, title_data):
    """
    Generates HTML to standard output for the title of the web page
    """
    req.write('<TITLE>' + 'PMT Database' + ': ' + title_data + '</TITLE>')

def executeSQL(db, sqlStatement):
    """
    Execute a sql statement specified by sqlStatement for the already
    open db connection designate by db
    Returns a queryResult type, see above
    """

    try:
        pgqueryObject = db.query(sqlStatement)

    except TypeError:
        return {'status' : 'error', 'message' : "TypeError: Bad Argument type, or too many arguments", 'result' : None} 
    except ValueError:
        return {'status' : 'error', 'message' : "ValueError: Empty SQL Query", 'result' : None} 
    except _pg.ProgrammingError, message:
        debug('programming error: message = %s' % (message))
        return {'status' : 'error', 'message' : message, 'result' : None}

    # sql statement is not a select or insert
    if pgqueryObject == None:
        return {'status' : 'success', 'message' : "SQL Statement processed returning nothing", 'result' : None}

    # sql statement is an insert or update statement
    if type(pgqueryObject) is types.IntType:
        return {'status' : 'success', 'message' : "SQL Statement processed return number rows affected", 'result' : pgqueryObject}

    elif type(pgqueryObject) is types.LongType:
        return {'status' : 'success', 'message' : "SQL Statement processed return number rows affected", 'result' : pgqueryObject}

    result = pgqueryObject.dictresult()

    for row in xrange(0,len(result)):
        for column in result[row].keys():
            if result[row][column] == None:
                result[row][column] = ""

    return {'status' : 'success', 'message' : "SQL Query processed returning rows fetched", 'result' : result}

def create_tables(req, db, table_data, echoStatement=0):

    table_name_keys = table_data.keys()

    table_name_keys.sort()

    # loop through each table name
    for table_name in table_name_keys:

        sqlStatement = "DROP TABLE " + table_name

        queryResult = executeSQL(db, sqlStatement)

        sqlStatement = "CREATE TABLE "

        sqlStatement = sqlStatement + table_name + " ("

        column_name_keys = table_data[table_name].keys()

        column_name_keys.sort()

        creation_order = []
        max=0
        for i in column_name_keys:
            val=int(table_data[table_name][i]['display_order'])
            if val>max:
                max=val

        for i in xrange(0,max):
            creation_order.append("")

        for i in column_name_keys:
            creation_order[int(table_data[table_name][i]['display_order'])-1] = i

        # put id key up front
        for column_name in creation_order:
            if column_name=='':
                continue

            sqlStatement = sqlStatement + buildColumnDeclaration(table_name, column_name, table_data)

            sqlStatement = sqlStatement + ", "

        sqlStatement = sqlStatement[:-2] + ")"

        if echoStatement == 1:
            req.write("\nSQL Statement:\n" + sqlStatement + "\nPerformed successfully")

        queryResult = executeSQL(db, sqlStatement)

        if queryResult['status'] != 'success':
            return queryResult

    return {'status' : 'success', 'message' : "Database tables created successfully", 'result' : None}

def connectDB(username, password, database):

    try:

        db = DB(database, 'localhost', 5432, None, None, username, password)

    except TypeError:
        return {'status' : 'error', 'message' : "Bad Argument type, or too many arguments", 'result' : None}

    except SyntaxError:
        return {'status' : 'error', 'message' : "Duplicate argument definition in connect", 'result' : None}

    except _pg.InternalError, message:
        return {'status' : 'error', 'message' : message, 'result' : None}

    return {'status' : 'success', 'message' : 'Database connection succeeded', 'result' : db}

def executeSqlItemList(req, db, sqlList, echoStatement=0,ignoreErrors=0):

    for sqlItem in sqlList:

        queryResult = executeSQL(db, sqlItem)

        if not ignoreErrors:
            if queryResult["status"] != 'success':
                return queryResult

        if echoStatement == 1:
            print "\nSQL Statement: " + sqlItem + '\nPerformed with status: ' + queryResult['status']
            if queryResult['status'] != 'success':
                print 'Details: ' + queryResult['message']

    return {'status' : "success", 'message' : "Items in SqlItemList processed", 'result' : None}

def table_data_to_email(table_data, table_name, displayOrder='useValues'):

    email_form = ''

    field_name_keys = table_data[table_name].keys()

    if displayOrder == 'sort':
        field_name_keys.sort()

    elif displayOrder == 'useValues':
        display_list = []

        # build display list array
        for i in xrange(0,len(field_name_keys)):
            display_list.append("")

        # load display_list entries with table display order field_names
        for i in field_name_keys:
            display_list[int(table_data[table_name][i]['display_order'])-1] = i

        field_name_keys = display_list

    for field_name in field_name_keys:

        if table_data[table_name][field_name]["display"] == 'editable' or \
           table_data[table_name][field_name]["display"] == 'read-only':

            email_form = email_form + table_data[table_name][field_name]['label'] + ': '

            # field specified in table data as editable
            if table_data[table_name][field_name]['display'] == 'editable' or \
               table_data[table_name][field_name]["display"] == 'read-only':

                email_form = email_form + table_data[table_name][field_name]['value'] + '\n'

    return email_form

def display_form(req, table_data, table_name, editable=1, displayOrder='useValues', displayHeader=1, db=None):

    req.write("<TABLE >")

    if editable == 1:
        req.write('<CAPTION>Field Labels in <B><FONT COLOR=RED>Red</FONT></B> or <B>Bold</B> on Mononchrome Displays are Required</CAPTION>')

    if displayHeader:
        req.write('<TR><TH>Field Name</TH><TH>Value</TH>')

    if editable == 1:
        req.write('<TH>Format</TH>')

    req.write('</TR>')

    field_name_keys = table_data[table_name].keys()

    if displayOrder == 'sort':
        field_name_keys.sort()

    elif displayOrder == 'useValues':
        display_list = []

        # build display list array
        for i in xrange(0,len(field_name_keys)):
            display_list.append("")

        # load display_list entries with table display order field_names
        for i in field_name_keys:
            display_list[int(table_data[table_name][i]['display_order'])-1] = i

        field_name_keys = display_list

    for field_name in field_name_keys:

        if table_data[table_name][field_name]["display"] == 'editable' or \
           table_data[table_name][field_name]["display"] == 'read-only':

            req.write('<TR>')

            if editable == 1:

                if table_data[table_name][field_name].has_key('required'):

                    if  table_data[table_name][field_name]['required']:
                        req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=RED SIZE="-1">' + '<B>' + table_data[table_name][field_name]["label"] + ':' + '</B>' + '</FONT></TD>')
                    else:
                        req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>')
                else:
                    req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>')

            else:
                req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + '<B>' + table_data[table_name][field_name]["label"] + ':</B>' + '</FONT></TD>')

            req.write('<TD ALIGN=LEFT >')

            # field specified in table data as editable
            if table_data[table_name][field_name]["display"] == 'editable':

                # caller wants for displayed editable
                if editable == 1:

                    if table_data[table_name][field_name]["type"] == 'BOOL':
                        if table_data[table_name][field_name]["value"] == 'Yes':
                            optionMenu(req,field_name,"1",["Yes","No"],["SELECTED",""])
                        else:
                            optionMenu(req,field_name,"1",["Yes","No"],["","SELECTED"])

                    else:
                        if int(table_data[table_name][field_name]["form_size"]) > 64:
                            rows=8
                            if int(table_data[table_name][field_name]["form_size"])<8*64:
                                rows=int(table_data[table_name][field_name]["form_size"])/64
                            textarea(req,
                                     table_name,
                                     field_name, 
                                     table_data[table_name][field_name]["value"],
                                     `rows`,#`int(table_data[table_name][field_name]["form_size"]) / 64`,
                                     '64',
                                     table_data[table_name][field_name]["leaveFocus"],
                                     table_data[table_name][field_name]["gainFocus"])

                        else:
                            if table_data[table_name][field_name].has_key('lov'):
                                # display an option menu since the field is only allowed to
                                # be set to the item in a list of value table

                                dbResult = executeSQL(db, table_data[table_name][field_name]['lov'])

                                if dbResult['status'] != 'success':
                                    # error could not process sql lov
                                    pass
                                else:

                                    result = dbResult['result']
                                    option_items = []
                                    selection_list = []

                                    if not table_data[table_name][field_name].has_key('required'):
                                        option_items.append('')

                                        if string.strip(table_data[table_name][field_name]['value']) == '':
                                            selection_list.append('SELECTED')
                                        else:
                                            selection_list.append('')


                                    match=0
                                    for i in xrange(0,len(result)):

                                        item_list = result[i].values()
                                        item=""
                                        if item_list[0]=='All':
                                            item=item_list[0]
                                        else:
                                            for i in xrange(0,len(item_list)):
                                                item=item+item_list[i]+', '

                                            item=item[:-2]

                                        option_items.append(item)

                                        if item == table_data[table_name][field_name]['value']:
                                            selection_list.append("SELECTED")
                                            match=1
                                        elif string.find(item,','):
                                            index=string.find(item,',')
                                            if item[:index]==table_data[table_name][field_name]['value']:
                                                selection_list.append("SELECTED")
                                                mathc=1
                                            else:
                                                selection_list.append("")

                                        else:
                                            selection_list.append("")

                                    if match==0:
                                        option_items.append(table_data[table_name][field_name]['value'])
                                        selection_list.append("SELECTED")
                                    optionMenu(req,field_name,"1",option_items,selection_list)

                            else:
                                if table_data[table_name][field_name].has_key('form_input_type'):
                                    form_input_type = table_data[table_name][field_name]['form_input_type']
                                else:
                                    form_input_type = 'text'

                                textbox(req,
                                        table_name,
                                        field_name,
                                        table_data[table_name][field_name]["value"],
                                        table_data[table_name][field_name]["form_size"],
                                        table_data[table_name][field_name]["form_size"],
                                        table_data[table_name][field_name]["leaveFocus"],
                                        table_data[table_name][field_name]["gainFocus"],
                                        form_input_type)
                else:

                    if table_data[table_name][field_name].has_key('form_input_type') and table_data[table_name][field_name]['form_input_type'] == 'password':
                        req.write('')
                    else:
                        if table_data[table_name][field_name].has_key('display_link') and table_data[table_name][field_name]['display_link'] == 1:
                            urlhref(req, 'mailto:%s' % (table_data[table_name][field_name]["value"]),table_data[table_name][field_name]["value"])
                        else:
                            req.write(table_data[table_name][field_name]["value"])

            else:
                if table_data[table_name][field_name].has_key('form_input_type') and table_data[table_name][field_name]['form_input_type'] == 'password':
                    req.write('')
                else:
                    if table_data[table_name][field_name].has_key('display_link') and table_data[table_name][field_name]['display_link'] == 1:
                        urlhref(req, 'mailto:%s' % (table_data[table_name][field_name]["value"]),table_data[table_name][field_name]["value"])
                    else:
                        if editable!=1:
                            req.write(table_data[table_name][field_name]['value'])

                        else:
                            if table_data[table_name][field_name].has_key('form_input_type'):
                                form_input_type = table_data[table_name][field_name]['form_input_type']
                            else:
                                form_input_type = 'text'

                            textbox(req,
                                    table_name,field_name,
                                    table_data[table_name][field_name]["value"],
                                    table_data[table_name][field_name]["form_size"],
                                    table_data[table_name][field_name]["form_size"],
                                    table_data[table_name][field_name]["leaveFocus"],
                                    table_data[table_name][field_name]["gainFocus"],
                                    form_input_type,readonly=1)


            req.write('</TD>')

            if table_data[table_name][field_name].has_key("format"):
                if editable == 1:
                    tableColumn(req,table_data[table_name][field_name]["format"],'left')

            req.write('</TR>')

    req.write('</TABLE>')

def init_table_data(table_data, table_name):

    field_name_keys = table_data[table_name].keys()

    for field_name in field_name_keys:
        if table_data[table_name][field_name]["default"] != None:
            table_data[table_name][field_name]["value"] = table_data[table_name][field_name]["default"]
        else:
            table_data[table_name][field_name]["value"] = ''

    return table_data

def executeQuery(req, db, table_data, table_name, queryFields, whereFields, itemFunctions, queryItemFunctionsHtml, orderClause='ORDER BY id', queryItemKeys=['id'], whereClause=None,ignoreFields=None,queryButtonAction="return execute('query')",queryItemFunctionArgs=None,customSQL=None):
    """
    Executes a user specified query from the column headers on an existing
    or 
    """

    # allocate the options list
    options = []
    selectedOptions = []

    # table names
    #fieldNames = table_data[table_name].keys()
    fieldNames = []

    # set options to the label associated with the field names of the keys in table name
    for columnName in table_data[table_name].keys():
        # load options list with column labels for each column that exists in table except any that have been specified to be ignored or are hidden

        # Don't allow passwords to be displayed
        if table_data[table_name][columnName].has_key('form_input_type'):
            if string.lower(table_data[table_name][columnName]['form_input_type'])=='password':
                if ignoreFields==None:
                    ignoreFields=[columnName]
                else:
                    ignoreFields.append(columnName)

        if ignoreFields != None:
            if columnName not in ignoreFields and \
               string.lower(table_data[table_name][columnName]['display']) != 'hidden':
                options.append(table_data[table_name][columnName]["label"])
                selectedOptions.append("")
                fieldNames.append(columnName)
        else:
            if string.lower(table_data[table_name][columnName]['display']) != 'hidden':
                options.append(table_data[table_name][columnName]["label"])
                selectedOptions.append("")
                fieldNames.append(columnName)

    options.append("None")	
    selectedOptions.append("")

    req.write('<FONT FACE="Arial,Helvetica" SIZE="-2">')
    req.write('<TABLE BORDER=1>')
    req.write('<TR>')

    # for each field in query fields list
    for columnNumber in xrange(0,len(queryFields)):

        req.write('<TH>')

        # the item that is supposed to be the field name is found by
        # using the index of the field name

        selectedOptions[fieldNames.index(queryFields[columnNumber])] = "SELECTED"

        # generate the options menu with the current field to display for this column
        optionMenu(req,'columnOption' + `columnNumber`, '1', options, selectedOptions)

        selectedOptions[fieldNames.index(queryFields[columnNumber])] = ""

        relops, selRelops = queryRelops(table_data, table_name, queryFields[columnNumber])

        # generate the options menu with the current field to display for this column
        optionMenu(req,'columnRelop' + `columnNumber`, '1', relops, selRelops)

        textbox(req, table_name, 'columnMatch' + `columnNumber`, '', '10', table_data[table_name][queryFields[columnNumber]]["form_size"],None,None)

        req.write('</TH>')

    req.write('<TH><FONT FACE="Arial,Helvetica" SIZE="-1">Add Column<BR>')

    # generate the options menu with the current field to display for this column
    # remove the None from options list

    selectedOptions[len(selectedOptions)-1] = "SELECTED"
    optionMenu(req,'addColumn', '1', options, selectedOptions)

    if queryButtonAction != None:
        req.write('<INPUT NAME="subQuery" type="button" value=" Query " onClick="%s">' % (queryButtonAction))

    req.write('</TH>')
    req.write('</TR>')

    if customSQL!=None:
        sqlStatement=customSQL
    else:
        sqlStatement = 'SELECT '

        for columnNumber in xrange(0,len(queryItemKeys)):

            sqlStatement = sqlStatement + queryItemKeys[columnNumber] + ', '

        for columnNumber in xrange(0,len(queryFields)):
            sqlStatement = sqlStatement + queryFields[columnNumber] + ', '

        sqlStatement = sqlStatement[:-2]

        sqlStatement = sqlStatement + ' FROM ' + table_name

        if whereFields != None and whereFields != []:
            sqlStatement = sqlStatement + " WHERE "

            for whereFieldNumber in xrange(0,len(whereFields)):
                sqlStatement = sqlStatement + whereFields[whereFieldNumber] + ' AND '

            sqlStatement = sqlStatement[:-5]

        if whereClause != None:
            if whereFields != None and whereFields != []:
                sqlStatement = sqlStatement + ' AND ' + whereClause
            else:
                sqlStatement = sqlStatement + ' WHERE ' + whereClause

        sqlStatement = sqlStatement + ' ' + orderClause

    queryResult = executeSQL(db, sqlStatement)

    if queryResult['status'] != 'success':

        return (queryResult, sqlStatement)

    else:

        result = queryResult['result']

        # loop through all rows returned from query
        for row in xrange(0,len(result)):

            table_data = dbToTableData(table_data, table_name, result[row])

            req.write('<TR>')

            # for each column specified by queryFields
            for col in xrange(0,len(queryFields)):

                # generate a table column

                if table_data[table_name][queryFields[col]].has_key('display_link') and table_data[table_name][queryFields[col]]['display_link'] == 1:
                    req.write('<TD ALIGN=' + "CENTER" + ' NOWRAP><FONT FACE="Arial,Helvetica" SIZE="-1">')
                    urlhref(req, 'mailto:%s' % (table_data[table_name][queryFields[col]]["value"]),table_data[table_name][queryFields[col]]["value"])
                    req.write('</FONT></TD>')
                else:

                    if table_data[table_name][queryFields[col]]['form_size'] > 40:
                        tableColumn(req,table_data[table_name][queryFields[col]]["value"],'CENTER','WRAP')

                    else:
                        tableColumn(req,table_data[table_name][queryFields[col]]["value"],'CENTER','NOWRAP')

            if itemFunctions == 'query':

                if queryItemFunctionArgs != None:
                    args = []
                    for columnNumber in xrange(0,len(queryItemKeys)):
                        args.append(table_data[table_name][queryItemKeys[columnNumber]]["value"])
                    req.write(queryItemFunctionsHtml(args + queryItemFunctionArgs))

            req.write('</TR>')

        req.write('</TABLE>')

    return (queryResult, sqlStatement)

def getQueryWhereFields(form, table_data, table_name):

    if form.has_key("columnOption0"):

        queryFields = []
        whereFields = []

        found = 0
        numCol = 0

        while 1:
            if form.has_key("columnOption" + `numCol`):
                numCol = numCol + 1
            else:
                break

        # loop through all columns on query page
        for columnNumber in xrange(0,numCol):

            for columnName in table_data[table_name].keys():

                if table_data[table_name][columnName]["label"] == form["columnOption" + `columnNumber`].value:
                    if string.strip(form["columnMatch" + `columnNumber`].value) != "":
                        if (table_data[table_name][columnName]["type"] == 'VARCHAR') or \
                           (table_data[table_name][columnName]["type"] == 'DATE') or \
                           (table_data[table_name][columnName]["type"] == 'BOOL'):

                            if form['columnMatch' + `columnNumber`].value == 'NULL':
                                whereFields.append(columnName + " " + form["columnRelop" + `columnNumber`].value + " " + form["columnMatch" + `columnNumber`].value)

                            else:
                                whereFields.append(columnName + " " + form["columnRelop" + `columnNumber`].value + " '" + form["columnMatch" + `columnNumber`].value + "'")

                        else:

                            if table_data[table_name][columnName]['type'] == 'DECIMAL':
                                # have to cast db items declared as decimal
                                whereFieldItem = 'float8(' + columnName + ") " + form["columnRelop" + `columnNumber`].value + " " + form["columnMatch" + `columnNumber`].value
                            else:
                                whereFieldItem = columnName + " " + form["columnRelop" + `columnNumber`].value + " " + form["columnMatch" + `columnNumber`].value

                            whereFields.append(whereFieldItem)

                    queryFields.append(columnName)
                    break

        if form.has_key("addColumn"):
            if form["addColumn"].value != "None":

                for columnName in table_data[table_name].keys():				
                    if table_data[table_name][columnName]["label"] == form["addColumn"].value:
                        queryFields.append(columnName)

        return (queryFields, whereFields)

    else:
        return (None, None)

def queryRelops(table_data, table_name, queryField):

    if table_data[table_name][queryField]["type"] == 'VARCHAR':
        relOptions = []
        relOptions.append("<")
        relOptions.append("<=")
        relOptions.append("=")
        relOptions.append("!=")
        relOptions.append(">")
        relOptions.append(">=")
        relOptions.append("like")
        relOptions.append("IS")
        selRelops = []
        selRelops.append("")
        selRelops.append("")
        selRelops.append("SELECTED")
        selRelops.append("")
        selRelops.append("")
        selRelops.append("")
        selRelops.append("")
        selRelops.append("")

    elif table_data[table_name][queryField]["type"] == 'BOOL':
        relOptions = []
        relOptions.append("=")
        relOptions.append("!=")
        selRelops = []
        selRelops.append("SELECTED")
        selRelops.append("")

    elif table_data[table_name][queryField]["type"] == 'INT4' or \
             table_data[table_name][queryField]["type"] == 'FLOAT4' or \
             table_data[table_name][queryField]["type"] == 'DECIMAL' or \
             table_data[table_name][queryField]["type"] == 'DATE':
        relOptions = []
        relOptions.append("<")
        relOptions.append("<=")
        relOptions.append("=")
        relOptions.append("!=")
        relOptions.append(">")
        relOptions.append(">=")
        relOptions.append("IS")
        selRelops = []
        selRelops.append("")
        selRelops.append("")
        selRelops.append("SELECTED")
        selRelops.append("")
        selRelops.append("")
        selRelops.append("")
        selRelops.append("")

    return (relOptions, selRelops)

def alertsArea(req, form, value):
    req.write("<BR>Alerts:")
    textarea(req, None, 'alerts', value, '2', '64', None, None)

def storeHiddenFields(req, username, password):
    textbox(req, None, 'key_id', '', '10', '10', None, None, 'hidden')
    textbox(req, None, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, None, 'item_no', '', '8', '8', None, None, 'hidden')

def createHiddenFields(req, username, password):
    textbox(req, 'key_id', '', '10', '10', None, None, 'hidden')
    textbox(req, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, 'item_no', '', '8', '8', None, None, 'hidden')

def viewPropertiesHiddenFields(req, username, password):
    textbox(req, 'key_id', '', '10', '10', None, None, 'hidden')
    textbox(req, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, 'item_no', '', '8', '8', None, None, 'hidden')

def storeHiddenFields(req, username, password):
    textbox(req, 'key_id', '', '10', '10', None, None, 'hidden')
    textbox(req, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, 'item_no', '', '8', '8', None, None, 'hidden')

def queryHiddenFields(req, username, password, key_id=''):
    textbox(req, 'key_id', key_id, '10', '10', None, None, 'hidden')
    textbox(req, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, 'item_no', '', '8', '8', None, None, 'hidden')

def editHiddenFields(req, username, password, key_id=''):
    textbox(req, 'key_id', key_id, '10', '10', None, None, 'hidden')
    textbox(req, 'action', '', '10', '10', None, None, 'hidden')
    textbox(req, 'item_no', '', '8', '8', None, None, 'hidden')

def queryItemFunctionsHtmlNoEdit(db_key):
    return '<TD ALIGN=CENTER NOWRAP><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">'

def queryItemFunctionsHtml(db_key):
    return '<TD ALIGN=CENTER NOWRAP><INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ", '" + db_key + "'" + ')"><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">'

def viewPropertiesFunctionsHtml(db_key):
    return '<TD ALIGN=CENTER NOWRAP><FONT FACE="Arial,Helvetica" SIZE=-1"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')"></FONT></TD>'

def queryItemFunctions(db_key):
    tableColumn(req,'<INPUT NAME="edit" type="button" value=" Edit " onClick="return execute(' + "'edit'" + ", '" + db_key + "'" + ')"><INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ", '" + db_key + "'" + ')"><INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')

def queryFunctionButtons(req, loginOk=1, help_pdf=pmt_site):
    req.write('<HR>')
    req.write('<TABLE>')
    req.write('<TR>')
    tableColumn(req,'<INPUT NAME="query" type="button" value=" Query " onClick="return execute(' + "'query'" + ')">')
    if loginOk == 1:
        tableColumn(req,'<INPUT NAME="create" type="button" value=" Create " onClick="return execute(' + "'create'" + ')">')	
    tableColumn(req,'<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
    req.write('</TR>')
    req.write('</TABLE>')

def createFunctionButtons(req, db_key, menu_name, help_pdf=pmt_site):
    req.write('<HR>')
    req.write('<TABLE>')
    req.write('<TR>')
    tableColumn(req,'<INPUT NAME="create" type="button" value=" Create " onClick="return execute(' + "'save','" + db_key + "'" + ')">')
    tableColumn(req,'<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
    tableColumn(req,'<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
    req.write('</TR>')
    req.write('</TABLE>')

def editFunctionButtons(req, db_key, menu_name, help_pdf=pmt_site):
    req.write('<HR>')
    req.write('<TABLE>')
    req.write('<TR>')
    tableColumn(req,'<INPUT NAME="save" type="button" value=" Save " onClick="return execute(' + "'save'" + ",'" + db_key + "'" + ')">')
    tableColumn(req,'<INPUT NAME="delete" type="button" value=" Delete " onClick="return execute(' + "'delete'" + ",'" + db_key + "'" + ')">')	
    tableColumn(req,'<INPUT NAME="view" type="button" value=" View " onClick="return execute(' + "'view'" + ", '" + db_key + "'" + ')">')
    tableColumn(req,'<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
    tableColumn(req,'<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
    req.write('</TR>')
    req.write('</TABLE>')

def viewFunctionButtons(req, menu_name, help_pdf=pmt_site):
    req.write('<HR>')
    req.write('<TABLE>')
    req.write('<TR>')
    tableColumn(req,'<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " onClick="return goto_url (' + "'" + menu_name + "'" + ')">')
    tableColumn(req,'<INPUT TYPE="button" NAME="help" VALUE=" Help " onClick="return goto_url (' + "'" + help_pdf + "'" + ')">')
    req.write('</TR>')
    req.write('</TABLE>')

def selectAllColumnsSqlStatement(table_data,table_name,id,id_field_name='id',where_clause=None):

    sqlStatement = "SELECT "

    for columnName in table_data[table_name].keys():
        sqlStatement = sqlStatement + columnName + ", "

    sqlStatement = sqlStatement[:-2]

    if where_clause == None:
        sqlStatement = sqlStatement + " FROM " + table_name + " WHERE " + id_field_name + " = '" + id + "'"

    else:
        sqlStatement = sqlStatement + " FROM " + table_name + " " + where_clause

    return sqlStatement

def set_table_data_read_only(table_data,table_name):
    for field_name in table_data[table_name].keys():
        table_data[table_name][field_name]['display'] = 'read-only'
    return table_data

def print_label(req, label, required=0, wrap=1):
    if wrap:
        wrap_html = ' '
    else:
        wrap_html = "NOWRAP"

    if required:
        req.write('<TD ALIGN=LEFT' + ' ' + wrap_html + '><FONT FACE="Arial,Helvetica" COLOR=RED SIZE="-1">' + '<B>' + label + ':' + '</B>' + '</FONT></TD>')
    else:
        req.write('<TD ALIGN=LEFT' + ' ' + wrap_html + '><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1"><B>' + label + ':</B>' + '</FONT></TD>')

def display_table_item_on_form(req,db,table_data, table_name, field_name, editable=1, display_item_only=0, display_format=1):

    if not display_item_only:
        req.write('<TABLE>')

    if table_data[table_name][field_name]["display"] == 'editable' or \
       table_data[table_name][field_name]["display"] == 'read-only':

        if not display_item_only:

            req.write('<TR>')

            if editable == 1:

                if table_data[table_name][field_name].has_key('required'):

                    if table_data[table_name][field_name]['required']:

                        req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=RED SIZE="-1">')
                        req.write('<B>' + table_data[table_name][field_name]["label"] + ':' + '</B>' + '</FONT></TD>')
                    else:
                        req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">')
                        req.write(table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>')

                else:
                    req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">')
                    req.write(table_data[table_name][field_name]["label"] + ':' + '</FONT></TD>')

            else:
                req.write('<TD ALIGN=LEFT' + ' NOWRAP><FONT FACE="Arial,Helvetica" COLOR=BLACK SIZE="-1">' + '<B>')
                req.write(table_data[table_name][field_name]["label"] + ':</B>' + '</FONT></TD>')

        if not display_item_only:
            req.write('<TD ALIGN=LEFT NOWRAP>')

        # field specified in table data as editable
        if table_data[table_name][field_name]["display"] == 'editable':

            # caller wants for editable
            if editable == 1:

                if table_data[table_name][field_name]["type"] == 'BOOL':
                    if table_data[table_name][field_name]["value"] == 'Yes':
                        optionMenu(req,field_name,"1",["Yes","No"],["SELECTED",""])
                    else:
                        optionMenu(req,field_name,"1",["Yes","No"],["","SELECTED"])

                elif (int(table_data[table_name][field_name]["form_size"]) > 64) and \
                         not table_data[table_name][field_name].has_key('lov'):


                    rows=8
                    if int(table_data[table_name][field_name]["form_size"])<8*64:
                        rows=int(table_data[table_name][field_name]["form_size"])/64

                    textarea(req,
                             table_name,
                             field_name,
                             table_data[table_name][field_name]["value"],
                             `rows`,#`int(table_data[table_name][field_name]["form_size"]) / 64`,

                             '64',
                             table_data[table_name][field_name]["leaveFocus"],
                             table_data[table_name][field_name]["gainFocus"])

                elif table_data[table_name][field_name].has_key('lov'):
                    # display an option menu since the field is only allowed to
                    # be set to the item in a list of value table

                    dbResult = executeSQL(db, table_data[table_name][field_name]['lov'])

                    if dbResult['status'] != 'success':
                        # error could not process sql lov
                        pass
                    else:

                        result = dbResult['result']
                        option_items = []
                        selection_list = []
                        match=0

                        for i in xrange(0,len(result)):
                            item_list = result[i].values()
                            item=''
                            if item_list[0]=="All":
                                item=item_list[0]
                            else:
                                for i in xrange(0,len(item_list)):
                                    item=item+item_list[i]+', '

                                item=item[:-2]

                            option_items.append(item)

                            if item == table_data[table_name][field_name]['value']:
                                selection_list.append("SELECTED")
                                match=1
                            elif string.find(item,','):
                                index=string.find(item,',')
                                if item[:index]==table_data[table_name][field_name]['value']:
                                    selection_list.append("SELECTED")
                                    match=1
                                else:
                                    selection_list.append("")
                            else:
                                selection_list.append("")

                        if match==0:
                            option_items.append(table_data[table_name][field_name]['value'])
                            selection_list.append("SELECTED")
                        optionMenu(req,field_name,"1",option_items,selection_list)

                elif table_data[table_name][field_name].has_key('form_input_type'):
                    form_input_type = table_data[table_name][field_name]['form_input_type']

                    textbox(req,
                            table_name,
                            field_name,
                            table_data[table_name][field_name]["value"],
                            table_data[table_name][field_name]["form_size"],
                            table_data[table_name][field_name]["form_size"],
                            table_data[table_name][field_name]["leaveFocus"],
                            table_data[table_name][field_name]["gainFocus"],
                            form_input_type)

                else:
                    form_input_type = 'text'

                    debug("\n\n<BR>"+  table_data[table_name][field_name]["value"] + "<BR>\n\n")

                    textbox(req,
                            table_name,
                            field_name,
                            table_data[table_name][field_name]["value"],
                            table_data[table_name][field_name]["form_size"],
                            table_data[table_name][field_name]["form_size"],
                            table_data[table_name][field_name]["leaveFocus"],
                            table_data[table_name][field_name]["gainFocus"],
                            form_input_type)

            else:

                req.write(table_data[table_name][field_name]["value"])

        else:
            req.write(table_data[table_name][field_name]["value"])

        if not display_item_only:
            req.write('</TD>')

        if table_data[table_name][field_name].has_key("format"):
            if display_format:
                if editable == 1:
                    tableColumn(req,table_data[table_name][field_name]["format"],'left')

        if not display_item_only:
            req.write('</TR>')

    if not display_item_only:
        req.write('</TABLE>')

#-------------------------------------------------------------------------------
def hasPriv(db,username,priviledge):

    sqlStatement="select %s from priviledges where member_username='%s'" % (priviledge,username)

    result=executeSQL(db, sqlStatement)

    if result['status']!='success':
        return 0

    if len(result['result'])==0:
        return 0

    if result['result'][0][priviledge]=='t':
        return 1

    return 0
#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
def emailList(db, mailserver, list_name, subject, message):
    theList=[]

    sqlStatement="select email from project_members, priviledges where project_members.member_username=priviledges.member_username and %s='t'" % list_name
    mailList=executeSQL(db,sqlStatement)
    for i in xrange(0,len(mailList['result'])):
        theList.append(mailList['result'][i]['email'])

    from_address='support@isrparc.org'

    send_email(mailserver, from_address, theList, subject, message)

#-------------------------------------------------------------------------------

