# $Id: clean_site.py,v 1.1 2003/12/30 17:21:42 lliabraa Exp $
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
#   E-mail: rsdavis@linuxden.com
#   Voice:  304.534.3031
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

email = declarations.pmt_info['db_name'] + "_cleaning@isrparc.org"	 # where to email upload reports;

def clean_results(html_message, email_message, form):
	print "<HTML><HEAD><TITLE>Clean Results</TITLE></HEAD><BODY>"
	print '<h3>Clean Results</h3>'
	print '<BLINK><STRONG>NOTE: All clean site maintenance is logged.</STRONG></BLINK><BR>'
	print html_message
	print "</BODY></HTML>"
    
	email_header = 'Website name: ' + declarations.pmt_info['db_name'] + '\n'
	email_header = email_header + 'Username: ' + form['username'].value + '\n\n'
	mail_support(email_header + email_message)
    
def mail_support(msg=""):
		
	if email:
        
		content = "---------------------------------------\n"
		content = content + msg + '\n\n'
		
		for x in [ 'REQUEST_URI','HTTP_USER_AGENT','REMOTE_ADDR','HTTP_FROM','REMOTE_HOST','REMOTE_PORT','SERVER_SOFTWARE','HTTP_REFERER','REMOTE_IDENT','REMOTE_USER','QUERY_STRING','DATE_LOCAL' ]:
			if os.environ.has_key(x):
				line = "%s: %s\n" % (x, os.environ[x])
				content = content + line

		content = content + "---------------------------------------\n"
        
		pmt_utils.send_email('www.isrparc.org',email,[email],"Clean Site Report",content)

def display_form(display_files=0,alerts=None):
	print "<HTML>"

	print "<HEAD>"

	pmt_utils.title("Site Maintenance (Clean)")

	print "</HEAD>"

	pmt_utils.bodySetup()

	pmt_utils.mainHeading('Site Maintenance')

	pmt_utils.subHeading('Clean')

	pmt_utils.formSetup("clean_site",declarations.pmt_info['db_name'],"clean_site",None)

	if not display_files:
		print '<TABLE BORDER=0><TR><TD><B>Username</B>:</TD><TD><input name="username" type="text" size="9" maxlength="9"></TD></TR><TR><TD><B>Password:</B></TD><TD><input name="password" type="password" size="8" maxlength="8"></TD></TR></TABLE>'

	if display_files:

		os.chdir(os.path.join('/home',string.lower(string.strip(declarations.pmt_info['db_name'])),'documents'))

		file_list = os_utils.walk_list_files(
			directory_name='.',
			list_only_files=0,
			exclude_list = [],
			include_file_type=1)

		if len(file_list) > 25:
			list_size = 25
		else:
			list_size = len(file_list)

		print """
		<CENTER>
		<TABLE BORDER=0>
		<CAPTION><BLINK><B>WARNING:<B></BLINK></CAPTION>
		<TR><TD WIDTH=300>
		Any files that you select for deletion are permanently deleted.  You should have a local
		backup of any files you delete in case you really did not mean to delete.
		Backups are crucial.  You have been warned.
		<p>Selecting a directory will delete the directory and all files under it including subdirectories.
		Select directory names with caution.
		<p>Your deletes will not be confirmed.  When you press [Delete Selected Files] your files
		are deleted.</TD></TR></TABLE>
		"""
		print '<BR><CENTER><B>Select files to delete</B>:<BR><SELECT NAME="files_to_remove" SIZE="%d" MULTIPLE>' % (list_size)

		for curfile in file_list:
			print '<OPTION>%s' % (curfile)
        
		print "</SELECT><BR>"

	if alerts != None:
		pmt_utils.alertsArea(form,alerts)

	print '</CENTER>'
	
	print """
	<CENTER>
    <HR>
	"""
	
	if display_files:
		print '<input name="submit" type="submit" value="Delete Selected Files">'
	else:
		print '<input name="submit" type="submit" value="Login">'
		

	print '</CENTER>'

	if display_files:

		print '<input name ="website_name_hidden" type="hidden" value="%s">' % (declarations.pmt_info['db_name'])
		
	print """
	<p align="right"><A HREF="mailto:support@isrparc.org">Contact Support Team</a>
    </form>
    </body>
    </html> 
	"""
    
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

