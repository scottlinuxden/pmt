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

# THESE CONSTANTS NEED MODIFIED PER PROGRAM
cvsroot = '/home/cvsroot/ifc'
web_tree_cvs_exports_dir = '/home/save/rwebexport/cvs_exports'

encapsulation_types = ['tar']

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

def select_list(item_list,selected_item):
    selections = []
    for i in xrange(0,len(item_list)):
        if item_list[i] == selected_item:
            selections.append('SELECTED')
        else:
            selections.append('')
    return selections
            
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
    print '<body bgcolor="#B7BAB7" TEXT="#000000"><FONT SIZE="2" COLOR=BLUE><B>Web CVS Export</B></FONT>'

    exportable_modules = []
    status, module_lines = file_io.readFromFile(cvsroot + '/CVSROOT/modules')

    if status != 'success':
        print 'ERROR: Module data can not be found contact <A HREF="mailto:cm@isrparc.org">CM</A> for more information'
        print '</body></html>'
        sys.exit(1)

    for i in xrange(0,len(module_lines)):
        fields = string.split(string.strip(module_lines[i]))
        if fields != []:
            if fields[0] != '#':
	            exportable_modules.append(fields[0])

    exportable_modules.sort()

    print '<form action="/rwebexport-cgi-bin/rweb_cvs_export.cgi" method="POST" enctype="application/x-www-form-urlencoded">'

    print '<FONT SIZE=2 COLOR=BLACK><B>Proprietary Software Download Site</B><BR><BR>'
    print '<FONT SIZE=2 COLOR=RED>NOTE:</FONT><BR><B>'
    print '      Some of the CVS modules that you download from this site are ISR proprietary<BR>'
    print '      You must be authorized to download these CVS modules.  Once any module(s)<BR>'
    print '      have been downloaded from this site they must not be released to any other<BR>'
    print '      party other than NASA DFRC personnel who have been approved for access to <BR>'
    print '      these  modules. <BR><BR> '
    print '      Some of the module(s) on this site have been provided by other parties for<BR>'
    print '      These modules may have their set of copyrights or access restrictions.<BR>'
    print '      It is the responsibility of the party who downloads such modules to recognize<BR>'
    print '      any copyrights or access restrictions associated with these module(s).</B><BR><BR>'
 
    print '<FONT SIZE=2 COLOR=RED><B>Instructions:</B></FONT><BR><BR>'
    print 'Enter the following information to retrieve the module for download.<BR>'
    print 'The module name is the module name found in the CVS repository.<BR>'
    print 'The release name is the release of the module or enter &quot;now&quot; to retrieve the latest version.<BR>'
    print 'The encapsulation type is Tar.  If you select Tar the encapsulation will be a tar file that is gzipped.<BR><BR>'
    print '<B>NOTE:</B> WinZip 8.0 can extract tar gzipped files as well.<BR><BR>'
    print 'Contact <A HREF="mailto:cm@isrparc.org">CM</A> for more information.'
    print '<TABLE BORDER=0>'

    print '<TR><TD><B>Module Name</B>:</TD><TD>'

    optionMenu('module_name','1',exportable_modules,select_list(exportable_modules,''))
    
    print '</TD></TR>'
    
    print '<TR><TD><B>Release:</B></TD><TD><input name="release" type="text" size="48" maxlength="48" value="%s"></TD></TR>' % (release)

    print '<TR><TD><B>Encapsulation Type:</b></TD><TD>'

    optionMenu('encapsulation_type','1',encapsulation_types,select_list(encapsulation_types,'zip'))
    
    print '</TD></TR>'

    print """</TABLE>
    <HR>
    <input name="submit" type="submit" value="Export">"""
    
    print """</form>
    </body>
    </html>"""
    
print "content-type: text/html\n"

form = cgi.FieldStorage(keep_blank_values=1)

