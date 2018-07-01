# $Id$
#
# COPYRIGHT:
#   Copyright (C) 1999 LinuXden, All Rights Reserved
#   Copright Statement at http://www.linuxden.com/copyrighted_apps.html
#
# AUTHOR: 
#   Lane LiaBraaten
#
# CONTACT:
#   R. Scott Davis
#   E-mail: scott.davis@linuxden.com
#
import pmt_utils

pmt_utils.htmlContentType()
form=pmt_utils.getFormData()

print '<HTML><HEAD>'
print '<META HTTP-EQUIV="Content-Type" CONTENT="text/html;charset=iso-8859-1">'
print '<META NAME="Author" CONTENT="Information Request">'
print '<META NAME="GENERATOR" CONTENT="Mozilla/4.03 [en](Win95;I) [Netscape]">'
print '<TITLE>Site Access Denied</TITLE></HEAD>'
print '<BODY BACKGROUND="/icons/circ_bg.jpg">'
print '<CENTER><B><FONT COLOR="#990000"><FONT SIZE=+0>'
print 'SITE ACCESS DENIED</FONT></FONT></B></CENTER>'
print '<HR WIDTH="100%"><B><FONT COLOR="#990000">'
print 'You have entered an invalid username/password while trying to access '
print 'a project '
print 'website.</FONT></B><BR>'

if form.has_key('project_name'):
	if form['project_name'].value=='save':
		project='IFCS'
	else:
		project=form['project_name'].value
else:
	project=''

print '<BR> If you would like to request a username/password to access a '
print 'project '
print '<A HREF="/cgi-bin/register.pyc?project_name=%s">click</A>' % project
print 'here.<BR><BR>'
print 'If you have been granted access to a project website but are '
print 'having problems logging in, contact '
print '<A HREF="mailto:scott.davis@linuxden.com">Support</A>'
print '<P><B><FONT COLOR="#000000"><FONT SIZE=-1><CENTER>'
print 'Unauthorized access to this site or tampering with data at this'
print 'site is strictly prohibited.</CENTER></FONT></FONT></B></BODY></HTML>'