if form.has_key('username'):

	dbResult = pmt_utils.connectDB(declarations.pmt_info['browser_username'], declarations.pmt_info['browser_password'], declarations.pmt_info['db_name'])
	
	# could not connect to db
	if dbResult['status'] != 'success':

		display_form(form, 'Can not verify user. Can not connect to database.')
		sys.exit(1)
	else:
		
		db = dbResult['result']
		
		# validate user based on db username password
		# need to check if user can perform clean
		# status, details = db_authentication.password_valid(db,
		#						   crypt_salt=declarations.pmt_info['db_name'],
		#						   username=form['username'].value,
		#						   password=form['password'].value)
		# if status != 'success':
	    
		status, found = authentication.password_valid(os.path.join('/home',string.lower(string.strip(declarations.pmt_info['db_name'])),'admin','clean.passwd'),declarations.pmt_info['db_name'],form['username'].value,form['password'].value)
		if (status != 'success') or (found == 0):
			details = 'Invalid username/password specified.' 
			html_msg = "%s<BR>" % (details)
			email_msg = details
			clean_results(html_msg, email_msg, form)
			sys.exit(1)

		if not os.path.exists(os.path.join('/home', string.lower(string.strip(declarations.pmt_info['db_name'])))):
			html_msg = "Website, " + declarations.pmt_info['db_name'] + ", does not exist.<BR>No clean site maintenance can be performed.<BR>"
			email_msg = "Website, " + declarations.pmt_info['db_name'] + ", does not exist.\nNo clean site maintenance can be performed.\n"
			clean_results(html_msg, email_msg, form)
			sys.exit()
			
		display_form(display_files=1)
		
else:

	if form.has_key('files_to_remove'):

		alerts = None
		email_msg = ''
		files_to_remove = []

		option_lines = pmt_utils.formOptionListToList(form,'files_to_remove')

		for option_line in option_lines:
			line_item = string.splitfields(option_line,':')
			files_to_remove.append(string.strip(line_item[0]))

		for curfile in files_to_remove:

			if os.path.isdir(os.path.join('/home',declarations.pmt_info['db_name'],'documents',curfile)):
				status, output = os_utils.super_remove(os.path.join('/home',declarations.pmt_info['db_name'],'documents',curfile))
				if status == 'error':
					alerts = 'Can not remove the directory, %s, permission denied or no longer exists.' % (curfile)
					email_msg = email_msg + alerts + '\n'
					break
				else:
					email_msg = email_msg + 'Directory deleted: ' + curfile + '\n'
				
			elif os.path.isfile(os.path.join('/home',declarations.pmt_info['db_name'],'documents',curfile)):
				try:
					os.remove(os.path.join('/home',declarations.pmt_info['db_name'],'documents',curfile))
				except OSError, details:
					alerts = 'Can not remove the file, %s, permission denied or no longer exists.' % (curfile)
					email_msg = email_msg + alerts + '\n'
					break

				email_msg = email_msg + 'File deleted: ' + curfile + '\n'
				
		display_form(display_files=1,alerts=alerts)

		email_header = 'Website name: ' + declarations.pmt_info['db_name'] + '\n'
		mail_support(msg=email_header+email_msg)
			
	else:

		if form.has_key('website_name_hidden'):
			# Processing data from screen other than login
			if not form.has_key('files_to_remove'):
				# user did not select a file
				display_form(display_files=1,alerts='Select file(s) or directory(s) to delete.')
				sys.exit()
			
		else:
			display_form()

