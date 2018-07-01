#!/usr/bin/env python
# -*- Mode: Python; tab-width: 4 -*-
# $Id$
# Copyright (C) 1999 LinuXden, All Rights Reserved
# Copright Statement at http://www.linuxden.com/copyrighted_apps.html
# 

import sys,os,cgi,glob,string
import os_utils
import commands
import urllib
import time_pkg
import file_io
import cvs_utils
import declarations
import pmt_utils


#------------------------------------------------------------------------
def optionMenu(name, size, options, selected):
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
    print '<FONT FACE="Arial,Helvetica" SIZE="2">'
    print '<SELECT NAME="' + name + '" SIZE=' + size + '>\n'
    for i in range(0,len(options)):
        print '<OPTION ' + selected[i] + '>' + options[i] + '\n'
    print '</SELECT>'
    print '</FONT>'
#------------------------------------------------------------------------


#------------------------------------------------------------------------
def select_list(item_list,selected_item):
    selections = []
    for i in xrange(0,len(item_list)):
        if item_list[i] == selected_item:
            selections.append('SELECTED')
        else:
            selections.append('')
    return selections
#------------------------------------------------------------------------


#------------------------------------------------------------------------
def display_form(form):

    module_name = ''
    release = ''

    if form.has_key('module_name'):
        module_name = form['module_name'].value

    if form.has_key('release'):
        release = form['release'].value

    if form.has_key('encapsulation_type'):
        encapsulation_type = form['encapsulation_type'].value

    print '<html><head><title>Web CVS Export</title></head>'
    print '<body background="/%s/icons/circ_bg.jpg"' % db_name
    print 'bgcolor="#B7BAB7" TEXT="#000000">'
    print '<FONT SIZE="2" COLOR=BLUE><B>Web CVS Export</B></FONT>'

    exportable_modules = []
    modFilename=cvsroot + '/CVSROOT/%s.modules' % db_name
    status, module_lines = file_io.readFromFile(modFilename)

    if status != 'success':
        msg="ERROR: Module data can not be found."
        msg="%s  Contact cm@isrparc.org for more information" % msg
        exit(msg)
        #print 'ERROR: Module data can not be found.  Contact'
        #print '<A HREF="mailto:cm@isrparc.org">CM</A> for more information'
        #print '</body></html>'
        #sys.exit(1)

    for i in xrange(0,len(module_lines)):
        fields = string.split(string.strip(module_lines[i]))
        if fields != []:
            if fields[0] != '#':
                if len(fields) >= 3:
                    if fields[2] !='#web_export_disabled':
                        exportable_modules.append(fields[0])
                else:
                    exportable_modules.append(fields[0])

    exportable_modules.sort()

    link='/%s-cgi-bin/web_cvs_export.pyc' % db_name
    print '<form action="%s" method="POST"' % link
    print 'enctype="application/x-www-form-urlencoded">'

    print '<FONT SIZE="2" COLOR=RED><B>Instructions:</B></FONT><BR><BR>'
    print 'Enter the following information to retrieve'
    print 'the module for download.<BR>'
    print 'The module name is the module name found in the CVS repository.<BR>'
    print 'The release name is the release of the module '
    print 'or enter &quot;now&quot; to retrieve the latest version.<BR>'
    print 'The encapsulation type is Tar.  If you select Tar the'
    print 'encapsulation will be a tar file that is gzipped.<BR><BR>'
    print '<B>NOTE:</B> WinZip 8.0 can extract tar gzipped files.<BR><BR>'
    print 'Contact <A HREF="mailto:cm@isrparc.org">CM</A> for more info.'
    print '<TABLE BORDER=0>'

    print '<TR><TD><B>Module Name</B>:</TD><TD>'
    optionMenu('module_name','1',
               exportable_modules,
               select_list(exportable_modules,''))
    print '</TD></TR>'

    print '<TR><TD><B>Release:</B></TD><TD>'
    print '<input name="release" type="text" size="48" maxlength="48"'
    print 'value="%s"></TD></TR>' % (release)
    
    print '<TR><TD><B>Encapsulation Type:</b></TD><TD>'
    optionMenu('encapsulation_type','1',
               encapsulation_types,
               select_list(encapsulation_types,'zip'))
    print '</TD></TR>'

    print '</TABLE><HR>'
    print '<input name="submit" type="submit" value="Download">'
    print '</form></body></html>'
#------------------------------------------------------------------------