if form.has_key('module_name'):

    print '<html><head><title>Web CVS Export</title></head>'
    print '<body bgcolor="#B7BAB7" TEXT="#000000"><FONT SIZE="2" COLOR=BLUE><B>Web CVS Export</B></FONT>'

    print '<TABLE BORDER=0>'
    print '<TR><TD>'

    if string.upper(string.strip(form['encapsulation_type'].value)) == 'TAR':
        module_filename = string.strip(form['module_name'].value) + '.tar.gz'
    elif string.upper(string.strip(form['encapsulation_type'].value)) == 'ZIP':
        module_filename = string.strip(form['module_name'].value) + '.zip'

    os.environ['CVSROOT'] = cvsroot
    encapsulated_file_location = web_tree_cvs_exports_dir + '/' + form['module_name'].value

    if not os.path.exists(encapsulated_file_location):
        os.mkdir(encapsulated_file_location)

    if string.upper(string.strip(form['release'].value)) == 'NOW':

	data = []
	data.append('ISR CVS Export for the module :%s' % (form['module_name'].value))
        data.append('User exported from the IFC repository: %s' % (cvsroot))
        data.append('User exported current version of all files in the module using NOW keyword')
        data.append('The date when CVS export occurred was %s' % (time_pkg.current_time_MM_DD_YYYY()))
	data.append('')

        data.append('Institute for Software Research (ISR), Inc.')
    	data.append('1000 Technology Drive')
   	data.append('Suite 3210')
	data.append('Fairmont, WV  26554')
    	data.append('Voice: 304-368-9300')
    	data.append('FAX: 304-534-4106')
    	data.append('E-mail: cm@isrparc.org')

        status, details = file_io.writeToFile(encapsulated_file_location + '/MODULE_VERSION',data)

	status, export_output, tar_ball_contents = cvs_utils.cvs_export_encapsulate_distribution(form['module_name'].value,form['encapsulation_type'].value,web_tree_cvs_exports_dir + '/' + form['module_name'].value,'now',None,0)

        if status != 'success':
            export_output = """<BR><BR><FONT SIZE=2 COLOR=RED>Can not find module specified.  Export aborted!</FONT>
            </TD></TR>
            </TABLE><BR>"""
            
    elif string.strip(form['release'].value) != '':

	data = []
	data.append('ISR CVS Export for the module :%s' % (form['module_name'].value))
        data.append('User exported from the IFC repository: %s' % (cvsroot))
        data.append('User exported version %s of this module' % (string.strip(form['release'].value)))
        data.append('The date when CVS export occurred was %s' % (time_pkg.current_time_MM_DD_YYYY()))
	data.append('')

        data.append('Institute for Software Research (ISR), Inc.')
    	data.append('1000 Technology Drive')
   	data.append('Suite 3210')
	data.append('Fairmont, WV  26554')
    	data.append('Voice: 304-368-9300')
    	data.append('FAX: 304-534-4106')
    	data.append('E-mail: cm@isrparc.org')

        status, details = file_io.writeToFile(encapsulated_file_location + '/MODULE_VERSION',data)

        status, export_output, tar_ball_contents = cvs_utils.cvs_export_encapsulate_distribution(form['module_name'].value,form['encapsulation_type'].value,web_tree_cvs_exports_dir + '/' + form['module_name'].value,None,string.strip(form['release'].value),0)


        if status != 'success':
            export_output = """<BR><BR><FONT SIZE=2 COLOR=RED>Can not find module specified.  Export aborted!</FONT>
            </TD></TR>
            </TABLE><BR>"""
            
    else:
    	print '<BR><FONT SIZE="2" COLOR=RED><B>No release information provided.  Export aborted!</B></FONT></TD></TR>'
    	print '</TABLE><BR>'
    
    	print """</body>
        </html>"""
	sys.exit(1)

    if status != 'success':
    	print '<BR><FONT SIZE="2" COLOR=RED><B>Module: %s can not be found</B></FONT></TD></TR>' % (form['module_name'].value)

    else:
    	print '<FONT SIZE="2" COLOR=RED><B>You can download the requested exported file by clicking on the link below:</B></FONT></TD></TR>'
    	print '<TR><TD><A HREF="/rwebexport-cvs-exports/%s">%s</A></TD></TR>' % (module_filename,module_filename)
   	print '<TR><TD><FONT SIZE="2" COLOR=RED><B>Contents of the file are:</B></FONT></TD></TR>'
	export_output = tar_ball_contents

    print '<TR><TD>'
    print '<PRE>'

    print export_output

    print '</PRE>'
    print '</TD></TR>'
    print '</TABLE><BR>'
    
    print """</body>
    </html>"""
            
else:
    display_form(form)
