import pmt_utils
import sys
import string
import smtplib

pmt_utils.htmlContentType()

def validate():
	valid='true'

	if form['project_name'].value=='':
		valid='false'
	if form['name'].value=='':
		valid='false'
	if form['org'].value=='':
		valid='false'
	if form['address'].value=='':
		valid='false'
	if form['city'].value=='':
		valid='false'
	if form['state'].value=='':
		valid='false'
	if form['zip'].value=='':
		valid='false'
	if form['phone'].value=='':
		valid='false'
	if form['email']=='':
		valid='false'
	if form['reason'].value=='':
		valid='false'

	return valid

def getData():
	if form.has_key('project_name'):
		project_name=form['project_name'].value
	else:	project_name=''
	if form.has_key('name'):
		name=form['name'].value
	else:	name=''
	if form.has_key('org'):
		org=form['org'].value
	else:	org=''
	if form.has_key('address'):
		address=form['address'].value
	else:	address=''
	if form.has_key('city'):
		city=form['city'].value
	else:	city=''
	if form.has_key('state'):
		state=form['state'].value
	else:	state=''
	if form.has_key('zip'):
		zip=form['zip'].value
	else:	zip=''
	if form.has_key('phone'):
		phone=form['phone'].value
	else:	phone=''
	if form.has_key('email'):
		email=form['email'].value
	else:	email=''
	if form.has_key('reason'):
		reason=form['reason'].value
	else:	reason=''
	
	print """Please enter your contact information.<br><br>
	<form>
	<table>"""
	print '<tr><td>Name:</td><td><input type=text name=name value="%s"></td></tr>' % name
	print '<tr><td>Organization:</td><td><input type=text name=org value="%s"></td></tr>' % org
	print '<tr><td>Address:</td><td><input type=text name=address value="%s"></td></tr>' % address
	print '<tr><td>City:</td><td><input type=text name=city value="%s"></td></tr>' % city
	print '<tr><td>State:</td><td><input type=text name=state value="%s"></td></tr>' % state
	print '<tr><td>Zip:</td><td><input type=text name=zip value="%s"></td></tr>' % zip
	print '<tr><td>Phone Number:</td><td><input type=text name=phone value="%s"></td></tr>' % phone
	print '<tr><td>Email:</td><td><input type=text name=email value="%s"></td></tr>' % email
	print '<tr><td>Project to access:</td><td><input type=text name=project_name value="%s"></td></tr>' % project_name
	print '<tr><td>Reason for access:</td><td><textarea name=reason rows=5 cols=20>%s</textarea></td></tr>' % reason
	print """<tr><td><input type=submit name=submit value=Submit></td></tr>
	</table>"""
#	if form.has_key('project_name'):
#		print "<input type=hidden name=project_name value=%s>" % form['project_name'].value
	print '</form>'

def sendEmail():
	subject="New user for %s project" % form['project_name'].value
	content="Name: %s\n" % form['name'].value
	content=content+"Organization: %s\n" % form['org'].value
	content=content+"Address: %s\n" % form['address'].value
	content=content+"City: %s\n" % form['city'].value
	content=content+"State: %s\n" % form['state'].value
	content=content+"Zip: %s\n" % form['zip'].value
	content=content+"Phone Number: %s\n" % form['phone'].value
	content=content+"Email: %s\n" % form['email'].value
	content=content+"Reason for Access: %s\n" % form['reason'].value


	try:
		pmt_utils.send_email('localhost',form['email'].value,['cm@isrparc.org'], subject, content)
	except smtplib.SMTPSenderRefused:
		getData()
		print "<br><font color=red><b>The email you entered is invalid.</b></font>"
		return

	if form.has_key('project_name'):
		if string.upper(form['project_name'].value)=="USAFSR":
			print "Thank you for your interest in the MultiUAV research software.  An email will be sent to %s with your username and password.<br><br>For further information please call (304)368-9300 x237" % form['email'].value
		else:
			print "An email will be sent to %s with your username and password." % form['email'].value

	print '<form>'
	print '<input type=submit value="Close Window" name=submit onClick=self.close()>'
	print '</form>'



form = pmt_utils.getFormData()

if form.has_key('project_name'):
	print '<html><title>Register for access to %s website</title>' % form['project_name'].value
else:
	print '<html><title>Register for access to project website</title>'

print '<body background="../icons/circ_bg.jpg">'

if form.has_key('name'):
	if validate()=='true':
		sendEmail()
	else:
		getData()
		print "<br><font color=red><b>All fields are required.</b></font>"
else:
	getData()

print '</body></html>'