#------------------------------------------------------------------------
def doPublicAccess():
    module_name='MultiUAV'
    release='now'
    encapsulation_type='tar'

    print '<html><head><title>Web CVS Export</title></head>'
    print '<body background="/%s/icons/circ_bg.jpg"' % db_name
    print 'bgcolor="#B7BAB7" TEXT="#000000">'
    print '<FONT SIZE="2" COLOR=BLUE><B>Web CVS Export</B></FONT>'
    print '<form method=post>'
    print 'Public Area<BR>'
    print '<input type=hidden name=module_name value="%s">' % module_name
    print '<input type=hidden name=release value="%s">' % release
    print '<input type=hidden name=encapsulation_type'
    print 'value="%s">' % encapsulation_type
    print '<input type=submit name=submit value="Get Public Release">'
    print '</form>'
    print '</body></html>'
#------------------------------------------------------------------------



#-----------------------------------------------------------------------------
def pageEnd(table_data,db):
    print "</FORM>"
    pmt_utils.trailer(table_data, db)
    db.close()
    print "</BODY>"
    print "</HTML>"    
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
def exit(message,table_data=None,display_login=1):

    if display_login:
        pmt_utils.usernamePasswordDisplay(username)
    pmt_utils.alertsArea(form, message);

    #if username!=None and db!=None:
    #    create_priv=pmt_utils.hasPriv(db,username,'create_spr')
    #else:
    #    create_priv=0

    #url='/%s/html/sprsum.html' % db_name
    #pmt_utils.queryFunctionButtons(create_priv, url)

    textbox(None, 'key_id', '', '10', '10', None, None, 'hidden')
    textbox(None, 'action', '', '10', '10', None, None, 'hidden')
    textbox(None, 'item_no', '', '8', '8', None, None, 'hidden')
    
    if table_data!=None and db!=None:
        pageEnd(table_data,db)
    sys.exit()
#-----------------------------------------------------------------------------

#------------------------------------------------------------------------
# THESE CONSTANTS NEED MODIFIED PER PROGRAM
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()

db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if db_name=='save':
    cvs_db_name='ifc' 
else:
    cvs_db_name=db_name
cvsroot = '/home/cvsroot/%s' % cvs_db_name
web_cvs_dir = '/home/%s/cvs_exports/' % db_name
encapsulation_types = ['tar']


