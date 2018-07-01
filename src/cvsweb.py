# $Id: cvsweb.py,v 1.3 2005/04/12 16:31:12 lliabraa Exp $
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Scott Davis
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#

import os, string, sys
import cgi, glob
from pg import DB
import urllib
import os_utils
import pmt_utils
import declarations
import time_pkg
import time
import stat
import file_io
import db_authentication


#------------------------------------------------------------------------------
def displayLogin(form,alert=None):
	print "<HTML>"
	print "<HEAD>"
	pmt_utils.javaScript("cvsweb")
	pmt_utils.title("Development Library")
	print "</HEAD>"
	pmt_utils.bodySetup()
	pmt_utils.mainHeading('Development Library')
	pmt_utils.subHeading('Login')
	pmt_utils.formSetup("cvsweb",
			    db_name,
			    "cvsweb",
			    "return submitForm(document.cvsweb)")
	pmt_utils.usernamePasswordDisplay()
	if alert!=None:
		pmt_utils.alertsArea(form, alert)
	print "<hr><INPUT TYPE='submit' NAME='submit' value='Submit' >"
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def verifyUserPass():
	db = pmt_utils.connectDB(declarations.pmt_info['browser_username'],
				 declarations.pmt_info['browser_password'],
				 declarations.pmt_info['db_name'])

	# could not connect to db
	if db['status'] != 'success':
		message= "Can not connect to database,\n" + db['message']
		pmt_utils.alertsArea(form,message)
		displayLogin(form)
		sys.exit(1)
	
	status, details = db_authentication.password_valid(db['result'],
							   crypt_salt=db_name,
							   username=username,
							   password=password)
	if status != 'success':
		displayLogin(form,details)
		sys.exit(1)

	cvs_web_priv=pmt_utils.hasPriv(db['result'],username,'cvs_web')
	cvs_export_priv=pmt_utils.hasPriv(db['result'],username,'cvs_export')

	if cvs_web_priv==0 and cvs_export_priv==0:
		message='User %s does not have access to CVS' % username
		displayLogin(form, message)
		sys.exit()

	return cvs_web_priv,cvs_export_priv
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def printPage(cvs_web_priv,cvs_export_priv):
    print '<!DOCTYPE doctype PUBLIC "-//w3c/dtd html 4.0 transitional//en">'
    print '<html><head>'
    print '<meta http-equiv="Content-Type" content="text/html;'
    print 'charset=iso-8859-1">'
    print '<meta name="GENERATOR"'
    print 'content="Mozilla/4.5 [en] (X11; I; Linux 2.0.36 i686)[Netscape]">'
    print '<title>Development Library</title></head>'
    print '<b><font color="#000099" size="2">Development Library</font></b>'
    print '<hr size="1" noshade="noshade" width="100%">'
    print 'You may access the Program Development Library Modules via a web'
    print 'interface or you may export a CVS modules that will be encapsulated'
    print 'in a WinZip file for download.<br><br>'
    print '<b>NOTE:</b>'
    print 'If you download an exported CVS module and want to make changes'
    print 'the changes you make will not be recorded in CVS as you make'
    print 'changes since the CVS repository directories will not be contained'
    print 'within the encapsulated file.  <br>'
    print '<hr size="1" noshade="noshade" width="100%">'
    print '<b><font color="#990000" size="2">Options</font></b><br>'
    print '<ul>'

    if cvs_web_priv==1:
        print '<li><a href="/%s-cvs-web/viewcvs.cgi">CVS Web</a><br>'%(db_name)

    if cvs_export_priv==1:
        url='/%s-cgi-bin/web_cvs_export.pyc' % db_name
        print '</li><li><a href="%s">Export and Download CVS Module</a>' % url

    print '</li></ul>'
    print '<script>'
    print 'document.write("Last Modified:"+ document.lastModified);'
    print '</script>Last Modified:Wed, 27 Jun 2001 17:32:05 GMT'
    print '</body></html>'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']
username,password=pmt_utils.getUserPass(form)

if username==None:
	displayLogin(form)
else:
	pmt_utils.bodySetup()
	cvs_web_priv,cvs_export_priv = verifyUserPass()
	printPage(cvs_web_priv,cvs_export_priv)
#------------------------------------------------------------------------------



