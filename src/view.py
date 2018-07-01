# $Id$
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

pmt_utils.htmlContentType()
form = pmt_utils.getFormData()



#-------------------------------------------------------------------------------
def getDetails(file=None):
	details={'name':'', 'date':'', 'version':'','description':''}
	if file==None:
		return details

	path,filename=os.path.split(file)
	filename,ext=os.path.splitext(filename)
	# if the filename has more than 1 period in it replace them with _
	if string.count(filename,".") > 1:
		filename = string.replace(filename,".","_")
	file=path+'/'+filename+ext
	
	status, lines = file_io.readFromFile(file)

	if status!='success':
		print "Can't read file"
		sys.exit()

	descIdx=0
	descEnd=0
	i=0
	oldversion=0
	for line in lines:
		word=string.split(line)
		if len(word)==0:
			continue
		else: end_index=len(word)-1
		if string.find(word[0],'Data')!=-1:
			details['name'] = string.join(word[3:end_index])
		elif string.find(word[0],'Version')!=-1:
			details['version'] = string.join(word[1:end_index])
		elif string.find(word[0],'Date')!=-1:
			if word[2]=='[':
				oldversion=1
				continue
			details['date'] = string.join(word[2:end_index])
			#details['date'] = string.split(details['date'],'@')[0]
		elif string.find(word[0],'Description')!=-1:
			descIdx=i+oldversion
		elif (oldversion==0) and (string.upper(word[0][:7])=='</TABLE'):
			descEnd=i+oldversion
		elif (oldversion==1) and (string.upper(word[0][:6])=='</BODY'):
			descEnd=i+oldversion
		i=i+1

	details['description']=string.join(lines[descIdx:descEnd])
	if oldversion==0:
		details['description']=string.split(details['description'],'<TD>')[2]
		details['description']=string.split(details['description'],'<BR>')[0]
	else:   details['description']=string.split(details['description'],'<BR>')[1]
	return details
#-------------------------------------------------------------------------------


#-------------------------------------------------------------------------------
def viewDetails():

	# get the current data if it exists
	html_filename=form['filename'].value

	# if the filename has more than 1 period in it replace them with _
	if string.count(html_filename,".") > 1:
		html_filename = string.replace(html_filename,".","_")


	file='/home/%s/documents/%s/%s.html' % (form['project'].value,form['directory'].value,form['filename'].value)
	details=getDetails(file)
	# write detail info in HTML format
	print '<HTML><HEAD><TITLE>Data Item Details for: %s</TITLE></HEAD><BODY>' % (form['filename'].value)
	pmt_utils.bodySetup()
	print '<CENTER><B><FONT COLOR="#000099">Data Item Details Page</FONT></B><HR SIZE=1 NOSHADE WIDTH=100%>'

	print '<TABLE border=0>'
	print '<TR><TD><B>Data Item Name:</B></TD><TD> %s <BR>' % (details['name'])
	print '<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % (details['date'])
	print '<TR><TD><B>Filename:</B></TD><TD> %s <BR>' % (form['filename'].value)
	print '<TR><TD><B>Version:</B></TD><TD> %s <BR>' % (details['version'])
	print '<TR><TD><B>Location:</B></TD><TD> %s <BR>' % (form['directory'].value)
	print '<TR><TD><B>Description:</B></TD><TD> %s <BR>' % (details['description'])
	print '</TABLE>'

	print '<HR><form method="POST"'
	print '<input type="button" value="Close Window" onClick="self.close()">'
	print '</form>'
	print '</BODY></HTML>'

#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
def viewLinkDetails():

	name=href=date=description=None

	if os.path.exists(form['file'].value):
		bookmarks=open(form['file'].value,'r')
	else:	sys.exit()

	lines=bookmarks.readlines()
	for line in lines:
		words=string.split(line)
		if words[0]==form['link'].value:
			name=words[2]
			i=3
			while words[i]!='|':
				name=name+' '+words[i]
				i=i+1
			href=words[i+1]
			date=words[i+3]
			description=string.join(words[i+5:],' ')

	bookmarks.close()

	print '<HTML><HEAD><TITLE>Data Item Details for: %s</TITLE></HEAD><BODY>' % (name)
	pmt_utils.bodySetup()
	print '<CENTER><B><FONT COLOR="#000099">Data Item Details Page</FONT></B><HR SIZE=1 NOSHADE WIDTH=100%>'

	print '<TABLE border=0>'
	print '<TR><TD><B>Data Item Name:</B></TD><TD> %s <BR>' % (name)
	print '<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % (date)
	print '<TR><TD><B>Target:</B></TD><TD> %s <BR>' % (href)
	print '<TR><TD><B>Description:</B></TD><TD> %s <BR>' % (description)
	print '</TABLE>'

	print '<HR><form method="POST"'
	print '<input type="button" value="Close Window" onClick="self.close()">'
	print '</form>'
	print '</BODY></HTML>'



#-------------------------------------------------------------------------------



#-------------------------------------------------------------------------------
if form.has_key('filename'):
	viewDetails()
elif form.has_key('link'):
	viewLinkDetails()
else:
	print "No Comprende"
#-------------------------------------------------------------------------------