#------------------------------------------------------------------------
if form.has_key('module_name'):

    print '<html><head>'
    pmt_utils.title("Web CVS Export")
    print '</head>'
    pmt_utils.bodySetup()
    pmt_utils.mainHeading("Web CVS Export")

    print '<TABLE BORDER=0>'
    print '<TR><TD>'

    if not form.has_key('encapsulation_type'):
        msg="No encapsulation type specified"
        exit(msg)
    elif string.upper(string.strip(form['encapsulation_type'].value)) == 'TAR':
        module_filename = string.strip(form['module_name'].value) + '.tar.gz'
    elif string.upper(string.strip(form['encapsulation_type'].value)) == 'ZIP':
        module_filename = string.strip(form['module_name'].value) + '.zip'


    module_path = None
    module_list_file=cvsroot + '/CVSROOT/%s.modules' % db_name
    #print "<BR>module_list_file:%s<BR>" % module_list_file
    status, module_lines = file_io.readFromFile(module_list_file)

    if status != 'success':
        msg="Module data can not be found."
        msg="%s  Contact cm@isrparc.org for more information." % msg
        exit(msg)

    # for each line in the modules file ...
    for i in xrange(0,len(module_lines)):
        # ... split the line into fields
        fields = string.split(string.strip(module_lines[i]))

        # if this is a blank line...
        if fields == []:
            # ...skip to next line
            continue

        # if this line is commented out...
        #if fields[0] != '#':
        if fields[0][0]=='#':
            # ...skip to next line
            continue

        # if there is only one field...
        if len(fields)==1:
            # then this is an invalid line so skip to the next line
            continue

        # if there are two fields...
        if len(fields)==2:
            # ...then if the first field matches the specified module...
            if fields[0]==form['module_name'].value:
                # ...then set the module path to the value in the second field
                module_path=fields[1]

        # if there are 3 or more fields...
        if len(fields) >= 3:
            # ... then if the thrid field does not disable web_export...
            if fields[2] !='#web_export_disabled':
                # ... then if the first field is the specified module...
                if fields[0]==form['module_name'].value:
                    # ... then set module path to the value in the second field
                    module_path=fields[1]

    os.environ['CVSROOT'] = cvsroot
    #print "<BR>"+cvsroot +"<BR>"
    encapsulated_file_location=web_cvs_dir+form['module_name'].value

    if not os.path.exists(encapsulated_file_location):
        os.mkdir(encapsulated_file_location)

    if string.upper(string.strip(form['release'].value)) == 'NOW':

        data = []
        msg='ISR CVS Export for module :%s' % (form['module_name'].value)
        data.append(msg)
        msg='User exported from the %s repository:' % string.upper(cvs_db_name)
        data.append("%s %s" % (msg,cvsroot))
        msg='User exported current version of all files in the module'
        msg='%s using NOW keyword' % msg
        data.append(msg)
        date=time_pkg.current_time_MM_DD_YYYY()
        data.append('The date when CVS export occurred was %s' % (date))
        data.append('')

        data.append('Institute for Software Research (ISR), Inc.')
        data.append('1000 Technology Drive')
        data.append('Suite 3210')
        data.append('Fairmont, WV  26554')
        data.append('Voice: 304-368-9300')
        data.append('FAX: 304-534-4106')
        data.append('E-mail: cm@isrparc.org')

        outFilename=encapsulated_file_location + '/MODULE_VERSION'
        status, details = file_io.writeToFile(outFilename,data)

        outFilename=web_cvs_dir + '/' + form['module_name'].value
        result=cvs_utils.cvs_export_encapsulate_distribution(
                                              form['module_name'].value,
                                              form['encapsulation_type'].value,
                                              outFilename,
                                              'now',None,1,module_path)
        status,export_output,tar_ball_contents = result

        if status != 'success':
            export_output = '<BR><FONT SIZE="3" COLOR=RED>%s<BR>'%export_output
            export_output = '%sCan not find module specified.'   %export_output
            export_output = '%s Export aborted!'                 %export_output
            export_output = '%s</FONT></TD></TR></TABLE><BR>'    %export_output

    elif string.strip(form['release'].value) != '':

        data = []
        msg='ISR CVS Export for the module :%s' % (form['module_name'].value)
        data.append(msg)
        msg='User exported from the %s repository:' % string.upper(cvs_db_name)
        data.append("%s %s" % (msg,cvsroot))
        msg='User exported version %s' % (string.strip(form['release'].value))
        msg='%s of this module' % msg
        data.append(msg)
        date=time_pkg.current_time_MM_DD_YYYY()
        data.append('The date when CVS export occurred was %s' % date)
        data.append('')

        data.append('Institute for Software Research (ISR), Inc.')
        data.append('1000 Technology Drive')
        data.append('Suite 3210')
        data.append('Fairmont, WV  26554')
        data.append('Voice: 304-368-9300')
        data.append('FAX: 304-534-4106')
        data.append('E-mail: cm@isrparc.org')

        outFilename=encapsulated_file_location + '/MODULE_VERSION'
        status, details = file_io.writeToFile(outFilename,data)

        outFilename=web_cvs_dir + '/' + form['module_name'].value
        result=cvs_utils.cvs_export_encapsulate_distribution(
                                         form['module_name'].value,
                                         form['encapsulation_type'].value,
                                         outFilename,
                                         None,
                                         string.strip(form['release'].value),
                                         0,module_path)
        status, export_output, tar_ball_contents = result
        
        if status != 'success':
            export_output = '<BR><BR><FONT SIZE="3" COLOR=RED>'
            export_output = '%sCan not find module specified.' % export_output
            export_output = '%s  Export aborted!'              % export_output
            export_output = '%s</FONT></TD></TR></TABLE><BR>'  % export_output

    else:
        print '<BR><FONT SIZE="2" COLOR=RED><B>'
        print 'No release information provided.  Export aborted!'
        print '</B></FONT></TD></TR></TABLE><BR></body></html>'
        sys.exit(1)

    if status != 'success':
        print '<BR><FONT SIZE="2" COLOR=RED><B>'
        print 'Module: %s can not be found' % (form['module_name'].value)
        print '</B></FONT></TD></TR>'

    else:
        print '<FONT SIZE="2" COLOR=RED><B>'
        print 'Download the exported file by clicking on the link below:'
        print '</B></FONT></TD></TR>'
        link='/%s-cvs-exports/%s' % (cvs_db_name,module_filename)
        print '<TR><TD><A HREF="%s">%s</A></TD></TR>' % (link,module_filename)
        print '<TR><TD><FONT SIZE="2" COLOR=RED><B>'
        print 'Contents of the file are:</B></FONT></TD></TR>'
        export_output = tar_ball_contents
        print '<TR><TD><PRE>'        
        print export_output
        print '</PRE></TD></TR>'
        print '</TABLE><BR>'

    print '</body></html>'
#------------------------------------------------------------------------

else:
    db=pmt_utils.connectDB(declarations.pmt_info['browser_username'],
                           declarations.pmt_info['browser_password'],
                           declarations.pmt_info['db_name'])

    if db['status'] != 'success':
        msg="Can not connect to database,\n" + db['message']
        exit(msg)
 
    display_form(form)   
