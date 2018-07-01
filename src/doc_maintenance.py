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

import sys
import os
import cgi
import glob
import string
import declarations
import pmt_utils
import os_utils
import db_authentication
import commands
import os_utils
import authentication


#-----------------------------------------------------------------------------
def mail_support(msg=""):
    email_addr = db_name +"_document_maintenance@linuxden.com"

    content = "---------------------------------------\n"
    content = content + msg + '\n\n'

    for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR',
               'HTTP_FROM','REMOTE_HOST','REMOTE_PORT',
               'SERVER_SOFTWARE','HTTP_REFERER','REMOTE_IDENT',
               'REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
        if os.environ.has_key(x):
            line = "%s: %s\n" % (x, os.environ[x])
            content = content + line

    content = content + "---------------------------------------\n"

    db_label=string.upper(db_name)
    if db_label=="SAVE":
        db_label="IFCS"
    elif db_label=="BUAV":
        db_label="FCST"
    elif db_label=="CUAB":
        db_label="PADV"
    subject="%s Documentation Maintenance Report" % db_label
    pmt_utils.send_email('www.linuxden.com',
                         email_addr,[email_addr],
                         subject,content)
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def display_form(display_files=0,alerts=None):
    print "<HTML>"
    print "<HEAD>"
    pmt_utils.javaScript("doc_maintenance")
    pmt_utils.title("Documentation Maintenance")
    print "</HEAD>"
    pmt_utils.bodySetup()
    pmt_utils.mainHeading('Documentation Maintenance')
    pmt_utils.subHeading('Create and Delete Folders/Files')
    pmt_utils.formSetup("doc_maintenance",db_name,"doc_maintenance",None)

    dbResult=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                                 declarations.pmt_info['browser_password'],
                                 declarations.pmt_info['db_name'])
    if dbResult['status']!='success':
        exit(dbResult['message'])

    db=dbResult['result']
    status,details = db_authentication.password_valid(db,
                                                      crypt_salt=db_name,
                                                      username=username,
                                                      password=password)
    if status!='success':
        exit(details)

    if not pmt_utils.hasPriv(db,username,'folder_admin'):
        msg="User %s does not have folder maintenance priviledges" % username
        exit(msg)
        
    print '<hr><br><CENTER><B>Delete Folders/Files</B></CENTER>'
    stripped_db=string.lower(string.strip(db_name))
    os.chdir(os.path.join('/home',stripped_db,'documents'))

    file_list = os_utils.walk_list_files(
        directory_name='.',
        list_only_files=0,
        exclude_list = [],
        include_file_type=1)

    if len(file_list) > 25:
        list_size = 25
    else:
        list_size = len(file_list)

    print '<BLINK><B>WARNING:</B></BLINK><br>'
    print 'Any folders or files that you select for deletion are '
    print 'permanently deleted.  You should have a local backup of '
    print 'any folders/files you delete in case you really did not mean '
    print 'to delete.  Backups are crucial.  You have been warned.'
    print '<p>Selecting a folder will delete the folder and all files '
    print 'under it including sub folders.  '
    print 'Select folder names with caution.'
    print '<p>Your deletes will not be confirmed.  '
    print 'When you press [Delete Folders/Files] your files are deleted.'

    print '<BR><CENTER><B>Select folders/files to delete</B>:<BR>'
    print '<SELECT NAME="files_to_remove" SIZE="8" MULTIPLE>'
    for curfile in file_list:
        print '<OPTION>%s' % (curfile)
    print "</SELECT><br>"
    java_call="return execute('delete_folder','1')"
    print '<input name="delete_folder" type="button" '
    print 'value=" Delete Folders/Files " onClick="%s">' % java_call
    print '<input name ="website_name_hidden" '
    print 'type="hidden" value="%s">' % (db_name)
    print "<hr><BR><BR>"

    print '<CENTER><B>Create Folder</B></CENTER><BR>'
    print '<B>Folder Name</B>:&nbsp;'
    print '<input name="folder" type="text" size="50" maxlength="100"><BR>'
    java_call="return execute('create','1')"
    print '<input name="create" type="button" '
    print 'value=" Create Folder " onClick="%s">' % java_call
    print '<input name ="website_name_hidden" '
    print 'type="hidden" value="%s"><hr>' % (db_name)

    if alerts != None:
        pmt_utils.alertsArea(form,alerts)

    print '</CENTER>'

    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'key_id', '1', '10', '10', None, None,'hidden')

    print '</form>'
    print '<p align="right">'
    print '<A HREF="mailto:support@isrparc.org">Contact Support Team</a>'
    print "</body></html>"
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doDeleteFolder():

    if form.has_key('files_to_remove'):
        files_to_remove = []
        option_lines = pmt_utils.formOptionListToList(form,'files_to_remove')

        for option_line in option_lines:
            line_item = string.splitfields(option_line,':')
            files_to_remove.append(string.strip(line_item[0]))

        alerts=''
        for curfile in files_to_remove:

            filepath=os.path.join('/home',db_name,'documents',curfile)

            if os.path.isdir(filepath):
                status, output = os_utils.super_remove(filepath)
                if status == 'error':
                    alerts=alerts+"Can't remove directory %s.\n" % curfile
                    alerts=alerts+"%s\n" % output
                    break
                else:
                    alerts=alerts+ 'Directory deleted: %s\n' % curfile

            elif os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                except OSError, details:
                    alerts=alerts+"Can't remove the file %s.\n" % curfile
                    alerts=alerts+"%s\n" % output
                    break

                alerts=alerts+ 'File deleted: ' + curfile + '\n'
        mail_support(alerts)
    else:
        # user did not select any files
        alerts='Select file(s) or directory(s) to delete.'

    display_form(alerts=alerts)

#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def doCreate():
    
    folder=string.lower(string.strip(form['folder'].value))
    if folder != '':
        try:
            path='/home/%s/documents/%s' % (db_name,folder)
            os.makedirs(path,0700)
        except OSError, details:
            alerts = 'Can not create folder: %s.\n%s\n' % (folder,details)
        else:
            alerts = 'Folder created: %s\n' % folder
            mail_support(alerts)

    display_form(alerts=alerts)
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

    create_priv=0

    #url='/%s/html/sprsum.html' % db_name
    #pmt_utils.queryFunctionButtons(create_priv, url)
    print '<HR>'
    print '<TABLE><TR>'
    java="return goto_url ('doc_maintenance.pyc')"
    html='<INPUT TYPE="button" NAME="return_to_menu" VALUE=" Listing " '
    html=html+'onClick="%s">' % java
    pmt_utils.tableColumn(html)
    print '</TR></TABLE>'

    pmt_utils.textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    pmt_utils.textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
        pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
if os.environ.has_key("HTTP_USER_AGENT"):
    browser = os.environ["HTTP_USER_AGENT"]
else:
    browser = "No Known Browser"

if os.environ.has_key("SCRIPT_NAME"):
    posturl = os.environ["SCRIPT_NAME"]
else:
    posturl = ""

pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)





if form.has_key("action"):

    if form['action'].value == 'delete_folder':
        doDeleteFolder()

    elif form['action'].value == 'create':
        doCreate()
    else:
        display_form()

else:
    display_form()
    


