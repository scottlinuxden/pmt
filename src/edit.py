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
import shutil


#------------------------------------------------------------------------------
def validate():
    valid='true'

    if form['name'].value=='':
        valid='false'
    if form['target'].value=='':
        valid='false'
    if form['description'].value=='':
        valid='false'

    return valid

#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def editDetails(filepath, filename):

    # get the current data if it exists
    html_filename=form['filename'].value

    # if the filename has more than 1 period in it replace them with _
    if string.count(html_filename,".") > 1:
        html_filename = string.replace(html_filename,".","_")
    if os.path.exists(filepath+'/'+html_filename+'.html'):
        details=getDetailsFromFile(filepath+'/'+html_filename+'.html',
				   form['filename'].value)
    else: 
        details=getDetailsFromFile()
	theTime=time.localtime(os.stat(filename)[stat.ST_MTIME])
        details['date']=time.strftime('%m/%d/%y', theTime)

    print '<center><h2>Edit details of file %s</h2>' % form['filename'].value

    print '<P><form action="/%s-cgi-bin/edit.pyc" method="POST" ' % (db_name)
    print 'enctype="multipart/form-data">'
    print '<TABLE BORDER=0>'

    # display the name of the data item
    print "<TR><TD><B>Data Item Name</B>:</TD><TD>"
    pmt_utils.textbox(None, 'name', details['name'], '30', '40', None, None)
    print "</TD></TR>"

    # display date entered and filename
    print "<TR><TD><B>Date Entered</B>:</TD><TD>%s" % details['date']
    print '<input name=date type=hidden value="%s">' % (details['date'])
    print "</TD></TR>"
    print "<TR><TD><B>Filename</B>:</TD><TD>%s" % form['filename'].value
    print '<input name=filename type=hidden value="%s">'%(form['filename'].value)
    print "</TD></TR>"

    # display the version field
    print "<TR><TD><B>Version:</B></TD><TD>"
    pmt_utils.textbox(None, 'version',
		      details['version'],
		      '30', '40', None, None)
    print "</TD></TR>"

    # display the description field
    print "<TR><TD><B>Description:</B></TD><TD>"
    pmt_utils.textarea(None, 'description',
		       details['description'],
		       '5', '25', None, None)
    print '</TABLE>'

    print '<input name=filepath type=hidden value=%s>' % (filepath)

    print '<input name="submit" type="submit" value="Save">'
    print '<input name="Close Window" type="button" value="Close Window"'
    print 'onClick=self.close()'
    print '</form>'
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def getDetailsFromFile(file=None, original=None):
    details={'name':'', 'date':'', 'version':'','description':''}
    if file==None:
        return details

    status, lines = file_io.readFromFile(file)

    oldversion=0
    descIdx=0
    descEnd=0
    i=0
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
                dir, filename = os.path.split(file)
		mod=os.stat(dir+'/'+original)[stat.ST_MTIME]
                details['date']=time.strftime('%m/%d/%y',time.localtime(mod))
                continue
            details['date'] = string.join(word[2:end_index])
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
    else :
        details['description']=string.split(details['description'],'<BR>')[1]
    return details
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
def updateDetails(filename, full_path):
    index = string.find(full_path,'documents')
    folder = full_path[index+10:]
    if folder!='':
        data = os.stat(full_path+'/'+filename)
    else:
        folder = '/'
        data=os.stat(full_path+filename)
    date=time.strftime('%m/%d/%y',time.localtime(data[8]))

    # write detail info in HTML format
    lines = []
    lines.append('<HTML><HEAD><TITLE>Data Item Details for: %s' % filename)
    lines.append('</TITLE></HEAD><BODY>')
    lines.append('<body background="/%s/icons/circ_bg.jpg">' % (db_name))
    lines.append('<CENTER><B><FONT COLOR="#000099">Data Item Details Page')
    lines.append('</FONT></B><HR SIZE=1 NOSHADE WIDTH=100%>')

    lines.append('<TABLE border=0 align=center><TR><TD><B>')
    lines.append('Data Item Name:</B></TD><TD> %s <BR>' % (form['name'].value))
    lines.append('<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % (form['date'].value))
    lines.append('<TR><TD><B>Filename:</B></TD><TD> %s <BR>' % (filename))
    lines.append('<TR><TD><B>Version:</B></TD><TD> %s <BR>' % (form['version'].value))
    lines.append('<TR><TD><B>Location:</B></TD><TD> %s <BR>' % (folder))
    lines.append('<TR><TD><B>Description:</B></TD><TD> %s <BR>' % (form['description'].value))
    lines.append('</TABLE>')

    lines.append('<HR><form method="POST" >')
    lines.append('<input type="button" value="Close Window" ')
    lines.append('onClick="return closerefresh()">')
    lines.append('</FORM></CENTER></BODY></HTML>')

    # if the filename has more than 1 period in it replace them with _
    if string.count(filename,".") > 1:
        filename = string.replace(filename,".","_")

    for line in lines:
        print line

    # create html file with detail info
    status,details=file_io.writeToFile('%s/%s.html'%(full_path,filename),lines)
    
    if status != 'success':
        file=open(fullpath+filename+'.html','w')
        file.close()
        file_io.writeToFile('%s/%s.html'%(full_path,filename), lines)
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def linkDetails():
    name=href=date=description=None

    if os.path.exists(form['file'].value):
        bookmarks=open(form['file'].value,'r')
    else:
        sys.exit()

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


    print '<center><h2>Edit details of link %s</h2>' % name

    print '<P><form action="/%s-cgi-bin/edit.pyc" method="POST" '% (db_name)
    print 'enctype="multipart/form-data">' 
    print '<TABLE BORDER=0>'

    # display the name of the data item
    print "<TR><TD><B>Link Name</B>:</TD><TD>"
    pmt_utils.textbox(None, 'name', name, '30', '40', None, None)
    print "</TD></TR>"

    # display date entered and href of target
    print "<TR><TD><B>Date Entered</B>:</TD><TD>%s" % date
    print '<input name=date type=hidden value="%s">' % date
    print "</TD></TR>"
    print "<TR><TD><B>Target</B>:</TD><TD>"
    pmt_utils.textbox(None, 'target', href, '30', '256', None, None)
    print "</TD></TR>"

    # display the description field
    print "<TR><TD><B>Description:</B></TD><TD>"
    pmt_utils.textarea(None, 'description', description, '5', '25', None, None)
    print '</TABLE>'

    print '<input name="file" type="hidden" value="%s">' % form['file'].value
    print '<input name="link" type="hidden" value="%s">' % form['link'].value
    print '<input name="submit" type="submit" value="Save">'
    print '<input name="Close Window" type="button" value="Close Window"'
    print ' onClick=self.close()>'
    print '</form>'
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
def updateLinkDetails():

    description=string.replace(form['description'].value,'\n',' ')
    description=string.replace(description,'\r',' ')

    shutil.copy(form['file'].value,'%s.backup' % (form['file'].value,))
    #os.system('cp %s %s.backup' % (form['file'].value,form['file'].value))
    backup=open('%s.backup' % form['file'].value,'r')
    bookmarks=open(form['file'].value,'w')

    lines=backup.readlines()
    for line in lines:
        words=string.split(line)
        if words[0]==form['link'].value:
            newline="%s | %s | %s | %s | %s\n" % (form['link'].value,
						  form['name'].value, 
						  form['target'].value, 
						  form['date'].value, 
						  description)

            bookmarks.write(newline)
        else:
            bookmarks.write(line)
            
    backup.close()
    bookmarks.close()
    
    print '<CENTER><B><FONT COLOR="#000099">'
    print 'Data Item Details Page'
    print '</FONT></B><HR SIZE=1 NOSHADE WIDTH=100%>'
    print '<TABLE border=0 align=center>'
    print '<TR><TD><B>Data Item Name:</B></TD><TD> %s <BR>' % (form['name'].value)
    print '<TR><TD><B>Date Entered:</B></TD><TD> %s <BR>' % (form['date'].value)
    print '<TR><TD><B>Target:</B></TD><TD> %s <BR>' % (form['target'].value)
    print '<TR><TD><B>Description:</B></TD><TD> %s <BR>' % (form['description'].value)
    print '</TABLE>'

    print '<HR><form method="POST" >'
    print '<input type="button" value="Close Window" '
    print 'onClick="return closerefresh()">'
    print '</form>'
    print '</CENTER>'
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
pmt_utils.htmlContentType()
form = pmt_utils.getFormData()
db_name=declarations.pmt_info['db_name']

print "<HTML>"
print "<HEAD>"
print '<SCRIPT TYPE="text/javascript">'
print 'pmt_utils.title("Edit Document Details")'
print '<!--'
print 'function closerefresh()'
print '{'
print 'if (! (window.focus && window.opener))'
print '   return true;'
print 'window.opener.focus();'
print 'window.close();'
print 'if (opener.top.location != opener.location) {'
print '  opener.location.reload();}'
print 'return false;'
print '}'
print '//-->'
print '</SCRIPT>'
print "</HEAD>"
pmt_utils.bodySetup()
print '<Font Face="SerpentineSansICG,Arial">'



# call function based on form keys
if form.has_key('project') and \
   form.has_key('directory') and \
   form.has_key('filename'):
    # get the filename to modify details of
    filepath='/home/%s/documents/%s' % ( db_name, form['directory'].value)
    filename=filepath + '/' + form['filename'].value
    editDetails(filepath,filename)
    
elif form.has_key('filename') and form.has_key('filepath'):
    updateDetails(form['filename'].value, form['filepath'].value)

elif form.has_key('link') and \
     form.has_key('file') and not \
     form.has_key('target'):
    linkDetails()
elif form.has_key('target'):
    if validate()=='true':
        updateLinkDetails()
    else:
        linkDetails()
        print '<br><font color=red><b>All fields are required.</b></font>'
else:
    print "No Comprende"

print '</BODY>'
print '</HTML>'
#------------------------------------------------------------------------------
